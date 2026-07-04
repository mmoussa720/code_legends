from fastapi import APIRouter,Depends,HTTPException
from .schemas import FighterRead,FighterCreate
from .service import FighterService
from typing import Any
from .exceptions import FighterExistsError
from .dependencies import FighterServiceDep
router=APIRouter(tags=["Fighters"])
from src.infrastructure import AsyncSessionDep
@router.get("/",summary="List All fighters",description="""Retrieves a paginated list of all fighters in the system""",responses={401:{"description":"Not authenticated"},403:{"description":"Not authorized"}},response_description="A paginated list of fighters with total count and pagination metadata")
async def get_fighters(service:FighterServiceDep,db:AsyncSessionDep):
    return await service.get_paginated(db)


@router.post("/",status_code=201,response_model=FighterRead,summary="Create new fighter account",description="""Creates a new fighter account in the system.
                                This endpoint allows registration of new users with their basic information:
                                -First name
                                -Last name
                                -Email address
                                -Password (With security requirements)
             """,responses={201:{"description":"Fighter Account created"},400:{"description":"Invalid fighter data"},409:{"description":"Username of email already exists"}},response_description="The created fighter profile with assigned ID")

async def create_user(fighter:FighterCreate,db:AsyncSessionDep,service:FighterServiceDep)->dict[str,Any]:
    return await service.create(fighter,db)
        
    
    
    
    