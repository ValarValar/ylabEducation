from datetime import datetime
from typing import Union

from pydantic import BaseModel, constr, EmailStr

__all__ = (
    "UserModel",
    "UserCreate",
)


class UserBase(BaseModel):
    username: constr(min_length=5, max_length=40)
    email: EmailStr
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserCreate(UserBase):
    password: str


class UserModel(UserBase):
    hashed_password: str
    id: Union[int, None] = None
    created_at: Union[datetime, None] = None
