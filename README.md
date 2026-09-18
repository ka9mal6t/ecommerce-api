# Ecommerce API

An asynchronous backend foundation for an e-commerce application. The project uses FastAPI for the HTTP API, PostgreSQL for persistence, SQLAlchemy's async ORM layer, Alembic for schema migrations, and JWT bearer tokens for authenticated requests.

> All router modules in this repository are registered by `app/main.py` and are available through the FastAPI application.

## Highlights

- **Async by default** — FastAPI, `asyncpg`, and SQLAlchemy's `AsyncSession` keep database I/O non-blocking.
- **JWT authentication** — register a user, sign in, and use a bearer token for protected endpoints.
- **Role-aware domain layer** — the data model includes `Admin` and `User` roles; management handlers check for the `Admin` role.
- **E-commerce data model** — users, roles, categories, products, orders, order items, and order statuses.
- **Database migrations** — Alembic is configured to use the async database URL and SQLAlchemy metadata.
- **Docker Compose setup** — PostgreSQL and the API are defined as a single local stack.

## Technology

| Area | Tooling |
| --- | --- |
| API | FastAPI, Uvicorn |
| Database | PostgreSQL 16, SQLAlchemy 2.0, asyncpg |
| Schema migrations | Alembic |
| Authentication | PyJWT |
| Validation | Pydantic v2, email-validator |
| Configuration | python-dotenv |
| Containers | Docker, Docker Compose |

## Project structure

```text
app/
├── main.py                 # FastAPI app, registered routers, CORS
├── config.py               # Environment-driven settings and database URL
├── database.py             # Async engine, sessions, SQLAlchemy base
├── dao/base.py             # Reusable async CRUD data-access operations
├── users/                  # Registration, login, JWT dependency, user model
├── roles/                  # Role model, DAO, initial role setup
├── categories/             # Category model, DAO, admin handlers
├── products/               # Product model, schemas, DAO, admin handlers
├── orders/                 # Order model, DAO, handlers
├── order_items/            # Order line-item model, DAO, handlers
├── status/                 # Order-status model and DAO
└── migrations/             # Alembic migration environment
docker/
└── app.sh                  # Waits for PostgreSQL, migrates, starts the API
docker-compose.yml          # API and PostgreSQL services
```

## Prerequisites

Choose one of the following ways to run the service:

- **Local development:** Python 3.14, PostgreSQL 16, and a virtual environment.
- **Containers:** Docker Engine and Docker Compose.

The database must be reachable using the credentials configured in `.env`.

## Configuration

The project reads configuration from a `.env` file in the repository root. This file is ignored by Git — keep its passwords and JWT signing key private.

The checked local configuration is a **Docker Compose profile**. It has these required variables:

```dotenv
# API connection to the PostgreSQL Compose service
DB_HOST=db
DB_PORT=5432
DB_NAME=<your-database-name>
DB_USER=<your-database-user>
DB_PASS=<your-database-password>

# PostgreSQL container initialization — must match the DB_* values above
POSTGRES_DB=<same-as-DB_NAME>
POSTGRES_USER=<same-as-DB_USER>
POSTGRES_PASSWORD=<same-as-DB_PASS>

# JWT
ACCESS_SECRET_KEY=<long-random-secret>
ALGORITHM=HS256
```

`db` is the PostgreSQL service name from `docker-compose.yml`, so it is the correct host **inside the API container**. The Compose service exposes PostgreSQL at `localhost:5432` for applications running directly on your machine.

## Run locally

Use this option when PostgreSQL is already running locally, or when you want to run only the API on your machine while using the database started by Compose.

1. Create and activate a virtual environment.

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Start PostgreSQL. Its database name, user, and password must match `DB_NAME`, `DB_USER`, and `DB_PASS` in `.env`.

4. Override the Docker-only hostname for the current PowerShell session. This leaves `.env` unchanged and points the local API to the PostgreSQL port exposed on your machine.

   ```powershell
   $env:DB_HOST = "localhost"
   ```

5. Apply database migrations.

   ```powershell
   alembic upgrade head
   ```

6. Start the development server.

   ```powershell
   uvicorn app.main:app --reload
   ```

