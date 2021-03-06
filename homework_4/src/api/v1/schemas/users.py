from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, UUID4, constr
from sqlmodel import SQLModel

from src.api.v1.schemas.auth import UsernameBase, PasswordBase

__all__ = (
    "UserModel",
    "UserCreate",
    "UserFullOut",
    "UserModel"
)


class UserBase(UsernameBase, BaseModel):
    email: EmailStr


class UserCreate(PasswordBase, UserBase):
    pass


class UserFullOut(UserBase):
    uuid: Union[UUID4, str]
    created_at: Union[datetime, str]
    is_totp_enabled: bool
    is_superuser: bool
    is_active: bool

    def for_encoding_to_dict(self):
        data = self.dict()
        data["uuid"] = str(self.uuid)
        data["created_at"] = str(self.created_at)

        return data

    class Config:
        orm_mode = True


class UserModel(UserFullOut):
    hashed_password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=5, max_length=40)] = None

    class Config:
        orm_mode = True
