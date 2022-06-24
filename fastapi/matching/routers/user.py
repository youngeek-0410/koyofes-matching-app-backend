from typing import Optional

from matching.api import UserAPI
from matching.dependencies.auth import login_required
from matching.models import User
from matching.schemas import (
    CreateUserSchema,
    ReadUserSchema,
    UpdateUserSchema,
    VerifyCodeSchema,
)

from fastapi import APIRouter, Depends, Request

user_router = APIRouter()


@user_router.get(
    "/", response_model=ReadUserSchema, dependencies=[Depends(login_required)]
)
async def get(request: Request) -> Optional[User]:
    return UserAPI.get(request)


@user_router.post(
    "/",
    response_model=ReadUserSchema,
)
async def create(request: Request, schema: CreateUserSchema) -> User:
    return UserAPI.create(request, schema)


@user_router.put(
    "/",
    response_model=ReadUserSchema,
    dependencies=[Depends(login_required)],
)
async def update(request: Request, schema: UpdateUserSchema) -> User:
    return UserAPI.update(request, schema)


@user_router.delete("/", dependencies=[Depends(login_required)])
async def delete(request: Request) -> None:
    return UserAPI.delete(request)


@user_router.post(
    "/verify-code",
    response_model=ReadUserSchema,
)
async def verify_code(request: Request, schema: VerifyCodeSchema):
    return UserAPI.verify_code(request, schema)
