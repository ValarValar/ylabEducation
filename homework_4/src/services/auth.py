from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from src.api.v1.schemas.users import UserFullOut
from src.services.token import get_token_service
from src.services.user import UserService, get_user_service


class Auth:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()
    token_service = get_token_service()

    incorrect_credentials_401_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect login credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def verify_password(self, plain_password, hashed_password):
        return self.hasher.verify(plain_password, hashed_password)

    def authenticate_user(
            self, username: str, password: str,
            user_service: UserService = Depends(get_user_service)
    ):
        user = user_service.get_user(username)
        if user:
            user = user.dict()
        else:
            raise self.incorrect_credentials_401_exception
        if not self.verify_password(password, user["hashed_password"]):
            raise self.incorrect_credentials_401_exception

        return UserFullOut(**user)

    def get_password_hash(self, password):
        return self.hasher.hash(password)

    def create_access_token_user(self, user_model: UserFullOut, ):
        return self.token_service.encode_token(user_model)

    def create_refresh_token_user(self, user_model: UserFullOut, ):
        return self.token_service.encode_refresh_token(user_model)


# get_post_service — это провайдер PostService. Синглтон
@lru_cache()
def get_auth_class() -> Auth:
    return Auth()
