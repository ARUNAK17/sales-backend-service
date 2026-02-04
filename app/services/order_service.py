from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import cast

from app.models.orders import Order
from app.models.products import Product
from app.models.sales_record import SalesRecord
from app.models.enums import OrderStatus
from app.services.audit_service import log_action


async def create_order(
    db: AsyncSession,
    *,
    order_number: str,
    order_item: str,
    actor_id: int,
) -> Order:
    order = Order(
        order_number=order_number,
        order_item=order_item,
        status=OrderStatus.CREATED,
    )

    db.add(order)
    await db.flush()  # ensures order.id is available

    await log_action(
        db,
        actor_id=actor_id,
        action="CREATE",
        entity="Order",
        entity_id=cast(int, order.id),
    )

    await db.commit()
    await db.refresh(order)

    return order


async def update_order_status(
    db: AsyncSession,
    *,
    order_id: int,
    status: OrderStatus,
    actor_id: int,
) -> Order | None:
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        return None

    setattr(order, "status", status)

    await log_action(
        db,
        actor_id=actor_id,
        action=f"UPDATE_STATUS:{status}",
        entity="Order",
        entity_id=cast(int, order.id),
    )

    # 🔹 create SalesRecord when order is PAID
    if status == OrderStatus.PAID:
        product_stmt = select(Product).where(
            Product.productname == order.order_item
        )
        product_result = await db.execute(product_stmt)
        product = product_result.scalar_one_or_none()

        if product:
            sales_record = SalesRecord(
                order_number=order.order_number,
                product_name=order.order_item,
                sale_amount=product.productprice,
            )
            db.add(sales_record)

            await log_action(
                db,
                actor_id=actor_id,
                action="CREATE",
                entity="SalesRecord",
                entity_id=cast(int, order.id),
            )

    await db.commit()
    await db.refresh(order)

    return order


async def list_orders(
    db: AsyncSession,
) -> list[Order]:
    stmt = select(Order)
    result = await db.execute(stmt)
    orders = list(result.scalars().all())
    return orders
