import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, List, Optional
from backend.app.database.session import get_db
from backend.app.models import Route, Stop, Optimization, AIDecision, RouteHistory
from backend.app.agents.coordinator import coordinator
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()
logger = logging.getLogger("optimization_api")

class OptimizeRequest(BaseModel):
    route_id: str

class ReplanRequest(BaseModel):
    route_id: str
    event_type: str  # traffic, weather, road_closure, vehicle_breakdown, new_pickup
    event_details: Dict[str, Any]
    current_stop_index: int = 0

class ApproveRequest(BaseModel):
    optimization_id: str

@router.post("/run")
async def run_optimization(
    data: OptimizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger the Multi-Agent route optimization pipeline."""
    res = await coordinator.optimize_route(db, data.route_id)
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error", "Optimization failed"))
    return res

@router.post("/replan")
async def run_replanning(
    data: ReplanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger dynamic replanning due to a real-time event."""
    res = await coordinator.replan_on_event(
        db=db,
        route_id=data.route_id,
        event_type=data.event_type,
        event_details=data.event_details,
        current_stop_index=data.current_stop_index
    )
    if not res.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error", "Replanning failed"))
    return res

@router.get("/compare/{route_id}")
async def compare_route(
    route_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the latest pending optimization comparison for a route."""
    import uuid
    try:
        route_uuid = uuid.UUID(route_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid route ID format")
        
    # Find the latest optimization for this route
    result = await db.execute(
        select(Optimization)
        .filter_by(route_id=route_uuid)
        .order_by(Optimization.created_at.desc())
    )
    opt = result.scalars().first()
    if not opt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No optimization records found for this route")
        
    return {
        "optimization_id": str(opt.id),
        "route_id": str(opt.route_id),
        "optimization_type": opt.optimization_type,
        "algorithm": opt.algorithm,
        "distance_saved_km": opt.distance_saved,
        "time_saved_min": opt.time_saved,
        "fuel_saved_liters": opt.fuel_saved,
        "carbon_saved_kg": opt.carbon_saved,
        "confidence": opt.confidence,
        "reason": opt.reason,
        "old_route_sequence": opt.old_route,
        "new_route_sequence": opt.new_route
    }

@router.post("/approve")
async def approve_optimization(
    data: ApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve the pending optimized route and write changes to route stops."""
    import uuid
    try:
        opt_uuid = uuid.UUID(data.optimization_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid optimization ID format")
        
    result = await db.execute(select(Optimization).filter_by(id=opt_uuid))
    opt = result.scalars().first()
    if not opt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Optimization record not found")
        
    # 1. Fetch the Route
    route_result = await db.execute(select(Route).filter_by(id=opt.route_id))
    route = route_result.scalars().first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated route not found")
        
    # 2. Fetch current stops of the route
    stops_result = await db.execute(select(Stop).filter_by(route_id=route.id))
    stops = stops_result.scalars().all()
    
    # 3. Apply the new sequences from opt.new_route
    # opt.new_route is a list of {"stop_id": "...", "sequence": idx}
    new_sequences = {item["stop_id"]: item["sequence"] for item in opt.new_route}
    
    for stop in stops:
        stop_id_str = str(stop.id)
        if stop_id_str in new_sequences:
            stop.sequence = new_sequences[stop_id_str]
            
    # 4. Update Route planned totals
    route.planned_distance = max(0.0, route.planned_distance - opt.distance_saved)
    route.planned_duration = max(0.0, route.planned_duration - opt.time_saved)
    route.optimization_score = min(100.0, opt.confidence)
    route.status = "planned"
    
    # 5. Mark AIDecision as approved
    decision_result = await db.execute(select(AIDecision).filter_by(route_id=route.id).order_by(AIDecision.created_at.desc()))
    dec = decision_result.scalars().first()
    if dec:
        dec.approved = True
        
    # 6. Save Route History entry
    history = RouteHistory(
        route_id=route.id,
        version=1,  # increment or load
        modified_by=current_user.name,
        change_reason=f"Approved optimization: {opt.reason}",
        old_data=opt.old_route,
        new_data=opt.new_route
    )
    db.add(history)
    await db.commit()
    
    return {
        "success": True,
        "message": f"Optimization for route {route.route_code} approved successfully.",
        "new_distance_km": route.planned_distance,
        "new_duration_min": route.planned_duration
    }

@router.post("/reject")
async def reject_optimization(
    data: ApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject the pending optimization."""
    import uuid
    try:
        opt_uuid = uuid.UUID(data.optimization_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid optimization ID format")
        
    result = await db.execute(select(Optimization).filter_by(id=opt_uuid))
    opt = result.scalars().first()
    if not opt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Optimization record not found")
        
    # Mark decision as rejected (approved = False)
    decision_result = await db.execute(select(AIDecision).filter_by(route_id=opt.route_id).order_by(AIDecision.created_at.desc()))
    dec = decision_result.scalars().first()
    if dec:
        dec.approved = False
        
    # Remove the optimization run record if rejected
    await db.delete(opt)
    await db.commit()
    
    return {
        "success": True,
        "message": "Route optimization rejected."
    }
