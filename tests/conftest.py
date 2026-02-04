import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.db.base import Base
from app.db.engine import get_async_db_session


# -------------------------
# TEST DATABASE
# -------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# -------------------------
# CREATE + DROP TABLES
# -------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# -------------------------
# DB SESSION FIXTURE (IMPORTANT)
# -------------------------
@pytest_asyncio.fixture
async def db():
    async with TestingSessionLocal() as session:
        yield session


# -------------------------
# OVERRIDE APP DB DEPENDENCY
# -------------------------
async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def override_dependency():
    app.dependency_overrides[get_async_db_session] = override_db


# -------------------------
# TEST CLIENT
# -------------------------
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
