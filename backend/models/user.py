import uuid
from datetime import datetime
from typing import List

from _decimal import Decimal
from sqlalchemy import UUID, Numeric, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.database.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    balance_cents: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    orders: Mapped[List["Order"]] = relationship("Order",back_populates="user")
