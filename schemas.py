from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from models import UserRole, AuthProvider

# =================================
# REQUEST SCHEMAS
# =================================
class UserCreate(BaseModel):
    """
    Schema for user registration.

    Eg:
    {
        "email": "abc@example.com",
        "username": "username",
        "password": "SecurePAss",
    }
    """

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "abc@example.com",
                "username": "username",
                "password": "SecurePAss",
            }
        }
    )

class UserLogin(BaseModel):
    """
    Schema for user Login
    """

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "abc@example.com",
                "username": "username",
                "password": "SecurePAss",
            }
        }
    )


class TokenRefresh(BaseModel):
    """
    Schema for refreshing access token.

    Example request body:
    {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    """
    refresh_token: str

class PasswordChange(BaseModel):
    """
    Schema for password change.
    """

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

# =================================
# RESPONSE SCHEMAS
# =================================
class UserResponse(BaseModel):
    """
    Schema for user data in API Response

    Example response:
    {
        "id": 1,
        "email": "john@example.com",
        "username": "johndoe",
        "is_active": true,
        "is_verified": false,
        "role": "user",
        "auth_provider": "local",
        "profile_picture": null,
        "created_at": "2024-02-11T10:30:00Z"
    }
    """
    id: int
    email: str
    username: str
    is_active: bool
    is_verified: bool
    role: UserRole
    auth_provider: AuthProvider
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """
        Schema for JWT token response after login/registration.

        Example response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }

        Your React app will:
        1. Store these tokens (localStorage or memory)
        2. Send access_token in Authorization header: "Bearer <access_token>"
        3. Use refresh_token to get new access_token when it expires
        """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for data extracted FROM a JWT token.
    This is what we decode from the token to identify the user.

    Internal use only - not sent to client.
    """
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class MessageResponse(BaseModel):
    """
    Generic message response for operations like logout, password reset, etc.

    Example response:
    {
        "message": "Password changed successfully"
    }
    """
    message: str
