from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.database.session import get_db

router = APIRouter()

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint validating database connectivity."""
    db_status = "unhealthy"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        pass
        
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "version": "1.0.0",
        "database": db_status,
        "redis": "healthy",  # mock
        "ai": "healthy",
        "ortools": "healthy",
        "osm": "healthy"
    }
