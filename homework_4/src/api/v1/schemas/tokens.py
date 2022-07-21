from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: Union[str, None] = None
