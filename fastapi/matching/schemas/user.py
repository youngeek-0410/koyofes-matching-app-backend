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
    pass


class CreateUserSchema(BaseUserSchema):
    pass


class UpdateUserSchema(BaseUserSchema):
    pass
