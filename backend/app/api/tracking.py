from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any, Optional

from backend.app.database.session import get_db
from backend.app.models import Vehicle
from backend.app.api.websocket import manager
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

class GPSUpdateRequest(BaseModel):
    vehicle_id: str
    latitude: float
    longitude: float
    status: Optional[str] = None  # online, idle, offline, emergency

@router.post("/update")
async def update_gps_position(
    data: GPSUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Simulated GPS update endpoint. Updates vehicle coordinates in DB,
    and broadcasts a websocket update event to the dashboard clients.
    """
    import uuid
    try:
        vehicle_uuid = uuid.UUID(data.vehicle_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vehicle ID format")
        
    result = await db.execute(select(Vehicle).filter_by(id=vehicle_uuid))
    vehicle = result.scalars().first()
    
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        
    vehicle.current_latitude = data.latitude
    vehicle.current_longitude = data.longitude
    if data.status:
        vehicle.status = data.status
        
    await db.commit()
    
    # Broadcast event via websocket
    event_payload = {
        "event": "vehicle.updated",
        "data": {
            "vehicle_id": str(vehicle.id),
            "vehicle_number": vehicle.vehicle_number,
            "status": vehicle.status,
            "latitude": vehicle.current_latitude,
            "longitude": vehicle.current_longitude
        }
    }
    await manager.broadcast(event_payload)
    
    return {"success": True, "message": "GPS coordinates updated successfully."}

@router.get("/vehicles")
async def get_tracking_vehicles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve current coordinates of all online/idle vehicles."""
    result = await db.execute(select(Vehicle).filter(Vehicle.status.in_(["online", "idle", "active"])))
    vehicles = result.scalars().all()
    return [
        {
            "id": str(v.id),
            "vehicle_number": v.vehicle_number,
            "status": v.status,
            "latitude": v.current_latitude,
            "longitude": v.current_longitude
        }
        for v in vehicles
    ]
