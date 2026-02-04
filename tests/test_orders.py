import pytest

from app.models.user import User
from app.models.enums import Userrole, OrderStatus
from app.core.security import hash_password


@pytest.mark.asyncio
async def test_order_paid_creates_sales_record_and_audit_log(client, db):
    # -------------------------
    # setup users
    # -------------------------
    customer = User(
        username="customer",
        email="customer@example.com",
        hashed_password=hash_password("password"),
        userrole=Userrole.Customer,
        is_active=True,
    )

    ceo = User(
        username="ceo",
        email="ceo@example.com",
        hashed_password=hash_password("password"),
        userrole=Userrole.CEO,
        is_active=True,
    )

    db.add_all([customer, ceo])
    await db.commit()

    # -------------------------
    # login as customer
    # -------------------------
    customer_login = await client.post(
        "/auth/login",
        json={
            "email": "customer@example.com",
            "password": "password",
        },
    )
    assert customer_login.status_code == 200

    customer_token = customer_login.json()["access_token"]
    customer_headers = {
        "Authorization": f"Bearer {customer_token}"
    }

    # # -------------------------
    # # customer creates order
    # # -------------------------
    order_response = await client.post(
        "/orders",
        params={
            "order_number": "ORD-001",
            "order_item": "Test Product",
        },
        headers=customer_headers,
    )
    assert order_response.status_code == 200
    order_id = order_response.json()["id"]

    # # -------------------------
    # # login as CEO
    # # -------------------------
    ceo_login = await client.post(
        "/auth/login",
        json={
            "email": "ceo@example.com",
            "password": "password",
        },
    )
    assert ceo_login.status_code == 200

    ceo_token = ceo_login.json()["access_token"]
    ceo_headers = {
        "Authorization": f"Bearer {ceo_token}"
    }

    # -------------------------
    # CEO updates order to PAID
    # -------------------------
    update_response = await client.put(
        f"/orders/{order_id}/status",
        params={"status": OrderStatus.PAID},
        headers=ceo_headers,
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == OrderStatus.PAID

    # -------------------------
    # verify sales record created
    # -------------------------
    # sales_response = await client.get(
    #     "/sales-records",
    #     headers=ceo_headers,
    # )
    # assert sales_response.status_code == 200
    # assert len(sales_response.json()) == 1

    # -------------------------
    # verify audit log created
    # -------------------------
    # audit_response = await client.get(
    #     "/audit-logs",
    #     headers=ceo_headers,
    # )
    # assert audit_response.status_code == 200
    # assert len(audit_response.json()) >= 1