The API is available at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is served at [`/docs`](http://127.0.0.1:8000/docs), and the ReDoc view at [`/redoc`](http://127.0.0.1:8000/redoc).

## Run with Docker Compose

This is the recommended option for a complete local stack. The existing `.env` already uses `DB_HOST=db`, which is correct for this flow.

1. Build and start the stack.

   ```bash
   docker compose up --build
   ```

The API container waits for `db:5432`, runs `alembic upgrade head`, then starts the application on port `8000`. PostgreSQL is exposed at `localhost:5432` and the API at `http://localhost:8000`.

To stop the stack:

```bash
docker compose down
```

## Current HTTP API

All currently registered endpoints are listed below. FastAPI also exposes the same information interactively at `/docs`.

| Method | Endpoint | Authentication | Description |
| --- | --- | --- | --- |
| `GET` | `/connection/ping` | No | Health-style connectivity check; returns `pong`. |
| `GET` | `/connection/hello` | Bearer token | Returns a greeting for the authenticated user. |
| `POST` | `/auth/register` | No | Creates a user account and ensures the default roles are initialized. |
| `POST` | `/auth/login` | No | Authenticates by username and returns a JWT access token. |
| `POST` | `/categories/add` | Admin bearer token | Creates a category. `name` and optional `description` are query parameters. |
| `POST` | `/categories/delete` | Admin bearer token | Deletes a category by the `category_id` query parameter. |
| `POST` | `/categories/update` | Admin bearer token | Updates a category using `category_id`, `name`, and optional `description` query parameters. |
| `POST` | `/products/add` | Admin bearer token | Creates a product from a JSON body; optional `category_id` is a query parameter. |
| `POST` | `/products/delete` | Admin bearer token | Deletes a product by the `product_id` query parameter. |
| `POST` | `/products/update` | Admin bearer token | Updates a product from a JSON body; optional `category_id` is a query parameter. |
| `POST` | `/orders/add` | Bearer token | Creates an order for the authenticated user with `Created` status. |
| `POST` | `/orders/delete` | Bearer token | Deletes an order by the `order_id` query parameter. |
| `POST` | `/orders/update` | Admin bearer token | Changes an order status using `order_id` and `new_status` query parameters. |
| `POST` | `/order_items/add` | Bearer token | Adds a product and quantity to an owned order. Parameters: `order_id`, `product_id`, `quantity`. |
| `POST` | `/order_items/delete` | Bearer token | Deletes an order item by the `order_item_id` query parameter. |
| `POST` | `/order_items/update` | Bearer token | Updates an order item with `order_item_id`, `product_id`, and `quantity`. |

### Register a user

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "change-me"
  }'
```

### Sign in

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "change-me"
  }'
```

Successful login returns a response in this shape:

```json
{
  "token_type": "Bearer",
  "accessToken": "<JWT>"
}
```

### Call a protected endpoint

```bash
curl http://127.0.0.1:8000/connection/hello \
  -H "Authorization: Bearer <JWT>"
```

Access tokens currently expire after 2,000 minutes. Include the token in the `Authorization` header exactly as shown above.

### Product request body

Use this JSON body for `POST /products/add` and `POST /products/update`:

```json
{
  "name": "Wireless headphones",
  "description": "Over-ear Bluetooth headphones",
  "price": 99.99,
  "image_url": "https://example.com/headphones.jpg"
}
```

## Data model

```text
Roles 1 ─── * Users 1 ─── * Orders 1 ─── * OrderItems * ─── 1 Products * ─── 1 Categories
                         |
                         └─────────────────────────────── 1 Status
```

- **Roles** define user access levels.
- **Users** have a unique username and email, a password hash, and a role.
- **Categories** group products.
- **Products** contain a name, description, decimal price, optional image URL, and category.
- **Orders** belong to a user and reference a status such as `Created`.
- **Order items** link orders to products and capture quantity.

## Database migrations

Create an autogenerated migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

Apply all pending migrations:

```bash
alembic upgrade head
```

The migration environment loads the models explicitly so that `Base.metadata` contains the full schema.

## Security notes

- Never commit `.env`, database passwords, or `ACCESS_SECRET_KEY`.
- Use a high-entropy signing key and a secure production secret manager.
- All authenticated requests require `Authorization: Bearer <JWT>`.
- Password hashing currently uses SHA-256. Before production use, migrate to a deliberately slow password-hashing algorithm such as Argon2 or bcrypt.
- The app currently allows CORS requests from every origin. Restrict `origins` in `app/main.py` before deploying to production.

## Current setup caveats

- The Docker startup script launches Gunicorn, but `gunicorn` is not listed in `requirements.txt` at present. Add it to the dependency list before relying on the Compose workflow.
- Alembic is configured, but no revision files are currently committed under `app/migrations/versions`. Generate and commit an initial migration before expecting `alembic upgrade head` to create the schema.

## Development roadmap

- Add read/list endpoints, pagination, filtering, and consistent response schemas.
- Add automated tests and CI.
- Replace the password hashing implementation with Argon2 or bcrypt.
- Add structured error responses and operational health checks.
- Tighten CORS, secrets management, and production logging.

## License

This project is licensed under the [MIT License](LICENSE). You may use, modify, and distribute it in accordance with the terms in the license file.
