from .schemas import (
    ProductUpdate,
    ProductRead,
    ProductCreateInternal,
    ProductCreate, ProductBase, ProductUpdateInternal,
)
from .models import Product, ProductCategory
from .crud import crud_products
from src.infrastructure.common.helpers import generate_slug
from .exceptions import ProductExistsError, ProductNotFoundError, ProductCreationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any

from ..categories import CategoryNotFoundError, CategoryExistsError
from ..categories.crud import crud_categories


class ProductService:
    async def get_products_paginated(
        self, db: AsyncSession, skip: int = 0, limit: int = 100, category_slug: str | None = None
    ) -> dict[str, Any]:
        if category_slug:
            from ...modules.categories.crud import crud_categories
            category = await crud_categories.get(db=db, slug=category_slug)
            if not category:
                raise ProductNotFoundError("Category not found")
            data = await crud_products.get_multi(
                db,
                schema_to_select=ProductRead,
                offset=skip,
                limit=limit,
                category_ids=[category["id"]],
            )
        else:
            data = await crud_products.get_multi(
                db, schema_to_select=ProductRead, offset=skip, limit=limit
            )
        return data

    async def create_product(
        self, product: ProductCreate, image_url: str | None, db: AsyncSession
    ) -> dict[str, Any]:
        print(1)
        slug = generate_slug(product.name)
        print(2)
        slug_exists = await crud_products.exists(db=db, slug=slug)
        print(3)
        if slug_exists:
            raise ProductExistsError("Product with this name already exists")
        for cat in product.category_ids:
            category_exists = await crud_categories.exists(db=db, id=cat)
            if not category_exists:
                raise CategoryNotFoundError(f"category with id ${cat} doesn't exist")
        product_internal_dict = product.model_dump(exclude={"category_ids"})
        product_internal_dict["slug"] = slug
        product_internal_dict["image_url"] = image_url
        product_internal = ProductCreateInternal(**product_internal_dict)
        print(product_internal)
        created_product = await crud_products.create(
            db=db, object=product_internal, schema_to_select=ProductRead
        )
        if not created_product:
            raise ProductCreationError("Failed to create product")
        for cat_id in product.category_ids:
            await db.execute(
                ProductCategory.__table__.insert().values(
                    product_id=created_product["id"], category_id=cat_id
                )
            )
        await db.commit()
        return created_product

    async def find_product_by_slug(
        self, slug: str, db: AsyncSession
    ) -> ProductRead:
        product = await crud_products.get(
            db=db, slug=slug, schema_to_select=ProductRead
        )
        if not product:
            raise ProductNotFoundError("Product not found")
        return product

    async def delete_a_product(self, slug: str, db: AsyncSession):
        product = await crud_products.get(
            db=db, slug=slug, schema_to_select=ProductRead
        )
        if not product:
            raise ProductNotFoundError("Product not found")
        await crud_products.delete(db=db, slug=slug)
        return {"message": "Product deleted successfully"}

    async def update_product(
        self, data: ProductUpdate, slug: str, image_url: str | None, db: AsyncSession
    ):
        product = await crud_products.get(
            slug=slug, db=db, schema_to_select=ProductRead
        )
        print(product)
        if not product:
            raise ProductNotFoundError("This product doesn't exist")
        update_data = data.model_dump(exclude_unset=True, exclude={"category_ids"})
        print(update_data)
        if "name" in update_data and update_data["name"] != product["name"]:
            new_slug = generate_slug(update_data["name"])
            slug_exists = await crud_products.exists(db=db, slug=new_slug)
            if slug_exists:
                raise ProductExistsError("A product with this name already exists")
            update_data["slug"] = new_slug
        if image_url:
            update_data["image_url"] = image_url
        updated_product = await crud_products.update(
            db=db,
            object=ProductUpdateInternal(**update_data),
            slug=slug,
            return_columns=list(ProductRead.model_fields.keys()),
        )
        print("worked correctly")
        if "category_ids" in data.model_dump(exclude_unset=True) and data.category_ids is not None:
            for cat_id in data.category_ids:
                existing=await db.execute(ProductCategory.__table__.select().where(
                    ProductCategory.product_id==product["id"],ProductCategory.category_id==cat_id
                ))
                if existing.scalar_one_or_none() is None:
                    await db.execute(
                        ProductCategory.__table__.insert().values(
                            product_id=product["id"], category_id=cat_id
                        )
                    )
                else:
                    raise CategoryExistsError("This category is already set to this product")
            await db.commit()
        return updated_product
