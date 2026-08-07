import asyncio
import logging
from backend.app.database.base import Base
from backend.app.database.session import engine

# Import all models to register them on Base.metadata
from backend.app.models import (
    User, Hub, Driver, Vehicle, Route, Stop, Package,
    Optimization, AIDecision, RouteHistory, Notification,
    Analytics, TrafficEvent, WeatherEvent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_init")

async def init_db():
    logger.info("Initializing database tables...")
    async with engine.begin() as conn:
        # Create all tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
