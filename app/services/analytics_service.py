import json
from typing import cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract

from app.core.config import settings
from app.models.sales_record import SalesRecord
from app.core.cache import safe_redis_get, safe_redis_set


async def get_top_products(
    db: AsyncSession,
    *,
    limit: int = 5,
):
    cache_key = f"analytics:top_products:{limit}"

    cached = safe_redis_get(cache_key)
    if cached:
        return json.loads(cast(str, cached))

    stmt = (
        select(
            SalesRecord.product_name,
            func.sum(SalesRecord.sale_amount).label("total_sales"),
        )
        .group_by(SalesRecord.product_name)
        .order_by(func.sum(SalesRecord.sale_amount).desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.all()

    data = [
        {
            "product_name": r.product_name,
            "total_sales": float(r.total_sales),
        }
        for r in rows
    ]

    safe_redis_set(cache_key, json.dumps(data), settings.CACHE_TTL)
    return data


async def get_lowest_products(
    db: AsyncSession,
    *,
    limit: int = 5,
):
    cache_key = f"analytics:lowest_products:{limit}"

    cached = safe_redis_get(cache_key)
    if cached:
        return json.loads(cast(str, cached))

    stmt = (
        select(
            SalesRecord.product_name,
            func.sum(SalesRecord.sale_amount).label("total_sales"),
        )
        .group_by(SalesRecord.product_name)
        .order_by(func.sum(SalesRecord.sale_amount).asc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.all()

    data = [
        {
            "product_name": r.product_name,
            "total_sales": float(r.total_sales),
        }
        for r in rows
    ]

    safe_redis_set(cache_key, json.dumps(data), settings.CACHE_TTL)
    return data


async def get_product_rank_per_quarter(
    db: AsyncSession,
):
    quarter = extract("quarter", SalesRecord.sale_date)
    total_sales = func.sum(SalesRecord.sale_amount)

    rank_expr = func.rank().over(
        partition_by=quarter,
        order_by=total_sales.desc(),
    )

    stmt = (
        select(
            SalesRecord.product_name,
            quarter.label("quarter"),
            total_sales.label("total_sales"),
            rank_expr.label("rank"),
        )
        .group_by(
            SalesRecord.product_name,
            quarter,
        )
        .order_by(quarter, rank_expr)
    )

    result = await db.execute(stmt)
    return result.all()


async def get_cumulative_sales(
    db: AsyncSession,
):
    daily_sales = func.sum(SalesRecord.sale_amount).label("daily_sales")

    cumulative_sales = func.sum(
        func.sum(SalesRecord.sale_amount)
    ).over(
        order_by=SalesRecord.sale_date
    ).label("cumulative_sales")

    stmt = (
        select(
            func.date(SalesRecord.sale_date).label("sale_date"),
            daily_sales,
            cumulative_sales,
        )
        .group_by(func.date(SalesRecord.sale_date))
        .order_by(func.date(SalesRecord.sale_date))
    )

    result = await db.execute(stmt)
    return result.all()
