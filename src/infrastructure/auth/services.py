from asyncpg.pgproto.pgproto import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession

from .crud import auth_crud
from .exceptions import LoginError
from .helpers import get_current_user, create_token, authenticate_user
from ...modules.users.schemas import UserCreate, UserRead
from ...modules.users.services import UserService
from .schemas import Request, Token, TokenData, CreateTokenInDB
from dotenv import load_dotenv
import os

load_dotenv()


class AuthService:
    async def login(self, request: Request, db: AsyncSession, service: UserService):
        user = await authenticate_user(
            db, username=request.user_name, password=request.password
        )
        if not user:
            raise LoginError("invalid username or password")
        access_token_expires = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        refresh_token_expires = timedelta(
            days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
        )
        access_token = create_token(
            data=TokenData(
                sub=user.user_name,
                email=user.email,
                is_super_user=user.is_super_user,
            ).model_dump(),
            expires_delta=access_token_expires,
        )
        refresh_token = create_token(
            data={"sub": user.user_name, "role": user.role},
            expires_delta=refresh_token_expires,
        )
        data = await auth_crud.create(
            db=db, object=CreateTokenInDB(token=refresh_token, user_id=user.id)
        )
        return Token(access=access_token, refresh=refresh_token)

    async def register(self, request: UserCreate, db: AsyncSession, service: UserService):
        created_user=await service.create_user(db=db,user=request)
        user=UserRead(**created_user)
        access_token_expires = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
        refresh_token_expires = timedelta(
            days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
        )
        access_token = create_token(
            data=TokenData(
                sub=user.user_name,
                email=user.email,
                is_super_user=user.is_super_user,
            ).model_dump(),
            expires_delta=access_token_expires,
        )
        refresh_token = create_token(
            data={"sub": user.user_name, "role": user.role},
            expires_delta=refresh_token_expires,
        )
        data = await auth_crud.create(
            db=db, object=CreateTokenInDB(token=refresh_token, user_id=user.id)
        )
        return Token(access=access_token, refresh=refresh_token)
