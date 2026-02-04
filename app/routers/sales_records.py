from fastapi import APIRouter, Depends
from typing import Annotated

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role,require_roles
from app.models.enums import Userrole
from app.services import sales_record_service

router = APIRouter(prefix="/sales-records", tags=["sales-records"])

DBSession = async_db_session_dependency


@router.get(
    "",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def list_sales_records(
    db: DBSession,
):
    return await sales_record_service.list_sales_records(db)
