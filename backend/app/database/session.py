import os
import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from backend.app.core.config import settings

logger = logging.getLogger("db_session")

# Determine engine type and handle fallback
db_url = settings.DATABASE_URL

# Fallback to local SQLite if Postgres is unavailable
if "postgresql" in db_url:
    import socket
    try:
        netloc = db_url.split("@")[1].split("/")[0]
        if ":" in netloc:
            host, port = netloc.split(":")
            port = int(port)
        else:
            host = netloc
            port = 5432
            
        s = socket.create_connection((host, port), timeout=1.0)
        s.close()
    except Exception:
        logger.warning("PostgreSQL is unreachable. Falling back to local SQLite: routemind.db")
        db_url = "sqlite+aiosqlite:///./routemind.db"

# Create async engine
engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping=True,
    **({
        "pool_size": 10,
        "max_overflow": 20
    } if "postgresql" in db_url else {})
)

# Async sessionmaker
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# FastAPI dependency to yield async DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
