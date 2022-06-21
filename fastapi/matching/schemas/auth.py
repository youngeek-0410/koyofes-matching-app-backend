from pydantic import BaseModel

from fastapi import Form


class LoginSchema:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
    ):
        self.email = username
        self.password = password


class Token(BaseModel):
    access_token: str
    token_type: str
