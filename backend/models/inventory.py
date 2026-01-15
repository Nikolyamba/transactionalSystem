import uuid

from sqlalchemy import UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

class Inventory(Base):
    __tablename__ = "inventories"

    product_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        primary_key=True
    )
    total_quantity: Mapped[int] = mapped_column(nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    sold_quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    product: Mapped["Product"] = relationship("Product", back_populates="inventory")

    __table_args__ = (
    CheckConstraint("reserved_quantity >= 0"),
    CheckConstraint("sold_quantity >= 0"),
    CheckConstraint("total_quantity >= reserved_quantity + sold_quantity"),
    )