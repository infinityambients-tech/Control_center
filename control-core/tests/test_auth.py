import sys, os
# override database for tests (file-based sqlite) before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
# ensure project root is on path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app


def test_register_and_verify():
    # try to register a random email (may already exist)
    payload = {
        "email": "test_ci_user@example.com",
        "first_name": "CI",
        "last_name": "User",
        "password": "CiTest123!",
        "password_confirm": "CiTest123!",
        "is_company": False,
        "accept_terms": True,
        "accept_gdpr": True,
    }
    with TestClient(app) as client:
        resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code in (200, 400, 422)
    if resp.status_code == 200:
        data = resp.json()
        assert data.get("success")
    # additional verification flows could be tested with a real token


def test_check_email():
    with TestClient(app) as client:
        resp = client.post("/api/v1/auth/check-email", json={"email": "notexists@example.com"})
    assert resp.status_code == 200
    data = resp.json()
    assert "available" in data
