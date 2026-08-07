from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.database.session import get_db
from backend.app.models import Notification
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()

@router.get("")
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve notifications for the current user."""
    result = await db.execute(select(Notification).filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()))
    notifications = result.scalars().all()
    
    # Fallback to general notifications if none are found for specific user (e.g. system alerts)
    if not notifications:
        result = await db.execute(select(Notification).filter_by(user_id=None).order_by(Notification.created_at.desc()))
        notifications = result.scalars().all()
        
    return [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "priority": n.priority,
            "is_read": n.is_read,
            "created_at": str(n.created_at)
        }
        for n in notifications
    ]

@router.put("/read")
async def mark_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read."""
    result = await db.execute(select(Notification).filter_by(user_id=current_user.id, is_read=False))
    notifications = result.scalars().all()
    for n in notifications:
        n.is_read = True
    await db.commit()
    return {"success": True, "message": "All notifications marked as read."}
