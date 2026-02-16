from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from schemas import UserResponse
from models import User

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get(
    "",
    response_model=UserResponse,
    summary="Get current User",
    description="Get current User"
)
async def get_current_user(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user


@router.get(
    "/get-users",
    response_model=List[UserResponse],
    summary="Get all Users",
    description="Get all Users"
)
async def get_all_users(
        isActive: Optional[bool] = Query(None),
        db: Session = Depends(get_db)
    ) -> List[UserResponse]:

    users = db.query(User)
    if isActive is not None:
        users = db.query(User).filter(User.is_active == isActive)
        return users
    else:
        return users