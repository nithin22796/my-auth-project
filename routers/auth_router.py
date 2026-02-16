from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from auth import hash_password, create_access_token, create_refresh_token, verify_password, authenticate_user, \
    verify_token, get_current_user
from database import get_db
from models import User, AuthProvider
from schemas import Token, UserCreate, UserLogin, TokenRefresh, UserResponse, MessageResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Register Endpoints
@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user"
)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> Dict[str, str]:
    existing_user_email = db.query(User).filter(User.email == user_data.email).first()

    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use."
        )

    existing_user_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in use."
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        auth_provider=AuthProvider.LOCAL,
        is_active=True,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        data={
            "user_id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
        }
    )

    refresh_token = create_refresh_token(
        data = {
            "user_id": new_user.id,
            "email": new_user.email
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Login user"
)
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)) -> Dict[str, str]:
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is disabled. Please contact support",
        )

    access_token = create_access_token(
        data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
    )

    refresh_token = create_refresh_token(
        data = {
            "user_id": user.id,
            "email": user.email,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh token",
    description="Refresh token"
)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)) -> Dict[str, str]:
    try:
        payload = verify_token(token_data.refresh_token, token_type="refresh")
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    new_access_token = create_access_token(
        data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
    )

    new_refresh_token = create_refresh_token(
        data = {
            "user_id": user.id,
            "email": user.email,
        }
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Logout user"
)
async def logout_user(current_user: User = Depends(get_current_user)):
    return {
        "message": "You have been logged out",
    }