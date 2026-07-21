import uuid
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ...infrastructure.database.session import Base


class Review(Base):
    __tablename__ = "review"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product_review"),
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    product_id: Mapped[str] = mapped_column(
        ForeignKey("product.id",ondelete="CASCADE",onupdate="CASCADE"), nullable=False
    )
    comment: Mapped[str | None] = mapped_column(String, default=None)
    id: Mapped[str] = mapped_column(
        "id", unique=True, primary_key=True, default_factory=lambda: str(uuid.uuid4())
    )
    user: Mapped["User"] = relationship(lazy="selectin", init=False)
    product: Mapped["Product"] = relationship(
        back_populates="reviews", lazy="selectin", init=False
    )
