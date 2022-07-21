import os
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from src.api.v1.schemas.tokens import TokenData
from src.api.v1.schemas.users import UserFullOut
from src.services.user import UserService, get_user_service


class Auth:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_MINUTES = float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

    incorrect_credentials_401_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect login credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
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
            user: dict = user_service.get_user(username).dict()
        if not user:
            raise self.incorrect_credentials_401_exception
        if not self.verify_password(password, user["hashed_password"]):
            raise self.incorrect_credentials_401_exception

        return UserFullOut(**user)

    def get_password_hash(self, password):
        return self.hasher.hash(password)

    def encode_token(self, data: dict, scope: str = "access_token",
                     expire_time: float = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        data_to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expire_time)
        data_to_encode.update({"exp": expire, 'scope': scope, })
        encoded_jwt = jwt.encode(data_to_encode, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token, scope: str = "access_token") -> TokenData:
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self.credentials_exception

            if payload['scope'] == scope:
                token_data = TokenData(username=username)
                return token_data
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')

        except JWTError:
            raise self.credentials_exception

    def encode_refresh_token(self, data: dict) -> str:
        encoded_jwt = self.encode_token(data, scope='refresh_token',
                                        expire_time=self.REFRESH_TOKEN_EXPIRE_MINUTES, )
        return encoded_jwt

    def refresh_tokens(self, refresh_token):
        token_data = self.decode_token(refresh_token, scope="refresh_token")
        data_to_encode = {"sub": token_data.username}
        new_access_token = self.encode_token(data_to_encode)
        new_refresh_token = self.encode_token(data_to_encode, scope='refresh_token',
                                              expire_time=self.REFRESH_TOKEN_EXPIRE_MINUTES, )
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    def create_access_token_user(self, user_model: BaseModel):
        data_to_encode = {"sub": user_model.username}
        return self.encode_token(data_to_encode)

    def create_refresh_token_user(self, user_model: BaseModel):
        data_to_encode = {"sub": user_model.username}
        return self.encode_refresh_token(data_to_encode)
