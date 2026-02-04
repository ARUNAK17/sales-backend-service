from fastapi import APIRouter, Depends
from typing import Annotated

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role
from app.models.enums import Userrole
from app.services import audit_service

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])

DBSession = async_db_session_dependency


@router.get(
    "",
    dependencies=[Depends(require_role(Userrole.CEO))],
)
async def list_audit_logs(
    db: DBSession,
):
    return await audit_service.list_audit_logs(db)
