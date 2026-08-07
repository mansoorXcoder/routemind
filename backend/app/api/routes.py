from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Dict, Any
from backend.app.database.session import get_db
from backend.app.models import Route, Stop, Package, Driver, Vehicle
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("")
async def get_routes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all routes."""
    result = await db.execute(
        select(Route)
        .options(
            selectinload(Route.driver),
            selectinload(Route.vehicle),
            selectinload(Route.hub)
        )
    )
    routes = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "route_code": r.route_code,
            "date": str(r.date),
            "status": r.status,
            "planned_distance": r.planned_distance,
            "planned_duration": r.planned_duration,
            "optimization_score": r.optimization_score,
            "driver_name": r.driver.name if r.driver else None,
            "vehicle_number": r.vehicle.vehicle_number if r.vehicle else None,
            "hub_name": r.hub.name if r.hub else None
        }
        for r in routes
    ]

@router.get("/{route_id}")
async def get_route_details(
    route_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single route details with vehicles and driver context."""
    import uuid
    try:
        route_uuid = uuid.UUID(route_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid route ID format")
        
    result = await db.execute(
        select(Route)
        .filter_by(id=route_uuid)
        .options(
            selectinload(Route.driver),
            selectinload(Route.vehicle),
            selectinload(Route.hub)
        )
    )
    r = result.scalars().first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        
    return {
        "id": str(r.id),
        "route_code": r.route_code,
        "date": str(r.date),
        "status": r.status,
        "planned_distance": r.planned_distance,
        "actual_distance": r.actual_distance,
        "planned_duration": r.planned_duration,
        "actual_duration": r.actual_duration,
        "optimization_score": r.optimization_score,
        "driver": {
            "id": str(r.driver.id),
            "name": r.driver.name,
            "phone": r.driver.phone
        } if r.driver else None,
        "vehicle": {
            "id": str(r.vehicle.id),
            "vehicle_number": r.vehicle.vehicle_number,
            "vehicle_type": r.vehicle.vehicle_type
        } if r.vehicle else None,
        "hub": {
            "id": str(r.hub.id),
            "name": r.hub.name,
            "city": r.hub.city
        } if r.hub else None
    }

@router.get("/{route_id}/stops")
async def get_route_stops(
    route_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve list of stops in sequence for a route, including package associations."""
    import uuid
    try:
        route_uuid = uuid.UUID(route_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid route ID format")
        
    result = await db.execute(
        select(Stop)
        .filter_by(route_id=route_uuid)
        .options(selectinload(Stop.packages))
    )
    stops = result.scalars().all()
    
    # Sort by sequence
    sorted_stops = sorted(stops, key=lambda s: s.sequence)
    
    res = []
    for s in sorted_stops:
        res.append({
            "id": str(s.id),
            "sequence": s.sequence,
            "customer_name": s.customer_name,
            "address": s.address,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "stop_type": s.stop_type,
            "status": s.status,
            "arrival_time": str(s.arrival_time) if s.arrival_time else None,
            "packages": [
                {
                    "id": str(p.id),
                    "tracking_number": p.tracking_number,
                    "weight": p.weight,
                    "volume": p.volume,
                    "cod_amount": p.cod_amount,
                    "status": p.status,
                    "delivery_type": p.delivery_type
                }
                for p in s.packages
            ]
        })
    return res
