from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.products import Product


async def create_product(
    db: AsyncSession,
    *,
    name: str,
    price: float,
    description: str | None = None,
) -> Product:
    product = Product(
        productname=name,
        productprice=price,
        description=description,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


async def update_product(
    db: AsyncSession,
    *,
    product_id: int,
    name: str | None = None,
    price: float | None = None,
    description: str | None = None,
) -> Product | None:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        return None

    if name is not None:
        setattr(product, "productname", name)

    if price is not None:
        setattr(product, "productprice", price)

    if description is not None:
        setattr(product,"description",description)

    await db.commit()
    await db.refresh(product)

    return product


async def list_products(
    db: AsyncSession,
) -> list[Product]:
    stmt = select(Product)
    result = await db.execute(stmt)
    products = list(result.scalars().all())
    return products
