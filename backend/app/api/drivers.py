from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict
from backend.app.database.session import get_db
from backend.app.models import Driver
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("")
async def get_drivers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all driver profiles."""
    result = await db.execute(select(Driver))
    drivers = result.scalars().all()
    return [
        {
            "id": str(d.id),
            "employee_id": d.employee_id,
            "name": d.name,
            "phone": d.phone,
            "license_number": d.license_number,
            "experience": d.experience,
            "rating": d.rating,
            "status": d.status,
            "current_vehicle": d.current_vehicle
        }
        for d in drivers
    ]

@router.get("/{driver_id}")
async def get_driver_details(
    driver_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import uuid
    try:
        driver_uuid = uuid.UUID(driver_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid driver ID format")
        
    result = await db.execute(select(Driver).filter_by(id=driver_uuid))
    driver = result.scalars().first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        
    return {
        "id": str(driver.id),
        "employee_id": driver.employee_id,
        "name": driver.name,
        "phone": driver.phone,
        "license_number": driver.license_number,
        "experience": driver.experience,
        "rating": driver.rating,
        "status": driver.status,
        "current_vehicle": driver.current_vehicle,
        "hub_id": str(driver.hub_id) if driver.hub_id else None
    }
