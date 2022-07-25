from functools import lru_cache
from typing import Union

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.users import UserCreate, UserUpdate, UserFullOut
from src.db import AbstractCache, get_cache, get_session
from src.models.user import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):

    def check_username_is_used(self, item_username: str) -> bool:
        user = self.session.query(User).filter(User.username == item_username).first()
        if user:
            return True
        else:
            return False

    def get_user(self, item_username: str) -> Union[User, None]:
        user = self.session.query(User).filter(User.username == item_username).first()
        return user if user else None

    def get_user_info_by_username_to_encode(self, username: str, ) -> Union[UserFullOut, None]:
        user = self.get_user(username)
        if user:
            user_full_out = UserFullOut(**user.dict())
            return user_full_out
        return None

    #def get_user_by_token

    def create_user(self, user: UserCreate) -> User:
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def update_user(self, update_user: UserUpdate, current_username: str) -> Union[User, None]:
        update_data = update_user.dict(exclude_unset=True)
        current_user = self.get_user(current_username)
        if current_user:
            for key, value in update_data.items():
                setattr(current_user, key, value)
            self.session.commit()
            self.session.refresh(current_user)
        return current_user


@lru_cache()
def get_user_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
