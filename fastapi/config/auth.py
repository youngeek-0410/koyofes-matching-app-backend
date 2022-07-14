from typing import Optional

from matching.models import User
from starlette import authentication

from fastapi import HTTPException, Request, security


class OAuth2PasswordBearer(security.OAuth2PasswordBearer):
    """OAuth2PasswordBearerのラッパー."""

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = security.utils.get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code=400, detail="Invalid token")
            else:
                return None
        return param


class AuthenticatedUser(authentication.SimpleUser):
    def __init__(self, user: User) -> None:
        self.username = user.username
        self.uuid = user.uuid
        self.email = user.email

        self.user = user  # FIXME


class UnauthenticatedUser(authentication.UnauthenticatedUser):
    pass
