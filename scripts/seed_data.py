import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models.user import User
from app.models.products import Product
from app.models.enums import Userrole
from app.core.security import hash_password
from app.db.base import Base


DATABASE_URL = "postgresql+asyncpg://postgres:password-1@localhost:5432/sales_backend_service"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def seed():
    async with engine.begin() as conn:
        # make sure tables exist
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # ---------
        # CEO USER
        # ---------
        ceo = User(
            username="Arunkrishna",
            email="arun@gmail.com",
            hashed_password=hash_password("password"),
            userrole=Userrole.CEO,
            is_active=True,
        )

        # ---------
        # SAMPLE PRODUCT
        # ---------
        product = Product(
            productname="Test Product",
            productprice=100,
            description="Seeded test product",
        )

        db.add_all([ceo, product])
        await db.commit()

        print("✅ Seed data inserted successfully")


if __name__ == "__main__":
    asyncio.run(seed())
