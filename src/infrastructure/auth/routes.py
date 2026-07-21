from typing import Annotated

from fastapi import APIRouter, Body, status
from .schemas import Request, Token
from ..dependencies import AsyncSessionDep
from .dependencies import AuthServiceDep
from ...modules.users.dependencies import UserServiceDep
from ...modules.users.schemas import UserCreate

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary="Authenticates a user",

    description="This endpoint authenticates a user by its username and password",
    responses={404: {"description":"User not found"},200:{"description":"Login successful"},401:{"description":"Invalid credentials"}}
)
async def login(
    request: Annotated[Request, Body(description="The body of the login method")],
    db: AsyncSessionDep,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    return await auth_service.login(request, db, user_service)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    summary="register a user",
    description="This endpoint authenticates a user by its username and password",
    responses={409: {"description":"User already exists"},400:{"description":"Invalid data"},201:{"description":"User created and logged in successfully"}}
)
async def register(
    request: Annotated[UserCreate, Body(description="The body of the register method")],
    db: AsyncSessionDep,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    return await auth_service.register(request, db, user_service)
