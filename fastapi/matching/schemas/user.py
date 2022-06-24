from matching.models import User
from pydantic import BaseModel, Field


class BaseUserSchema(BaseModel):
    username: str = Field(
        ..., min_length=User.MIN_LENGTH_USERNAME, max_length=User.MAX_LENGTH_USERNAME
    )
    email: str = Field(..., regex=r"[^\s]+@[^\s]+")

    class Config:
        orm_mode = True


class ReadUserSchema(BaseUserSchema):
    is_verified: bool


class CreateUserSchema(BaseUserSchema):
    pass


class UpdateUserSchema(BaseUserSchema):
    pass


class VerifyCodeSchema(BaseModel):
    email: str = Field(..., regex=r"[^\s]+@[^\s]+")
    code: str = Field(...)
