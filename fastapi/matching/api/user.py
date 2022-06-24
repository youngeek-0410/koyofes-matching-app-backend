from typing import Optional

from config.twilio import check_verification_code, send_verification_code
from matching.models import User
from matching.schemas import CreateUserSchema, UpdateUserSchema, VerifyCodeSchema

from fastapi import HTTPException, Request


# TODO: 非同期処理がtwilioのAPIを叩いているときにロックされていないか確認する
class UserAPI:
    @classmethod
    def get(cls, request: Request) -> Optional[User]:
        return User.objects.filter(uuid=request.user.uuid).first()

    @classmethod
    def create(cls, request: Request, schema: CreateUserSchema) -> User:
        user = User.objects.filter(email=schema.email).first()
        if user and user.is_verified:
            raise HTTPException(
                status_code=400, detail="User with that email has already exists."
            )
        elif user and not user.is_verified:
            # await asyncio.get_event_loop().run_in_executor(
            #     None, send_verification_code, user.email
            # )
            send_verification_code(user.email)
        else:
            user = User.objects.create(**schema.dict())
            # await asyncio.get_event_loop().run_in_executor(
            #     None, send_verification_code, user.email
            # )
            send_verification_code(user.email)
        return user

    @classmethod
    def update(cls, request: Request, schema: UpdateUserSchema) -> User:
        user, _ = User.objects.update_or_create(
            uuid=request.user.uuid, defaults=schema.dict()
        )
        return user

    @classmethod
    def delete(cls, request: Request) -> None:
        user = User.objects.filter(uuid=request.user.uuid).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=400, detail="User with that uuid not found."
            )
        user.is_active = False
        user.save()
        return

    @classmethod
    def verify_code(cls, request: Request, schema: VerifyCodeSchema) -> User:
        try:
            is_verified = check_verification_code(schema.email, schema.code)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=str(e)
            )  # TODO: セキュリティ的にエラーをレスポンスしない
        if not is_verified:
            raise HTTPException(status_code=400, detail="Code was incorrect.")

        user = User.objects.filter(email=schema.email).first()
        assert user
        user.is_verified = True
        user.save()
        return user
