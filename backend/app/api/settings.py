from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.api.deps import get_current_user
from backend.app.models.user import User
from backend.app.core.config import settings

router = APIRouter()

class SettingsUpdateRequest(BaseModel):
    ai_provider: str
    routine_model: str
    reasoning_model: str

@router.get("")
async def get_settings(current_user: User = Depends(get_current_user)):
    """Retrieve active system preferences."""
    return {
        "ai_provider": settings.AI_PROVIDER,
        "routine_model": settings.AI_MODEL_ROUTINE,
        "reasoning_model": settings.AI_MODEL_REASONING,
        "app_env": settings.APP_ENV,
        "log_level": settings.LOG_LEVEL,
        "minio_endpoint": settings.MINIO_ENDPOINT
    }

@router.put("")
async def update_settings(
    data: SettingsUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """Update system runtime preferences (changes provider temporarily/persistently in settings object)."""
    settings.AI_PROVIDER = data.ai_provider
    settings.AI_MODEL_ROUTINE = data.routine_model
    settings.AI_MODEL_REASONING = data.reasoning_model
    
    return {
        "success": True,
        "message": "System settings updated successfully.",
        "settings": {
            "ai_provider": settings.AI_PROVIDER,
            "routine_model": settings.AI_MODEL_ROUTINE,
            "reasoning_model": settings.AI_MODEL_REASONING
        }
    }
