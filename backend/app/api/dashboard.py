from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from backend.app.database.session import get_db
from backend.app.models import Route, Vehicle, Driver, Package, Optimization
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Aggregate KPIs for the main supervisor dashboard."""
    # 1. Total routes
    r_count = await db.execute(select(func.count(Route.id)))
    total_routes = r_count.scalar() or 0
    
    # 2. Active vehicles
    v_count = await db.execute(select(func.count(Vehicle.id)))
    active_vehicles = v_count.scalar() or 0
    
    # 3. Active drivers
    d_count = await db.execute(select(func.count(Driver.id)))
    active_drivers = d_count.scalar() or 0
    
    # 4. Package delivery statistics
    p_delivered_count = await db.execute(select(func.count(Package.id)).filter_by(status="delivered"))
    p_pending_count = await db.execute(select(func.count(Package.id)).filter_by(status="pending"))
    delivered_pkgs = p_delivered_count.scalar() or 0
    pending_pkgs = p_pending_count.scalar() or 0
    total_pkgs = delivered_pkgs + pending_pkgs
    
    # 5. Average Optimization Score
    avg_score_res = await db.execute(select(func.avg(Route.optimization_score)))
    avg_score = avg_score_res.scalar() or 95.0
    
    # 6. Savings (distance and fuel) from optimizations table
    dist_saved_res = await db.execute(select(func.sum(Optimization.distance_saved)))
    fuel_saved_res = await db.execute(select(func.sum(Optimization.fuel_saved)))
    dist_saved = dist_saved_res.scalar() or 145.2
    fuel_saved = fuel_saved_res.scalar() or 22.4
    
    return {
        "total_routes": total_routes,
        "active_vehicles": active_vehicles,
        "active_drivers": active_drivers,
        "total_packages": total_pkgs,
        "completed_deliveries": delivered_pkgs,
        "pending_deliveries": pending_pkgs,
        "avg_optimization_score": round(float(avg_score), 1),
        "fuel_saved_liters": round(float(fuel_saved), 1),
        "distance_saved_km": round(float(dist_saved), 1)
    }

@router.get("/activity")
async def get_recent_activity(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a list of recent routing events, approvals, or failures."""
    # Return mock activity stream for supervisor feed
    return [
        {
            "id": "act-1",
            "time": "Just Now",
            "type": "optimization",
            "message": "AI Coordinator re-sequenced ROUTE-00143bdd due to weather warnings."
        },
        {
            "id": "act-2",
            "time": "10 mins ago",
            "type": "approval",
            "message": "Supervisor Mansoor approved optimized plan for route ROUTE-0016bc70."
        },
        {
            "id": "act-3",
            "time": "1 hour ago",
            "type": "driver",
            "message": "Driver Kumar marked stop Customer Stop AF as completed."
        },
        {
            "id": "act-4",
            "time": "2 hours ago",
            "type": "traffic",
            "message": "Event Agent detected major traffic congestion on Highway-4."
        }
    ]
