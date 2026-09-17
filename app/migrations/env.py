from logging.config import fileConfig
import sys
from os.path import dirname, abspath
import asyncio
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import DATABASE_URL
from app.database import Base

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.roles.models import Roles
from app.users.models import Users
from app.status.models import Status
from app.categories.models import Categories
from app.products.models import Products
from app.orders.models import Orders
from app.order_items.models import OrderItems

target_metadata = Base.metadata

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
config.set_main_option('sqlalchemy.url', f'{DATABASE_URL}?async_fallback=True')

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    """Run migrations using a synchronous Alembic connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()



async def run_async_migrations() -> None:
    """Run migrations using an async SQLAlchemy engine."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:


    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
