import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List

from _decimal import Decimal
from sqlalchemy import UUID, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class OrderStatus(str, PyEnum):
    pending = 'pending'
    paid = 'paid'
    cancelled = 'cancelled'
    expired = 'expired'

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.pending)
    amount_cents: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="order")