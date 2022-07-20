from functools import lru_cache
from typing import Optional

from fastapi import Depends
from passlib.context import CryptContext
from sqlmodel import Session

from src.api.v1.schemas.users import UserCreate
from src.db import AbstractCache, get_cache, get_session
from src.models.user import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class UserService(ServiceMixin):

    def check_username_is_used(self, item_username: str) -> bool:
        user = self.session.query(User).filter(User.username == item_username).first()
        if user:
            return True
        else:
            return False

    def get_user(self, item_username: str) -> Optional[dict]:

        user = self.session.query(User).filter(User.username == item_username).first()
        return user.dict() if user else None

    def create_user(self, user: UserCreate) -> dict:
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()


@lru_cache()
def get_user_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
