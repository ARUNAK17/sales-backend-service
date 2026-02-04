from fastapi import FastAPI

from app.routers import (
    auth,
    users,
    products,
    orders,
    sales_records,
    analytics,
    audit_logs,
)

app = FastAPI(title="Sales Backend Service")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(sales_records.router)
app.include_router(analytics.router)
app.include_router(audit_logs.router)
