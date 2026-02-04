from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sales_record import SalesRecord


async def list_sales_records(
    db: AsyncSession,
) -> list[SalesRecord]:
    stmt = select(SalesRecord)
    result = await db.execute(stmt)
    records = list(result.scalars().all())
    return records
