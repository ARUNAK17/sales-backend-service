from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role
from app.models.enums import Userrole
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

DBSession = async_db_session_dependency


@router.post(
    "",
    dependencies=[Depends(require_role(Userrole.CEO))],
)
async def create_user(
    db: DBSession,
    username: str,
    email: str,
    hashed_password: str,
    role: Userrole,
):
    return await user_service.create_user(
        db,
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )


@router.put(
    "/{user_id}",
    dependencies=[Depends(require_role(Userrole.CEO))],
)
async def update_user(
    user_id: int,
    db: DBSession,
    username: str | None = None,
    email: str | None = None,
    role: Userrole | None = None,
    is_active: bool | None = None,
):
    user = await user_service.update_user(
        db,
        user_id=user_id,
        username=username,
        email=email,
        role=role,
        is_active=is_active,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get(
    "",
    dependencies=[Depends(require_role(Userrole.CEO))],
)
async def list_users(
    db: DBSession,
):
    return await user_service.list_users(db)
