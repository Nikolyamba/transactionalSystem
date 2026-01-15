import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db
from backend.models import Order
from backend.models.order import OrderStatus

o_router = APIRouter(prefix="/order")

class MakeOrder(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID
    amount_cents: int

@o_router.post("")
async def new_order(data: MakeOrder, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(
            text("""
                    UPDATE inventories
                    SET reserved_quantity = reserved_quantity + 1
                    WHERE product_id = :product_id
                    AND (total_quantity - reserved_quantity - sold_quantity) > 0
                    RETURNING product_id
                    """),
            {"product_id": data.product_id}
        )

        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=409, detail="No available slots")

        order = Order(user_id = data.user_id,
                      product_id = data.product_id,
                      amount_cents=data.amount_cents,
                      status=OrderStatus.pending,
                      )

        db.add(order)

        return {"order_id": order.id, "status": order.status}
