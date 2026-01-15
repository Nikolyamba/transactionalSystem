import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool, Connection

from backend.database.base import Base

load_dotenv()
DATABASE_URL = os.getenv("DB_URL")

config = context.config
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from backend.models import *
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Миграции в оффлайн режиме (SQL скрипт)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online_async() -> None:
    """Миграции онлайн (асинхронно)."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Выбор режима запуска Alembic."""
    if config.attributes.get("asynchronous", False):
        asyncio.run(run_migrations_online_async())
    else:
        from sqlalchemy import create_engine

        sync_url = DATABASE_URL.replace("+asyncpg", "")
        connectable = create_engine(sync_url, poolclass=pool.NullPool)

        with connectable.connect() as connection:
            do_run_migrations(connection)

if context.is_offline_mode():
    run_migrations_offline()
else:
    config.attributes["asynchronous"] = True
    run_migrations_online()