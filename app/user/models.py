# app/user/models.py
from typing import Optional
from datetime import datetime, timezone
from uuid import uuid4
from sqlmodel import Field, SQLModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_utc_now():
    """Get current UTC time"""
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    bio: Optional[str] = Field(default=None, max_length=500)
    website: Optional[str] = Field(default=None, max_length=255)

    # Hashed password – NEVER store plain text
    hashed_password: str = Field(nullable=False)

    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain password against the stored hash"""
        return pwd_context.verify(plain_password, self.hashed_password)

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        """Hash a password for storage"""
        return pwd_context.hash(plain_password)