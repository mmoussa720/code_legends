from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from .database import async_session


#Database
AsyncSessionDep=Annotated[AsyncSession,Depends(async_session)]

#Users
