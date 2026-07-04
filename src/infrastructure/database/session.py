from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
from ..config.settings import settings
from collections.abc import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase,MappedAsDataclass

class Base(DeclarativeBase,MappedAsDataclass):
    pass

engine=create_async_engine(
    settings.DATABASE_URL
)

local_session=async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
async def async_session()->AsyncGenerator[AsyncSession,None]:
    async_get_db=local_session
    async with async_get_db() as db:
        yield db
    
async def create_tables()->None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    