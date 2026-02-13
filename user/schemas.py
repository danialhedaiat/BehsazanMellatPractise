from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    phone_number: str = Field(..., max_length=15)
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    pass
    password_confirm: str = Field(..., max_length=100)



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
