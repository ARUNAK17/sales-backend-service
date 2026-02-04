from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, cast

from app.db.engine import async_db_session_dependency
from app.core.dependencies import require_role, get_current_user,require_roles
from app.models.enums import Userrole, OrderStatus
from app.models.user import User
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

DBSession = async_db_session_dependency


@router.post(
    "",
    dependencies=[Depends(require_role(Userrole.Customer))],
)
async def create_order(
    db: DBSession,
    order_number: str,
    order_item: str,
    current_user: User = Depends(get_current_user),
):
    return await order_service.create_order(
        db,
        order_number=order_number,
        order_item=order_item,
        actor_id=cast(int, current_user.id),
    )


@router.put(
    "/{order_id}/status",
    dependencies=[
        Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: DBSession,
    current_user: User = Depends(get_current_user),
):
    order = await order_service.update_order_status(
        db,
        order_id=order_id,
        status=new_status,
        actor_id=cast(int, current_user.id),
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@router.get(
    "",
    dependencies=[
    Depends(require_roles(Userrole.CEO, Userrole.Salesperson)),
    ],
)
async def list_orders(
    db: DBSession,
):
    return await order_service.list_orders(db)
