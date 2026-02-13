from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBaseSchema(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=15)
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password_confirm: str = Field(..., max_length=100)

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not password_confirm == validation.data.get("password"):
            raise ValueError({"password":"password and password confirm are not equal!"},)
        return password_confirm


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    is_verify: bool | None = None


class UserResponseSchema(UserBaseSchema):
    id: int
    is_verify: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserLoginSchema(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)