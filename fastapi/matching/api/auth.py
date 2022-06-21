from typing import Dict

from config.jwt import create_claims, encode_claims_to_jwt_token, response_jwt_token
from config.password import verify_password
from matching.models import User
from matching.schemas.auth import LoginSchema

from fastapi import HTTPException, Request


class AuthAPI:
    @classmethod
    def login(cls, request: Request, schema: LoginSchema) -> Dict[str, str]:
        credentials = {"email": schema.email, "password": schema.password}

        if all(credentials.values()):
            user = cls().__authenticate_user(**credentials)
            claims = create_claims(user)
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return response_jwt_token(encode_claims_to_jwt_token(claims))

    def __authenticate_user(self, email: str, password: str) -> User:
        user = User.objects.filter(email=email).first()

        if not user:
            raise HTTPException(
                status_code=400, detail="Invalid email or password"
            )  # 「no such user with this email」とはセキュリティ観点から出さない
        if not verify_password(password, user.password) or not user.is_active:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return user
