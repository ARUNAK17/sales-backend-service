from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Create the engine
DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# expose async session using dependency
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# reusable DB dependency (instead of writing: db: AsyncSession = Depends(get_async_db_session) in every route)
#db: async_db_session_dependency
async_db_session_dependency = Annotated[
    AsyncSession,
    Depends(get_async_db_session)
]

#intialize alembic
"""alembic init alembic"""
""" import setting and base in alembic env.py"""
"""change metadata"""
"""change URL inn online & offline(add newly in online) in SET also add a function to replace async since alembic doesnt support async"""
"""import all the model in the env.py alembic"""
"""alembic revision --autogenerate -m "initial migration"
"""
"""alembic upgrade head
"""  #to apply the migration
"""alembic downgrade -1 """   #To rollback previous upgrade we downgrade