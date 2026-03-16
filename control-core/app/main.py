from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from starlette.responses import FileResponse
import os
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.projects.router import router as projects_router
from app.modules.analytics.router import router as analytics_router
from app.modules.finance.router import router as finance_router
from app.modules.subscriptions.router import router as subscriptions_router
from app.modules.audit.router import router as audit_router
from app.modules.plans.router import router as plans_router
from app.modules.deployments.router import router as deployments_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.companies.router import router as companies_router
from app.modules.users.router import router as users_router
from app.modules.invoices.router import router as invoices_router
from app.modules.settings.router import router as settings_router
from app.modules.logs.router import router as logs_router
from app.modules.updates.router import router as updates_router
from app.modules.notifications.router import router as notifications_router
from app.modules.backup.router import router as backup_router
from app.core.db import engine, Base
from app.core.plugins import load_plugins
from jose import jwt, JWTError
from app.core.config import settings as core_settings
import asyncio
from app.modules.auth import models as auth_models
from app.modules.projects import models as projects_models
from app.modules.audit import models as audit_models
from app.modules.plans import models as plans_models
from app.modules.deployments import models as deployments_models
from app.modules.subscriptions import models as subscriptions_models
from app.modules.settings import models as settings_models
from app.modules.logs import models as logs_models
from app.modules.invoices import models as invoices_models
from app.modules.notifications import models as notifications_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure metadata is loaded (imports above) and create tables for dev/test.
    # For production use Alembic migrations.
    Base.metadata.create_all(bind=engine)
    load_plugins(app, Path(__file__).resolve().parents[1] / "plugins")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Centralized Backend for Control Center",
    version=settings.VERSION,
    lifespan=lifespan,
)

# In-memory mapping of user_id -> set of active WebSocket connections
app.state.connections = {}


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    """Simple WebSocket endpoint. Client may provide `token` query param (access token) or rely on HttpOnly cookie `access_token`."""
    await websocket.accept()
    token = websocket.query_params.get('token') or websocket.cookies.get('access_token')
    if not token:
        await websocket.close(code=1008)
        return

    try:
        payload = jwt.decode(token, core_settings.SECRET_KEY, algorithms=[core_settings.ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    # register connection
    conns = app.state.connections.setdefault(str(user_id), set())
    conns.add(websocket)

    try:
        while True:
            # keep the connection alive; echo ping/pong behavior
            msg = await websocket.receive_text()
            # simple ping responder
            if msg == 'ping':
                await websocket.send_text('pong')
    except WebSocketDisconnect:
        # cleanup
        try:
            conns.remove(websocket)
        except Exception:
            pass
    except Exception:
        try:
            conns.remove(websocket)
        except Exception:
            pass

# serve frontend static files
static_dir = os.path.join(os.getcwd(), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    # also check package-relative static folder (when working dir differs)
    pkg_static = os.path.join(os.path.dirname(__file__), "static")
    if os.path.isdir(pkg_static):
        # mount only the assets folder so SPA fallback can return index.html
        assets_dir = os.path.join(pkg_static, "assets")
        if os.path.isdir(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        # expose vite.svg and other top-level static files explicitly
        @app.get("/vite.svg")
        async def vite_svg():
            path = os.path.join(pkg_static, "vite.svg")
            if os.path.exists(path):
                return FileResponse(path, media_type="image/svg+xml")
            raise HTTPException(status_code=404, detail="Not Found")

# Register Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(projects_router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(finance_router, prefix=f"{settings.API_V1_STR}/finance", tags=["finance"])
app.include_router(subscriptions_router, prefix=f"{settings.API_V1_STR}/subscriptions", tags=["subscriptions"])
app.include_router(audit_router, prefix=f"{settings.API_V1_STR}/audit", tags=["audit"])
app.include_router(plans_router, prefix=f"{settings.API_V1_STR}/plans", tags=["plans"])
app.include_router(deployments_router, prefix=f"{settings.API_V1_STR}/deployments", tags=["deployments"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(companies_router, prefix=f"{settings.API_V1_STR}/companies", tags=["companies"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(invoices_router, prefix=f"{settings.API_V1_STR}/invoices", tags=["invoices"])
app.include_router(settings_router, prefix=f"{settings.API_V1_STR}/settings", tags=["settings"])
app.include_router(logs_router, prefix=f"{settings.API_V1_STR}/logs", tags=["logs"])
app.include_router(updates_router, prefix=f"{settings.API_V1_STR}/updates", tags=["updates"])
app.include_router(notifications_router, prefix=f"{settings.API_V1_STR}/notifications", tags=["notifications"])
app.include_router(backup_router, prefix=f"{settings.API_V1_STR}/backup", tags=["backup"])

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Control Core API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# SPA fallback: serve index.html for frontend routes (e.g. /verify-email)
@app.get("/{full_path:path}")
async def spa(full_path: str):
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Not Found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
