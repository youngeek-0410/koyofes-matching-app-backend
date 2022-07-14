from logging import getLogger
from typing import Optional

from config.twilio import check_verification_code, send_verification_code
from django.core.files.base import ContentFile
from matching.models import User, UserImage
from matching.schemas import CreateUserSchema, UpdateUserSchema, VerifyCodeSchema

from fastapi import HTTPException, Request, UploadFile

logger = getLogger(__name__)


# TODO: 非同期処理がtwilioのAPIを叩いているときにロックされていないか確認する
class UserAPI:
    @classmethod
    def get(cls, request: Request) -> Optional[User]:
        user = User.objects.filter(uuid=request.user.uuid).first()
        assert user
        return user

    @classmethod
    def create(cls, request: Request, schema: CreateUserSchema) -> User:
        user = User.objects.filter(email=schema.email).first()
        if user and user.is_verified:
            raise HTTPException(
                status_code=400,
                detail=f"User with that email({schema.email}) already exists.",
            )
        elif user and not user.is_verified:
            # await asyncio.get_event_loop().run_in_executor(
            #     None, send_verification_code, user.email
            # )
            send_verification_code(user.email)
        else:
            _, domain = schema.email.split("@")
            if domain != "toyota.kosen-ac.jp":
                raise HTTPException(
                    status_code=400,
                    detail=f"Email must be a valid email address (@toyota.kosen-ac.jp).",
                )
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
        assert user
        user.is_active = False
        user.save()
        return

    @classmethod
    def verify_code(cls, request: Request, schema: VerifyCodeSchema) -> User:
        try:
            is_verified = check_verification_code(schema.email, schema.code)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Error: code was expired (10minutes) or approved.",
            )
        if not is_verified:
            raise HTTPException(
                status_code=400, detail="Verification code was incorrect."
            )

        user = User.objects.filter(email=schema.email).first()
        assert user
        user.is_verified = True
        user.save()
        return user

    @classmethod
    def upload_image(cls, request: Request, image: UploadFile) -> UserImage:
        user = User.objects.filter(uuid=request.user.uuid).first()
        assert user
        content = image.file.read()
        return UserImage.objects.create(
            user=user, image=ContentFile(content, image.filename)
        )
