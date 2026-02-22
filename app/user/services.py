# app/user/services.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.database import get_session
from app.user.models import User
from app.user.schemas import SignupSchema, ProfileSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=1440)  # 24 hours
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


async def register_user(data: SignupSchema, session: AsyncSession) -> User:
    """Register new user - business logic"""
    # Check if email or username already exists
    existing = await session.exec(
        select(User).where(
            (User.email == data.email) | (User.username == data.username)
        )
    ).first()

    if existing:
        raise ValueError("Email or username already registered")

    # Create user with hashed password
    hashed_pw = User.hash_password(data.password)

    user = User(
        email=data.email,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=hashed_pw,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(identifier: str, password: str, session: AsyncSession) -> User | None:
    """Verify credentials and return user if valid"""
    user = await session.exec(
        select(User).where(
            (User.email == identifier) | (User.username == identifier)
        )
    ).first()

    if not user:
        return None

    if not user.verify_password(password):
        return None

    return user


async def get_user_profile(user_id: str, session: AsyncSession) -> ProfileSchema:
    """Get profile data including follower/following counts"""
    user = await session.get(User, user_id)

    if not user:
        raise ValueError("User not found")

    # Placeholder for follower/following counts
    # TODO: Implement when Follow microservice is ready
    followers_count = 0
    following_count = 0

    profile = ProfileSchema.model_validate(user)
    profile.followers_count = followers_count
    profile.following_count = following_count

    return profile


# Dependency to get current authenticated user
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user