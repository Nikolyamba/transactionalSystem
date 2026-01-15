import uuid
from datetime import datetime
from typing import List

from _decimal import Decimal
from sqlalchemy import UUID, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    price_cents: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    inventory: Mapped["Inventory"] = relationship("Inventory", back_populates="product", uselist=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")