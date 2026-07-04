from pydantic import BaseModel,Field,EmailStr,ConfigDict
from typing import Annotated
from uuid import uuid4

class FighterBase(BaseModel):
    first_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Fighter"])]
    last_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Fighterson"])]
    user_name:Annotated[str,Field(min_length=2,max_length=20,examples=["Figher720"])]
    email:Annotated[EmailStr,Field(examples=["fighter.fighterson@example.com"])]

class Fighter(FighterBase):
    hashed_password:str
    profile_image_url:Annotated[str,Field(default="https://www.profileImageUrl.com",description="Url of the fighter's profile image")]
    
    
class FighterRead(BaseModel):
    id:Annotated[str,Field(description="The unique id of the fighter")]
    first_name:Annotated[str,Field(description="The first name of the fighter")]
    last_name:Annotated[str,Field(description="The last name of the fighter")]
    user_name:Annotated[str,Field(description="The user name of the fighter")]
    email:Annotated[EmailStr,Field(description="The email of the fighter")]
    profile_image_url:Annotated[str,Field(description="The profile image url of the fighter")]
    is_deleted:Annotated[bool,Field(description="Soft deletion",default=False)]
    email_verified:bool=False

class FighterCreate(FighterBase):
    password:Annotated[str,Field(examples=["FighterPassword#123"],description="The fighter password",pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$")]
    model_config=ConfigDict(extra="forbid")
    
class FighterUpdate(BaseModel):
    first_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Fighter"])]
    last_name:Annotated[str,Field(min_length=2,max_length=30,examples=["Fighterson"])]
    user_name:Annotated[str,Field(min_length=2,max_length=20,examples=["Figher720"])]
    email:Annotated[EmailStr,Field(examples=["fighter.fighterson@example.com"])]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            examples=["https://www.profileimageurl.com"],
            default=None,
        ),
    ]
    is_deleted:bool=False
    email_verified:bool=False

class FighterCreateInternal(FighterBase):
    hashed_password:str
    