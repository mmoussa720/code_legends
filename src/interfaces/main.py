from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from .api import router
from sqlalchemy import create_engine

from ..infrastructure.database.session import create_tables
from ..modules.fighter.models import Base
from ..infrastructure.database import engine

@asynccontextmanager
async def lifespan(app:FastAPI):
    await  create_tables()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(router=router)


