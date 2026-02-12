from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    """
    User roles for Role-Based Access Control (RBAC)
    """
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class AuthProvider(str, enum.Enum):
    """
    Authentication providers
    """
    LOCAL = "local"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"

class User(Base):
    """
    User model for authentication and authorization.
    Supports both local (email/password) and social login.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=True)
    auth_provider = Column(SQLEnum(AuthProvider), default=AuthProvider.LOCAL)
    provider_user_id = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User {self.username} ({self.email}) - {self.auth_provider}>"