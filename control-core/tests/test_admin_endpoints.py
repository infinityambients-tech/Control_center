import os
import sys
import pathlib

# ensure project root is on path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from app.core.db import Base, SessionLocal, engine
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.modules.auth.models import User, UserRole, UserStatus


def _auth_headers(user_id: str) -> dict:
    token = create_access_token(user_id)
    return {"Authorization": f"Bearer {token}"}


def test_admin_dashboard_and_users_list():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        admin = User(
            email="admin_test@example.com",
            hashed_password=get_password_hash("Admin123!"),
            first_name="Admin",
            last_name="Test",
            role=UserRole.admin,
            status=UserStatus.active,
            email_verified=True,
            is_company=False,
            is_active=True,
            is_superuser=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        headers = _auth_headers(str(admin.id))

    with TestClient(app) as client:
        resp = client.get("/api/v1/users/", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

        resp = client.get("/api/v1/dashboard/summary", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "projects_count" in data


def test_updates_check_requires_repo_setting():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user = User(
            email="user_test@example.com",
            hashed_password=get_password_hash("User123!"),
            first_name="User",
            last_name="Test",
            role=UserRole.client,
            status=UserStatus.active,
            email_verified=True,
            is_company=False,
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        headers = _auth_headers(str(user.id))

    with TestClient(app) as client:
        resp = client.get("/api/v1/updates/check", headers=headers)
        assert resp.status_code == 400

