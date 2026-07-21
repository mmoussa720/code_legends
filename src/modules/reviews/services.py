from .schemas import (
    ReviewUpdate,
    ReviewRead,
    ReviewCreateInternal,
    ReviewCreate, ReviewBase,
)
from .models import Review
from .crud import crud_reviews
from .exceptions import (
    ReviewExistsError,
    ReviewNotFoundError,
    ReviewCreationError,
    UserNotFoundForReviewError,
    ProductNotFoundForReviewError,
)
from ...modules.products.crud import crud_products
from ...modules.users.crud import crud_users
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class ReviewService:
    async def get_reviews_by_product(
        self, product_slug: str, db: AsyncSession
    ) -> dict[str, Any]:
        product = await crud_products.get(db=db, slug=product_slug)
        if not product:
            raise ProductNotFoundForReviewError("Product not found")
        data = await crud_reviews.get_multi(
            db, schema_to_select=ReviewRead, product_id=product["id"]
        )
        return data

    async def create_review(
        self, review: ReviewCreate, user_id: str, db: AsyncSession
    ) -> dict[str, Any]:
        user = await crud_users.get(db=db, id=user_id)
        if not user:
            raise UserNotFoundForReviewError("User not found")
        product = await crud_products.get(db=db, slug=review.product_slug)
        if not product:
            raise ProductNotFoundForReviewError("Product not found")
        existing_review = await crud_reviews.exists(
            db=db, user_id=user_id, product_id=product["id"]
        )
        if existing_review:
            raise ReviewExistsError("You have already reviewed this product")
        review_internal_dict = review.model_dump(exclude={"product_slug"})
        review_internal_dict["user_id"] = user_id
        review_internal_dict["product_id"] = product["id"]
        review_internal = ReviewCreateInternal(**review_internal_dict)
        created_review = await crud_reviews.create(
            db=db, object=review_internal, schema_to_select=ReviewRead
        )
        if not created_review:
            raise ReviewCreationError("Failed to create review")
        return created_review

    async def get_product_average_rating(
        self, product_slug: str, db: AsyncSession
    ) -> float:
        product = await crud_products.get(db=db, slug=product_slug)
        if not product:
            raise ProductNotFoundForReviewError("Product not found")
        reviews = await crud_reviews.get_multi(
            db=db, product_id=product["id"]
        )
        data = reviews.get("data", [])
        if not data:
            return 0.0
        total = sum(r["rating"] for r in data)
        return round(total / len(data), 2)

    async def update_review(
        self, data: ReviewUpdate, review_id: str, user_id: str, db: AsyncSession
    ):
        review = await crud_reviews.get(
            id=review_id, db=db, schema_to_select=ReviewRead
        )
        if not review:
            raise ReviewNotFoundError("Review not found")
        if review["user_id"] != user_id:
            raise ReviewCreationError("You can only update your own review")
        updated_review = await crud_reviews.update(
            db=db,
            object=data,
            id=review_id,
            return_columns=list(ReviewRead.model_fields.keys()),
        )
        return updated_review

    async def delete_review(self, review_id: str, user_id: str, db: AsyncSession):
        review = await crud_reviews.get(
            id=review_id, db=db, schema_to_select=ReviewRead
        )
        if not review:
            raise ReviewNotFoundError("Review not found")
        if review["user_id"] != user_id:
            raise ReviewCreationError("You can only delete your own review")
        await crud_reviews.delete(db=db, id=review_id)
        return {"message": "Review deleted successfully"}
