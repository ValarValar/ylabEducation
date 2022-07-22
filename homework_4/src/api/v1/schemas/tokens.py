from datetime import datetime
from typing import Union
from pydantic import BaseModel, UUID4

from src.api.v1.schemas.users import UserFullOut


class Token(BaseModel):
    token: str


class TokenData(UserFullOut):
    jti: Union[UUID4, str]
    exp: datetime
    type: str
