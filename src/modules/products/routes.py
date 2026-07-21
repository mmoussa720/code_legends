from fastapi import APIRouter, Path, Body, Query, UploadFile, File, Form
from .schemas import ProductRead, ProductCreate, ProductUpdate
from typing import Any, Annotated
from .dependencies import ProductServiceDep
from ...infrastructure.dependencies import AsyncSessionDep
import os

router = APIRouter(tags=["Products"])

UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get(
    "/",
    summary="List all products",
    description="Retrieves a paginated list of all products, optionally filtered by category slug",
    response_description="A paginated list of products",
    responses={401: {"description": "Not authenticated"}, 403: {"description": "Not authorized"}},
)
async def get_products(
    service: ProductServiceDep,
    db: AsyncSessionDep,
    skip: Annotated[int, Query(description="Number of records to skip", ge=0)] = 0,
    limit: Annotated[int, Query(description="Maximum number of records", ge=1)] = 100,
    category_slug: Annotated[str | None, Query(description="Filter by category slug")] = None,
):
    return await service.get_products_paginated(db, skip=skip, limit=limit, category_slug=category_slug)


@router.get(
    "/{slug}",
    status_code=200,
    response_model=ProductRead | None,
    summary="Return a product by its slug",
    description="Returns all the necessary product data by its slug",
    response_description="A json item of the desired product",
    responses={200: {"description": "Product data retrieved"}, 404: {"description": "Product not found"}},
)
async def get_product_by_slug(
    slug: Annotated[str, Path(description="The slug of the product")],
    service: ProductServiceDep,
    db: AsyncSessionDep,
):
    return await service.find_product_by_slug(slug, db)


@router.post(
    "/",
    status_code=201,
    response_model=ProductRead,
    summary="Create new product",
    description="Creates a new product. Accepts form data with an optional image upload.",
    response_description="The created product",
    responses={201: {"description": "Product created"}, 400: {"description": "Invalid data"}, 409: {"description": "Product with this name already exists"}},
)
async def create_product(
    name: Annotated[str, Form(min_length=2, max_length=100)],
    description: Annotated[str | None, Form()] = None,
    price: Annotated[float, Form(gt=0)] = ...,
    size: Annotated[str | None, Form()] = None,
    quantity: Annotated[int, Form(ge=0)] = 0,
    category_ids: Annotated[str, Form(description="Comma-separated category ids")] = "",
    image: Annotated[UploadFile | None, File(description="Product image")] = None,
    db: AsyncSessionDep = None,
    service: ProductServiceDep = None,
) -> dict[str, Any]:
    image_url = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename.lower().replace(" ","_"))
        content = await image.read()
        with open(file_path, "wb") as f:
            f.write(content)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"
    product_data = ProductCreate(
        name=name,
        description=description,
        price=price,
        size=size,
        quantity=quantity,
        category_ids=[c.strip() for c in category_ids.split(",") if c.strip()],
    )
    return await service.create_product(product_data, image_url, db)


@router.put(
    "/{slug}",
    status_code=200,
    summary="Update a product",
    description="This endpoint updates a product's data",
    response_description="The updated product data",
    responses={200: {"description": "Product updated"}, 404: {"description": "Product not found"}, 409: {"description": "Product with this name already exists"}},
)
async def update_product(
    slug: Annotated[str, Path(description="The slug of the product")],
    name: Annotated[str | None, Form(min_length=2, max_length=100)] = None,
    description: Annotated[str | None, Form()] = None,
    price: Annotated[float | None, Form(gt=0)] = None,
    size: Annotated[str | None, Form()] = None,
    quantity: Annotated[int | None, Form(ge=0)] = None,
    category_ids: Annotated[str | None, Form(description="Comma-separated category ids")] = None,
    image: Annotated[UploadFile | None, File(description="Product image")] = None,
    db: AsyncSessionDep = None,
    service: ProductServiceDep = None,
):
    image_url = None
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        content = await image.read()
        with open(file_path, "wb") as f:
            f.write(content)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"
    update_data = ProductUpdate(
        name=name,
        description=description,
        price=price,
        size=size,
        quantity=quantity,
        category_ids=[c.strip() for c in category_ids.split(",") if c.strip()] if category_ids else None,
    )
    return await service.update_product(update_data, slug, image_url, db)


@router.delete(
    "/{slug}",
    status_code=200,
    summary="Delete a product",
    description="This endpoint deletes a product from the system",
    response_description="A message confirming the product deletion",
    responses={200: {"description": "Product deleted"}, 404: {"description": "Product not found"}},
)
async def delete_product(
    slug: Annotated[str, Path(description="The slug of the product")],
    db: AsyncSessionDep,
    service: ProductServiceDep,
):
    return await service.delete_a_product(slug, db)
