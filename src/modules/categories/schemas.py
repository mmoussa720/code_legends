from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class CategoryBase(BaseModel):
    name: Annotated[
        str, Field(min_length=2, max_length=50, examples=["Electronics"])
    ]
    description: Annotated[str | None, Field(default=None, examples=["All electronic items"])]


class CategoryRead(BaseModel):
    id: Annotated[str, Field(description="The unique id of the category")]
    slug: Annotated[str, Field(description="The slug of the category")]
    name: Annotated[str, Field(description="The name of the category")]
    description: Annotated[
        str | None, Field(description="The description of the category")
    ]


class CategoryCreate(CategoryBase):
    model_config = ConfigDict(extra="forbid")


class CategoryUpdate(BaseModel):
    name: Annotated[
        str | None,
        Field(min_length=2, max_length=50, examples=["Electronics"], default=None),
    ]
    description: Annotated[
        str | None,
        Field(default=None, examples=["All electronic items"]),
    ]

class CategoryUpdateInternal(CategoryUpdate):
    slug:Annotated[
        str | None,
        Field(default=None, examples=["electronics"]),
    ]

class CategoryCreateInternal(CategoryBase):
    slug: str

