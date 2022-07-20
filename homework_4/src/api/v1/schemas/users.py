from datetime import datetime

from pydantic import BaseModel, constr, EmailStr, UUID4

__all__ = (
    "UserModel",
    "UserCreate",
)


class UserBase(BaseModel):
    username: constr(min_length=5, max_length=40)
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=3, max_length=40)


class UserFullOut(UserBase):
    uuid: UUID4
    created_at: datetime
    is_totp_enabled: bool
    is_superuser: bool
    is_active: bool


class UserModel(UserFullOut):
    hashed_password: str
