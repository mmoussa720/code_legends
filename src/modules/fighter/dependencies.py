from .service import FighterService
from fastapi import Depends
from typing import Annotated
def get_fighter_service()->FighterService:
    return FighterService()

FighterServiceDep=Annotated[FighterService,Depends(get_fighter_service)]