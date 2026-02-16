from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import auth_router, user_router

import time

# ========================================
# API Metadata for Documentation
# ========================================

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations for user authentication: register, login, logout, refresh tokens.",
    },
    {
        "name": "Users",
        "description": "Operations with users: get profile, update profile, change password.",
    },
    {
        "name": "Admin",
        "description": "Admin-only operations: manage users, view all users, change roles.",
    },
    {
        "name": "Health",
        "description": "Health check endpoints for monitoring.",
    },
]

app = FastAPI(
    title="Python Auth Backend API",
    description="""
    ## 🚀 Secure Authentication & Authorization API

    This API provides a complete authentication system with:

    * **User Registration** - Sign up with email and password
    * **User Login** - Authenticate and receive JWT tokens
    * **Token Refresh** - Get new access tokens without re-logging in
    * **Role-Based Access Control (RBAC)** - Admin, User, Moderator roles
    * **Password Management** - Change passwords securely
    * **Social Login Ready** - Prepared for Google, Facebook, GitHub integration

    ### 🔐 Security Features

    * Passwords hashed with bcrypt
    * JWT tokens with expiration
    * Refresh token rotation
    * CORS protection
    * SQL injection prevention (SQLAlchemy ORM)

    ### 📚 How to Use

    1. **Register** a new user at `/auth/register`
    2. **Login** at `/auth/login` to get tokens
    3. **Use the access_token** in the `Authorization` header: `Bearer <your_token>`
    4. **Refresh** your token at `/auth/refresh` when it expires

    ### 🧪 Try It Out

    Use the "Try it out" button on each endpoint to test the API directly from this page!
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative UI
    contact={
        "name": "Nithin Titus",
        "email": "nithin.titus@outlook.com",
    },
    license_info={
        "name": "MIT",
    },
)

# ========================================
# CORS Middleware - Allow React to call API
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Your React app URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router.router)
app.include_router(user_router.router)

# ========================================
# Health Check Endpoint
# ========================================
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check endpoint",
    response_description="Application Up and Running...."
)
async def health():
    return {"status": "ok"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (development only)
    )