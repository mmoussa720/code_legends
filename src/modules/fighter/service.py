from .schemas import FighterRead
from uuid import uuid4
from typing import Any
from .crud import crud_fighters
from src.infrastructure import get_password_hash,verify_password
from .exceptions import FighterExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import FighterCreateInternal,FighterCreate
class FighterService:
    async def get_paginated(self,db:AsyncSession)->dict[str,Any]:
        data=await crud_fighters.get_multi(
            db,schema_to_select=FighterRead,
        )
        return data

    async def create(self,fighter:FighterCreate,db:AsyncSession)->dict[str,Any]:
        email_exists=await crud_fighters.exists(db=db,email=fighter.email)
        if email_exists:
            raise FighterExistsError("Email already registred")
        username_exists=await crud_fighters.exists(db=db,user_name=fighter.user_name)
        if username_exists:
            raise FighterExistsError("Username already taken")
        fighter_internal_dict=fighter.model_dump()
        fighter_internal_dict["hashed_password"]=get_password_hash(password=fighter_internal_dict["password"])
        del fighter_internal_dict["password"]
        fighter_internal=FighterCreateInternal(**fighter_internal_dict)
        created_fighter=await crud_fighters.create(db=db,object=fighter_internal,schema_to_select=FighterRead)
        if not created_fighter:
            raise FighterExistsError("Failed to create fighter")
        return created_fighter
        
        