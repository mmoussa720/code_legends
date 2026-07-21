from .schemas import (
    CategoryUpdate,
    CategoryRead,
    CategoryCreateInternal,
    CategoryCreate, CategoryUpdateInternal,
)
from .models import Category
from .crud import crud_categories
from src.infrastructure.common.helpers import generate_slug
from .exceptions import CategoryExistsError, CategoryNotFoundError, CategoryCreationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class CategoryService:
    async def get_categories_paginated(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        data = await crud_categories.get_multi(
            db, schema_to_select=CategoryRead, offset=skip, limit=limit
        )
        return data

    async def create_category(
        self, category: CategoryCreate, db: AsyncSession
    ) -> dict[str, Any]:
        slug = generate_slug(category.name)
        slug_exists = await crud_categories.exists(db=db, slug=slug)
        if slug_exists:
            raise CategoryExistsError("Category with this name already exists")
        category_internal_dict = category.model_dump()
        category_internal_dict["slug"] = slug
        category_internal = CategoryCreateInternal(**category_internal_dict)
        created_category = await crud_categories.create(
            db=db, object=category_internal, schema_to_select=CategoryRead
        )
        if not created_category:
            raise CategoryCreationError("Failed to create category")
        return created_category

    async def find_category_by_slug(
        self, slug: str, db: AsyncSession
    ) -> CategoryRead:
        category = await crud_categories.get(
            db=db, slug=slug, schema_to_select=CategoryRead
        )
        if not category:
            raise CategoryNotFoundError("Category not found")
        return category

    async def delete_a_category(self, slug: str, db: AsyncSession):
        category = await crud_categories.get(
            db=db, slug=slug, schema_to_select=CategoryRead
        )
        if not category:
            raise CategoryNotFoundError("Category not found")
        await crud_categories.delete(db=db, slug=slug)
        return {"message": "Category deleted successfully"}

    async def update_category(
        self, data: CategoryUpdate, slug: str, db: AsyncSession
    ):
        category = await crud_categories.get(
            slug=slug, db=db, schema_to_select=CategoryRead
        )
        if not category:
            raise CategoryNotFoundError("This category doesn't exist")
        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] != category["name"]:
            new_slug = generate_slug(update_data["name"])
            slug_exists = await crud_categories.exists(
                db=db, slug=new_slug
            )
            if slug_exists:
                raise CategoryExistsError(
                    "A category with this name already exists"
                )
            update_data["slug"] = new_slug
        print(update_data)
        updated_category = await crud_categories.update(
            db=db,
            object=CategoryUpdateInternal(**update_data),
            slug=slug,
            return_columns=list(CategoryRead.model_fields.keys()),
        )
        return updated_category
