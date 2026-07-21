from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class ProductBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100, examples=["Gaming Mouse"])]
    description: Annotated[str | None, Field(default=None, examples=["A high quality gaming mouse"])]
    price: Annotated[float, Field(gt=0, examples=[49.99])]
    size: Annotated[str | None, Field(default=None, examples=["M"])]
    quantity: Annotated[int, Field(ge=0, default=0, examples=[10])]
    category_ids: Annotated[list[str], Field(description="List of category ids", examples=[["cat_id_1", "cat_id_2"]])]


class ProductRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the product")]
    slug: Annotated[str, Field(description="The slug of the product")]
    name: Annotated[str, Field(description="The name of the product")]
    description: Annotated[str | None, Field(description="The description of the product")]
    price: Annotated[float, Field(description="The price of the product")]
    image_url: Annotated[str | None, Field(description="The image url of the product")]
    size: Annotated[str | None, Field(description="The size of the product")]
    quantity: Annotated[int, Field(description="The quantity of the product")]
    is_new: Annotated[bool, Field(description="Indicates if the product is new")]


class ProductCreate(ProductBase):
    model_config = ConfigDict(extra="forbid")


class ProductUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=100, default=None)]
    description: Annotated[str | None, Field(default=None)]
    price: Annotated[float | None, Field(gt=0, default=None)]
    size: Annotated[str | None, Field(default=None)]
    quantity: Annotated[int | None, Field(ge=0, default=None)]
    category_ids: Annotated[list[str] | None, Field(default=None)]

class ProductUpdateInternal(BaseModel):
    name: Annotated[str | None, Field(min_length=2, max_length=100, default=None)]
    description: Annotated[str | None, Field(default=None)]
    price: Annotated[float | None, Field(gt=0, default=None)]
    size: Annotated[str | None, Field(default=None)]
    quantity: Annotated[int | None, Field(ge=0, default=None)]


class ProductCreateInternal(BaseModel):
    slug: str
    image_url: str | None = None
    name: Annotated[str, Field(min_length=2, max_length=100, examples=["Gaming Mouse"])]
    description: Annotated[str | None, Field(default=None, examples=["A high quality gaming mouse"])]
    price: Annotated[float, Field(gt=0, examples=[49.99])]
    size: Annotated[str | None, Field(default=None, examples=["M"])]
    quantity: Annotated[int, Field(ge=0, default=0, examples=[10])]

