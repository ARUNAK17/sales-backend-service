#auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import cast
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.core.security import verify_password, create_access_token


async def authenticate_user(
    db: AsyncSession,
    data: LoginRequest,
) -> str | None:
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(
    data.password,
    cast(str, user.hashed_password),):
        return None

    access_token = create_access_token(
        subject=str(user.id),
        role=user.userrole.value,
    )

    return access_token
