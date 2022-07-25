import uuid
from datetime import datetime, timedelta
from functools import lru_cache

import redis
from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.api.v1.schemas.tokens import TokenData, AccessTokenData, RefreshTokenData
from src.api.v1.schemas.users import UserFullOut
from src.core import config


class TokenService:
    JWT_SECRET_KEY = config.JWT_SECRET_KEY
    ALGORITHM = config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = config.REFRESH_TOKEN_EXPIRE_MINUTES

    _next_uuid = str(uuid.uuid4())

    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Can't validate token info",
        headers={"WWW-Authenticate": "Bearer"},
    )

    _blocked_access_tokens = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=1, decode_responses=True,
    )

    _active_refresh_tokens = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=2, decode_responses=True,
    )

    def put_access_token_in_blocked_db(self, token: str):
        token_data = self.decode_token(token)
        token_uuid = str(token_data.jti)
        self._blocked_access_tokens.set(name=token_uuid, value=token_uuid, )

    def put_refresh_token_in_active_db(self, token_jti: str, user_uuid):
        self._active_refresh_tokens.rpush(str(user_uuid), token_jti)

    def delete_refresh_token_in_active_db(self, access_token: str, all_tokens: bool = False):
        token_data = self.decode_token(access_token, "access_token")
        refresh_token_jti = str(token_data.refresh_uuid)
        user_uuid = str(token_data.uuid)
        if all_tokens:
            self._active_refresh_tokens.delete(user_uuid)
        else:
            self._active_refresh_tokens.lrem(user_uuid, 0, refresh_token_jti)

    def generate_uuid(self) -> str:
        res_value = self._next_uuid
        self._next_uuid = str(uuid.uuid4())
        return str(res_value)

    def check_uuid_in_db(self) -> bool:
        pass

    def encode_token(self, user_model: UserFullOut, type: str = "access_token",
                     expire_time: float = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        user_uuid = user_model.uuid
        data_to_encode = user_model.for_encoding_to_dict()
        expire = datetime.utcnow() + timedelta(minutes=expire_time)
        token_jti = self.generate_uuid()
        data_to_encode.update({"exp": expire, 'type': type, 'jti': token_jti})
        if type == "access_token":
            data_to_encode.update({"refresh_uuid": self._next_uuid})
        if type == "refresh_token":
            self.put_refresh_token_in_active_db(token_jti, user_uuid)

        encoded_jwt = jwt.encode(data_to_encode, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token, type: str = "access_token") -> TokenData:
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("username") is None:
                raise self.token_exception
            if payload['type'] == type:
                token_data = ""
                if type == "access_token":
                    token_data = AccessTokenData(**payload)
                else:
                    token_data = RefreshTokenData(**payload)
                return token_data
            raise HTTPException(status_code=401, detail='type for the token is invalid')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')

        except JWTError:
            raise self.token_exception

    def encode_refresh_token(self, user_model: UserFullOut) -> str:
        encoded_jwt = self.encode_token(user_model, type='refresh_token',
                                        expire_time=self.REFRESH_TOKEN_EXPIRE_MINUTES, )
        return encoded_jwt

    def refresh_tokens(self, refresh_token):
        token_data = self.decode_token(refresh_token, type="refresh_token")

        user_data_model_to_encode = UserFullOut(**token_data.dict())

        new_access_token = self.encode_token(user_data_model_to_encode)
        new_refresh_token = self.encode_token(user_data_model_to_encode, type='refresh_token',
                                              expire_time=self.REFRESH_TOKEN_EXPIRE_MINUTES, )
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
