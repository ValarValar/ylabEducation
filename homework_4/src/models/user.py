import uuid as uuid_pkg
from datetime import datetime

from sqlmodel import Field, SQLModel

__all__ = ("User",)


class UUIDModelBase(SQLModel):
    """
    Base class for UUID-based models.
    """
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class User(UUIDModelBase, table=True):
    __tablename__ = "users"

    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)

    is_active: bool = Field(nullable=False, default=True)
    is_totp_enabled: bool = Field(nullable=False, default=False)
    is_superuser: bool = Field(nullable=False, default=False)

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)