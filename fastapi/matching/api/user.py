from typing import Optional

from matching.models import User
from matching.schemas import CreateUserSchema, UpdateUserSchema

from fastapi import Request


class UserAPI:
    @classmethod
    def get(cls, request: Request) -> Optional[User]:
        return User.objects.filter(username="username").first()

    @classmethod
    def create(cls, request: Request, schema: CreateUserSchema) -> User:
        return User.objects.create(**schema.dict())

    @classmethod
    def update(cls, request: Request, schema: UpdateUserSchema) -> User:
        user = User.objects.filter(username="username").first()
        assert user is not None
        user.update(**schema.dict())
        return user

    @classmethod
    def delete(cls, request: Request) -> None:
        User.objects.filter(username="username").delete()
        return
