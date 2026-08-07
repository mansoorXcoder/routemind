from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict
from backend.app.database.session import get_db
from backend.app.models import Vehicle
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("")
async def get_vehicles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all vehicles."""
    result = await db.execute(select(Vehicle))
    vehicles = result.scalars().all()
    return [
        {
            "id": str(v.id),
            "vehicle_number": v.vehicle_number,
            "vehicle_type": v.vehicle_type,
            "capacity": v.capacity,
            "fuel_type": v.fuel_type,
            "current_driver": v.current_driver,
            "status": v.status,
            "latitude": v.current_latitude,
            "longitude": v.current_longitude
        }
        for v in vehicles
    ]

@router.get("/{vehicle_id}")
async def get_vehicle_details(
    vehicle_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import uuid
    try:
        vehicle_uuid = uuid.UUID(vehicle_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vehicle ID format")
        
    result = await db.execute(select(Vehicle).filter_by(id=vehicle_uuid))
    vehicle = result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        
    return {
        "id": str(vehicle.id),
        "vehicle_number": vehicle.vehicle_number,
        "vehicle_type": vehicle.vehicle_type,
        "capacity": vehicle.capacity,
        "fuel_type": vehicle.fuel_type,
        "current_driver": vehicle.current_driver,
        "status": vehicle.status,
        "latitude": vehicle.current_latitude,
        "longitude": vehicle.current_longitude,
        "hub_id": str(vehicle.hub_id) if vehicle.hub_id else None
    }
