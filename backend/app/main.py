import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from backend.app.core.config import settings
from backend.app.database.migrations import init_db

# Import routers
from backend.app.api.auth import router as auth_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.routes import router as routes_router
from backend.app.api.optimization import router as optimization_router
from backend.app.api.tracking import router as tracking_router
from backend.app.api.drivers import router as drivers_router
from backend.app.api.vehicles import router as vehicles_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.notifications import router as notifications_router
from backend.app.api.settings import router as settings_router
from backend.app.api.health import router as health_router
from backend.app.api.websocket import router as ws_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RouteMind Route Optimization & Decision Support REST API",
    version="1.0.0"
)

# Enable CORS for Next.js frontend local server requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup migrations
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up FastAPI application...")
    try:
        await init_db()
    except Exception as e:
        logger.exception("Error running migrations during startup")

# Register API routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(routes_router, prefix=f"{settings.API_V1_STR}/routes", tags=["Routes"])
app.include_router(optimization_router, prefix=f"{settings.API_V1_STR}/optimization", tags=["Optimization"])
app.include_router(tracking_router, prefix=f"{settings.API_V1_STR}/tracking", tags=["Live Tracking"])
app.include_router(drivers_router, prefix=f"{settings.API_V1_STR}/drivers", tags=["Drivers"])
app.include_router(vehicles_router, prefix=f"{settings.API_V1_STR}/vehicles", tags=["Vehicles"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
app.include_router(notifications_router, prefix=f"{settings.API_V1_STR}/notifications", tags=["Notifications"])
app.include_router(settings_router, prefix=f"{settings.API_V1_STR}/settings", tags=["Settings"])
app.include_router(health_router, prefix=f"{settings.API_V1_STR}/health", tags=["Health"])

# Register WebSocket router directly
app.include_router(ws_router)

# Serve Frontend static assets
@app.get("/")
def serve_frontend_dashboard():
    """Serve the index.html page synchronously from frontend folder."""
    index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/index.html"))
    if not os.path.exists(index_path):
        return HTMLResponse(content="<h3>index.html not found</h3>", status_code=404)
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/static/app.js")
def serve_frontend_js():
    """Serve app.js synchronously from frontend folder."""
    js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/app.js"))
    if not os.path.exists(js_path):
        return HTMLResponse(content="<h3>app.js not found</h3>", status_code=404)
    return FileResponse(js_path, media_type="application/javascript")
