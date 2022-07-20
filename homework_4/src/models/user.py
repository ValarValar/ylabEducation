import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel

__all__ = ("User",)

class UUIDModel(SQLModel):
   uuid: uuid_pkg.UUID = Field(
       default_factory=uuid_pkg.uuid4,
       primary_key=True,
       index=True,
       nullable=False,
       sa_column_kwargs={
           "server_default": text("gen_random_uuid()"),
           "unique": True
       }
   )

class User(UUIDModel, table=True):
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)

    is_active: bool = Field(nullable=False, default=True)
    is_totp_enabled: bool = Field(nullable=False, default=False)
    is_superuser: bool = Field(nullable=False, default=False)

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)