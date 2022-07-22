import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from jose import jwt, JWTError

from src.api.v1.schemas.tokens import TokenData
from src.api.v1.schemas.users import UserFullOut
from src.core import config


class TokenService:
    JWT_SECRET_KEY = config.JWT_SECRET_KEY
    ALGORITHM = config.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = config.REFRESH_TOKEN_EXPIRE_MINUTES

    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Can't validate token info",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def generate_uuid(self) -> str:
        new_uuid = uuid.uuid4()
        while self.check_uuid_in_db():
            new_uuid = uuid.uuid4()
        return str(new_uuid)

    def check_uuid_in_db(self) -> bool:
        return False

    def encode_token(self, user_model: UserFullOut, type: str = "access_token",
                     expire_time: float = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
        data_to_encode = user_model.for_encoding_to_dict()
        expire = datetime.utcnow() + timedelta(minutes=expire_time)
        data_to_encode.update({"exp": expire, 'type': type, 'jti': self.generate_uuid()})

        encoded_jwt = jwt.encode(data_to_encode, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token, type: str = "access_token") -> TokenData:
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("username") is None:
                raise self.token_exception
            if payload['type'] == type:
                token_data = TokenData(**payload)
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
