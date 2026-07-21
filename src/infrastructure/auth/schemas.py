from dataclasses import Field

from pydantic import BaseModel, Field, EmailStr
import os
from dotenv import load_dotenv
from typing import Annotated


class Token(BaseModel):
    access: Annotated[
        str, Field(description="a short-lived token used to verify the user access")
    ]
    refresh: Annotated[
        str, Field(description="a long-lived token used to generate other tokens")
    ]


class TokenData(BaseModel):
    sub: Annotated[
        str,
        Field(
            description="The sub of the token (in our case we are using the username)"
        ),
    ]
    email: Annotated[EmailStr, Field(description="The email of the user")]
    is_super_user: Annotated[
        bool, Field(description="This field indicates if the user is a super user or not")
    ]


class Request(BaseModel):
    user_name: Annotated[str, Field(description="the username of the user",examples=["User720"])]
    password: Annotated[str, Field(description="the password of the user",examples=["UserPassword#123"])]


class CreateTokenInDB(BaseModel):
    user_id: Annotated[str, Field("the id of the authenticated user")]
    token: Annotated[str, Field("the refresh token of the authenticated user")]
