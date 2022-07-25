from functools import lru_cache
from typing import Union
from uuid import UUID
from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.users import UserCreate, UserUpdate, UserFullOut
from src.db import AbstractCache, get_cache, get_session
from src.models.user import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")

from src.services.token import get_token_service, TokenService


class UserService(ServiceMixin):

    _token_service = get_token_service()

    def check_username_is_used(self, item_username: str) -> bool:
        user = self.session.query(User).filter(User.username == item_username).first()
        if user:
            return True
        else:
            return False

    def get_user_by_username(self, item_username: str) -> Union[User, None]:
        user = self.session.query(User).filter(User.username == item_username).first()
        return user if user else None

    def get_user_by_uuid(self, uuid) -> Union[User, None]:
        user = self.session.query(User).get(uuid)
        return user


    def get_user_info_by_username_to_encode(self, username: str, ) -> Union[UserFullOut, None]:
        user = self.get_user_by_username(username)
        if user:
            user_full_out = UserFullOut(**user.dict())
            return user_full_out
        return None

    def get_user_by_token(self, token: str) -> Union[User, None]:
        token_data = self._token_service.decode_token(token)
        user = self.get_user_by_uuid(token_data.uuid)
        return user

    def get_current_active_user(self, token: str) -> Union[dict, None]:
        current_user = self.get_user_by_token(token).dict()
        if not current_user.get("is_active"):
            return None
        return current_user

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

    def update_user(self, update_user: UserUpdate, token: str) -> Union[User, None]:
        if self.check_username_is_used(update_user.username):
            return None
        update_data = update_user.dict(exclude_unset=True)
        current_user = self.get_user_by_token(token)
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
