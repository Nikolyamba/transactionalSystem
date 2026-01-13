import uuid
from datetime import datetime

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

from enum import Enum as PyEnum

from backend.models.order import Order

class PaymentStatus(PyEnum):
    pending = 'pending'
    success = 'success'
    failed = 'failed'

class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.pending)
    idempotency_key: Mapped[uuid.UUID] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    order: Mapped["Order"] = relationship("Order", back_populates="payments")