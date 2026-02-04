sales_backend_service/
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py            # env vars, settings
│   │   ├── security.py          # JWT, password hashing
│   │   ├── dependencies.py      # RBAC, current_user, db deps
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── sales_record.py
│   │   ├── audit_log.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── analytics.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── analytics.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── order_service.py
│   │   ├── analytics_service.py
│   │   ├── audit_service.py
│   │   └── __init__.py
│   │
│   ├── db/
│   │   ├── session.py           # async session maker
│   │   ├── base.py              # SQLAlchemy Base
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── tests/
│   ├── conftest.py              # test DB, fixtures, overrides
│   │
│   ├── db/
│   │   ├── test_session.py      # test DB engine (SQLite / Postgres)
│   │   └── test_data.py         # seed data helpers
│   │
│   ├── fakes/                   # test doubles (no real DB/Redis)
│   │   ├── fake_users.py
│   │   ├── fake_orders.py
│   │   └── fake_analytics.py
│   │
│   ├── mocks/                   # mocked external services
│   │   ├── mock_redis.py
│   │   └── mock_auth.py
│   │
│   ├── test_auth.py
│   ├── test_orders.py
│   ├── test_analytics.py
│   ├── test_rbac.py
│   └── __init__.py
│
├── scripts/
│   ├── seed_data.py             # manual data seeding
│   ├── create_admin.py          # create CEO user
│   └── backfill_sales.py
│
├── requirements.txt
├── alembic.ini
├── .env
├── .env.test                    # test-specific env
└── README.md
