from fastapi import APIRouter, Depends
from typing import Annotated

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role,require_roles
from app.models.enums import Userrole
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])

DBSession = async_db_session_dependency


@router.get(
    "/top-products",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def top_products(
    db: DBSession,
):
    return await analytics_service.get_top_products(db)


@router.get(
    "/lowest-products",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def lowest_products(
    db: DBSession,
):
    return await analytics_service.get_lowest_products(db)


@router.get(
    "/product-rank-quarter",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def product_rank_per_quarter(
    db: DBSession,
):
    return await analytics_service.get_product_rank_per_quarter(db)


@router.get(
    "/cumulative-sales",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def cumulative_sales(
    db: DBSession,
):
    return await analytics_service.get_cumulative_sales(db)
