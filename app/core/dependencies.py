
#dependencies.py
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from app.models.user import User
from app.core.security import decode_access_token
from app.db.engine import async_db_session_dependency
from app.models.enums import Userrole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    db: async_db_session_dependency,
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def require_role(required_role: Userrole):
    async def role_checker(
        current_user = Depends(get_current_user),
    ):
        if current_user.userrole != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker

def require_roles(*roles: Userrole):
    async def role_checker(
        current_user = Depends(get_current_user),
    ):
        if current_user.userrole not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker