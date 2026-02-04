# auth_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import authenticate_user
from app.schemas.auth import LoginRequest, TokenResponse
from app.db.engine import async_db_session_dependency

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    db:async_db_session_dependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 requires `username`, but we treat it as email.
    """
    token = await authenticate_user(
        db,
        LoginRequest(
            email=form_data.username,   # 👈 email comes from username
            password=form_data.password,
        ),
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
