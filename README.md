# Sales Backend Service

A production-style **Sales Management Backend API** built with **FastAPI**, **async SQLAlchemy**, **PostgreSQL**, and **Redis**.

This project is designed as a **realistic backend portfolio project**, following clean architecture, async-first design, and industry practices. It focuses on **auth, RBAC, analytics, audit logging, and performance**, and is intentionally **backend-only**.

---

##  Live Deployment

* **API Base URL**: [https://sales-backend-service.onrender.com](https://sales-backend-service.onrender.com)
* **Swagger UI**: [https://sales-backend-service.onrender.com/docs](https://sales-backend-service.onrender.com/docs)
* **ReDoc**: [https://sales-backend-service.onrender.com/redoc](https://sales-backend-service.onrender.com/redoc)

* **use this** to authorize as admin in swagger UI and play with the API features.
  user= ceo@company.com
  password= StrongPass123

> The root route (`/`) returns `404` by design. Swagger is the primary interface.

---

##  Features

###  Authentication & Authorization

* JWT-based authentication
* Role-Based Access Control (RBAC)
* Roles supported:

  * **CEO**
  * **Salesperson**
  * **Customer**

###  User Management

* Secure user model with hashed passwords
* Role assignment and permission enforcement
* Public user creation disabled to prevent privilege escalation
* Initial privileged users bootstrapped directly at DB level (one-time)

###  Product Management

* **CEO & Salesperson**

  * Create and update products
* **Customer**

  * Read-only access to products

###  Order Management

* Customers can create orders
* CEO & Salesperson can:

  * View all orders
  * Update order status
* Automatic creation of:

  * Sales records
  * Audit logs

###  Analytics

* Top-selling products
* Lowest-selling products
* Sales ranking using SQL window functions
* Optimized with Redis caching

###  Audit Logging

* Tracks critical actions:

  * Create
  * Update
  * Status change
* Records:

  * Actor
  * Action
  * Entity
  * Timestamp

###  Performance

* Redis caching for analytics queries
* Fully async database operations

---

##  Tech Stack

* Python 3.11+
* FastAPI
* SQLAlchemy 2.0 (Async ORM)
* PostgreSQL (Render)
* Redis
* JWT (`python-jose`)
* Passlib (bcrypt)
* Alembic
* Pytest
* Uvicorn
* Docker

---

##  Project Structure

```
sales-backend-service/
├── app/
│   ├── main.py
│   ├── core/          # config, security, dependencies, cache
│   ├── db/            # async DB engine & base
│   ├── models/        # SQLAlchemy models & enums
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # business logic
│   └── routers/       # API routes
│
├── alembic/            # migrations
├── scripts/            # one-time bootstrap & utilities
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

##  Architecture Principles

* Clear separation of concerns:

  * Routers → HTTP layer
  * Services → business logic
  * Models → database layer
* Async-first design
* Testable service layer
* Real-world RBAC patterns

---

##  Authentication Flow

1. Login via `POST /auth/login`
2. Receive JWT access token
3. Authorize in Swagger:

   ```
   Bearer <access_token>
   ```
4. Access protected endpoints based on role

---

##  Database & Migrations

* Async DB access via `asyncpg`
* Alembic migrations with async → sync URL conversion

Apply migrations:

```bash
alembic upgrade head
```

---

##  Docker

### Build image

```bash
docker build -t sales-backend-api .
```

### Run container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e SECRET_KEY=your-secret \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=15 \
  -e CACHE_TTL=300 \
  -e REDIS_URL=redis://... \
  sales-backend-api
```

---

##  Testing

```bash
pytest
```

Includes:

* Authentication tests
* RBAC enforcement
* Order → SalesRecord → AuditLog integration tests

---

##  Deployment

* Deployed on **Render** using Docker
* PostgreSQL provided by Render
* Internal DB URL used by the service
* External DB URL used for migrations

---

##  Why This Project?

This project demonstrates:

* Real backend system design
* Auth + RBAC done correctly
* Analytics using SQL window functions
* Audit logging patterns
* Caching strategies
* Clean, scalable architecture

Designed specifically for **backend developer portfolios** and **production-ready thinking**.

---

##  Future Improvements

* User self-registration (restricted)
* Refresh tokens
* Pagination & filtering
* Background tasks (Celery / RQ)
* CI/CD pipeline

---

##  Author

**Arun Krishna**

---

## 📄 License

MIT
