import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, Text, Float, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base


class ProductCategory(Base):
    __tablename__ = "product_category"
    product_id: Mapped[str] = mapped_column(
        ForeignKey("product.id",ondelete="CASCADE",onupdate="CASCADE"),primary_key=True
    )
    category_id: Mapped[str] = mapped_column(
        ForeignKey("category.id",ondelete="CASCADE",onupdate="CASCADE"), primary_key=True
    )


class Product(Base):
    __tablename__ = "product"
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    image_url: Mapped[str | None] = mapped_column(String, default=None)
    size: Mapped[str | None] = mapped_column(String, default=None)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=None
    )
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    categories: Mapped[List["Category"] | None] = relationship(
        secondary="product_category",
        back_populates="products",
        lazy="selectin",
        default_factory=list,
        init=False,
    )
    reviews: Mapped[List["Review"] | None] = relationship(
        back_populates="product",
        lazy="selectin",
        default_factory=list,
        init=False,
    )
