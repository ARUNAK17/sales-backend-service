from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.enums import Userrole


async def create_user(
    db: AsyncSession,
    *,
    username: str,
    email: str,
    hashed_password: str,
    role: Userrole,
) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        userrole=role,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_user(
    db: AsyncSession,
    *,
    user_id: int,
    username: str | None = None,
    email: str | None = None,
    role: Userrole | None = None,
    is_active: bool | None = None,
) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return None

    if username is not None:
        setattr(user, "username", username)

    if email is not None:
        setattr(user, "email", email)

    if role is not None:
        setattr(user, "userrole", role)

    if is_active is not None:
        setattr(user, "is_active", is_active)

    await db.commit()
    await db.refresh(user)

    return user


async def list_users(
    db: AsyncSession,
) -> list[User]:
    stmt = select(User)
    result = await db.execute(stmt)
    users = list(result.scalars().all())
    return users
