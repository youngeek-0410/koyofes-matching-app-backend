from typing import Optional

from matching.api import UserAPI
from matching.models import User
from matching.schemas import CreateUserSchema, ReadUserSchema, UpdateUserSchema

from fastapi import APIRouter, Request

user_router = APIRouter()


@user_router.get("/", response_model=ReadUserSchema)
async def get(request: Request) -> Optional[User]:
    return UserAPI.get(request)


@user_router.post("/", response_model=ReadUserSchema)
async def create(request: Request, schema: CreateUserSchema) -> User:
    return UserAPI.create(request, schema)


@user_router.put("/", response_model=ReadUserSchema)
async def update(request: Request, schema: UpdateUserSchema) -> User:
    return UserAPI.update(request, schema)


@user_router.delete("/")
async def delete(request: Request) -> None:
    return UserAPI.delete(request)
