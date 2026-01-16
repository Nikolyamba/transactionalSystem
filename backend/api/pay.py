import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.models.payment import PaymentStatus

pay_router = APIRouter(prefix='/pay')

class PayRequest(BaseModel):
    order_id: uuid.UUID
    status: PaymentStatus.pending
    idempotency_key: str

@pay_router.post("")
async def make_payment(data: PayRequest, db: AsyncSession = Depends(get_db)) -> dict:
    async with db.begin():
        result = await db.execute(text("""
            SELECT id, user_id, product_id, amount_cents, status
            FROM orders
            WHERE id = :order_id
            FOR UPDATE
            """),
            {"order_id": data.order_id}
                            )

        order = result.fetchone()
        if not order:
            raise HTTPException(404, "Order not found")

        if order.status == "paid":
            return {"status": "already_paid"}

        if order.status != "pending":
            raise HTTPException(409, "Order cannot be paid")

        try:
            await db.execute(
                text("""
                INSERT INTO payments (order_id, idempotency_key, status)
                VALUES (:order_id, :key, 'pending')
                """),
                {"order_id": order.id, "key": data.idempotency_key}
            )
        except IntegrityError:
            return {"status": "payment_already_processed"}

        # 3. Списываем деньги
        result = await db.execute(
            text("""
            UPDATE users
            SET balance_cents = balance_cents - :amount
            WHERE id = :user_id
            AND balance_cents >= :amount
            RETURNING id
            """),
            {"user_id": order.user_id, "amount": order.amount_cents}
        )

        if result.fetchone() is None:
            await db.execute(
                text("""
                UPDATE payments
                SET status = 'failed'
                WHERE order_id = :order_id
                """),
                {"order_id": order.id}
            )
            raise HTTPException(409, "Insufficient balance")

        # 4. Подтверждаем заказ
        await db.execute(
            text("""
            UPDATE orders
            SET status = 'paid'
            WHERE id = :order_id
            """),
            {"order_id": order.id}
        )

        # 5. Обновляем inventory
        await db.execute(
            text("""
            UPDATE inventories
            SET reserved_quantity = reserved_quantity - 1,
                sold_quantity = sold_quantity + 1
            WHERE product_id = :product_id
            """),
            {"product_id": order.product_id}
        )

    return {"status": "paid"}

class ResponsePayment(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    status: PaymentStatus
    idempotency_key: str
    created_at: datetime


@pay_router.get("/{order_id}", response_model=ResponsePayment)
async def getPayment(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
    SELECT id, order_id, status, idempotency_key, created_at
    FROM payments
    where order_id = :order_id
    """), {'order_id': order_id})

    payment = result.fetchone()

    if not payment:
        raise HTTPException(404, "Payment not found")

    return ResponsePayment(
        id=payment.id,
        order_id=payment.order_id,
        status=payment.status,
        idempotency_key=payment.idempotency_key,
        created_at=payment.created_at
    )



