from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.agents.analytics import AnalyticsAgent
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()
analytics_agent = AnalyticsAgent()

@router.get("/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compile overall metrics and analytics summaries using the Analytics Agent."""
    metrics = await analytics_agent.run(db)
    
    # Compile chart mock historical data points for the frontend charts
    # Daily savings over the last 7 days
    savings_history = [
        {"day": "Mon", "distance_saved": 12.5, "fuel_saved": 2.2, "cost_saved": 220},
        {"day": "Tue", "distance_saved": 18.2, "fuel_saved": 3.1, "cost_saved": 310},
        {"day": "Wed", "distance_saved": 15.0, "fuel_saved": 2.5, "cost_saved": 250},
        {"day": "Thu", "distance_saved": 22.1, "fuel_saved": 3.8, "cost_saved": 380},
        {"day": "Fri", "distance_saved": 28.4, "fuel_saved": 4.9, "cost_saved": 490},
        {"day": "Sat", "distance_saved": 30.5, "fuel_saved": 5.1, "cost_saved": 510},
        {"day": "Sun", "distance_saved": 18.5, "fuel_saved": 3.0, "cost_saved": 300}
    ]
    
    return {
        "metrics": metrics,
        "history": savings_history
    }
