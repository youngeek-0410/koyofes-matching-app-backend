from config.auth import AuthenticatedUser, UnauthenticatedUser
from config.jwt import decode_jwt_token
from jose import jwt
from matching.models import User
from starlette.middleware.authentication import AuthCredentials, AuthenticationBackend

from fastapi import HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param


class BackendAuth(AuthenticationBackend):
    async def authenticate(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, access_token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            return (
                AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )

        try:
            claims = decode_jwt_token(access_token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception:
            return (
                AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )

        user = User.objects.filter(uuid=claims["user_uuid"]).first()
        if not user or not user.is_active:
            return (
                AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )

        if user.is_admin:
            return (
                AuthCredentials(["admin", "authenticated"]),
                AuthenticatedUser(user),
            )
        else:
            return AuthCredentials(["authenticated"]), AuthenticatedUser(user)
