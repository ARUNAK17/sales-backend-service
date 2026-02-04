from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.audit_log import AuditLog


async def log_action(
    db: AsyncSession,
    *,
    actor_id: int,
    action: str,
    entity: str,
    entity_id: int,
) -> None:
    log = AuditLog(
        actor_id=actor_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
    )

    db.add(log)
    await db.commit()


async def list_audit_logs(
    db: AsyncSession,
) -> list[AuditLog]:
    stmt = select(AuditLog)
    result = await db.execute(stmt)
    logs = list(result.scalars().all())
    return logs
