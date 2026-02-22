# app/user/api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.user.schemas import (
    SignupSchema, LoginSchema, TokenSchema, ProfileSchema, UserReadSchema
)
from app.user.services import (
    register_user,
    authenticate_user,
    get_user_profile,
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def signup(
        user_in: SignupSchema,
        session: AsyncSession = Depends(get_session)
):
    """
    Register a new user
    """
    try:
        new_user = await register_user(user_in, session)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenSchema)
async def login(
        credentials: LoginSchema,
        session: AsyncSession = Depends(get_session)
):
    """
    Authenticate user and return JWT access token
    """
    user = await authenticate_user(credentials.identifier, credentials.password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=ProfileSchema)
async def get_current_user_profile(
        current_user=Depends(get_current_user),  # we'll define this dependency next
        session: AsyncSession = Depends(get_session)
):
    """
    Get current authenticated user's profile with follower/following counts
    """
    profile = await get_user_profile(current_user.id, session)
    return profile