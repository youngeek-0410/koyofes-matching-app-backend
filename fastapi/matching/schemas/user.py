from typing import Optional

from matching.models import User
from pydantic import BaseModel, Field

from ..models import Department, Sex


class RequiredUserInfoSchema(BaseModel):
    username: str = Field(
        ..., min_length=User.MIN_LENGTH_USERNAME, max_length=User.MAX_LENGTH_USERNAME
    )
    email: str = Field(..., regex=r"[^\s]+@[^\s]+", max_length=User.MAX_LENGTH_EMAIL)

    class Config:
        orm_mode = True


class OptionalUserInfoSchema(BaseModel):
    department: Optional[Department]
    sex: Optional[Sex]
    grade: Optional[int] = Field(None, ge=1, le=5)
    description: Optional[str] = Field(None, max_length=User.MAX_LENGTH_DESCRIPTION)

    class Config:
        orm_mode = True
        use_enum_values = True


class ReadUserSchema(RequiredUserInfoSchema, OptionalUserInfoSchema):
    is_verified: bool


class CreateUserSchema(RequiredUserInfoSchema):
    pass


class UpdateUserSchema(OptionalUserInfoSchema):
    pass


class VerifyCodeSchema(BaseModel):
    email: str = Field(..., regex=r"[^\s]+@[^\s]+", max_length=User.MAX_LENGTH_EMAIL)
    code: str = Field(...)
