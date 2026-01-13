import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base
from backend.models.product import Product


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    total_quantity: Mapped[int] = mapped_column(nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(nullable=False)
    sold_quantity: Mapped[int] = mapped_column(nullable=False)

    product: Mapped[Product] = relationship("Product", back_populates="inventory")