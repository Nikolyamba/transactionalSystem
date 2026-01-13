import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.database.base import Base
from backend.models.order import Order

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    balance_cents: Mapped[Numeric] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
