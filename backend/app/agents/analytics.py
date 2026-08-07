import logging
from typing import List, Dict, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models import Optimization, AIDecision

logger = logging.getLogger("analytics_agent")

class AnalyticsAgent:
    def __init__(self):
        pass
        
    async def run(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Query the database to compile running metrics and KPIs.
        """
        logger.info("Analytics Agent collecting system-wide metrics...")
        
        # 1. Query all optimizations
        opt_result = await db.execute(select(Optimization))
        opts = opt_result.scalars().all()
        
        total_distance_saved = sum(o.distance_saved for o in opts)
        total_time_saved = sum(o.time_saved for o in opts)
        total_fuel_saved = sum(o.fuel_saved for o in opts)
        total_carbon_saved = sum(o.carbon_saved for o in opts)
        
        # 2. Query AI decisions for approval rate
        decision_result = await db.execute(select(AIDecision))
        decisions = decision_result.scalars().all()
        
        total_decisions = len(decisions)
        approved_decisions = sum(1 for d in decisions if d.approved)
        rejected_decisions = total_decisions - approved_decisions
        
        approval_rate = (approved_decisions / max(1, total_decisions)) * 100.0
        
        # Calculate approximate cost savings (assume 100 INR per liter of fuel saved)
        cost_saved_inr = total_fuel_saved * 100.0
        
        return {
            "total_distance_saved_km": round(total_distance_saved, 2),
            "total_time_saved_min": round(total_time_saved, 2),
            "total_fuel_saved_liters": round(total_fuel_saved, 2),
            "total_carbon_saved_kg": round(total_carbon_saved, 2),
            "cost_saved_inr": round(cost_saved_inr, 2),
            "approval_rate_percent": round(approval_rate, 2),
            "approved_plans_count": approved_decisions,
            "rejected_plans_count": rejected_decisions,
            "total_ai_decisions_count": total_decisions
        }
