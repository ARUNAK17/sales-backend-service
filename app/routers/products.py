from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role,require_roles
from app.models.enums import Userrole
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])

DBSession = async_db_session_dependency


@router.post(
    "",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def create_product(
    db: DBSession,
    name: str,
    price: float,
    description: str | None = None,
):
    return await product_service.create_product(
        db,
        name=name,
        price=price,
        description=description,
    )


@router.put(
    "/{product_id}",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def update_product(
    product_id: int,
    db: DBSession,
    name: str | None = None,
    price: float | None = None,
    description: str | None = None,
):
    product = await product_service.update_product(
        db,
        product_id=product_id,
        name=name,
        price=price,
        description=description,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.get("")
async def list_products(
    db: DBSession,
):
    return await product_service.list_products(db)
