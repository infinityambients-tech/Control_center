# Control Center

Control Center to desktopowa aplikacja (Windows/macOS) do zarządzania projektami developerskimi, klientami (firmami), planami/subskrypcjami, deploymentami, fakturami, ustawieniami i logami.

W tym repo znajdują się:
- `control-core/` — backend API (FastAPI + SQLAlchemy; PostgreSQL/SQLite; opcjonalnie Redis)
- `desktop-qt/` — desktop GUI (PySide6, ciemny motyw, zakładki)
- `build/desktop/` — skrypty budowania `.exe` / `.app` (PyInstaller)

## Moduły backendu (MVP)
- `auth/` (JWT, role: `admin/developer/client` + kompatybilne `manager`)
- `users/`, `companies/`, `projects/`, `plans/`, `subscriptions/`, `deployments/`
- `invoices/` (numeracja + best-effort PDF przez `reportlab`)
- `settings/` (klucze w DB), `logs/`, `audit/`, `notifications/`, `backup/`, `updates/`
- `plugins/` (ładowanie pluginów `register(app)` z `control-core/plugins/*.py`)

## Szybki start (lokalnie)

1) Backend

```powershell
cd control-core
.\.venv\Scripts\python -m pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./control_core.db"
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

2) Desktop (PySide6)

```powershell
cd desktop-qt
python -m pip install -r requirements.txt
python main.py
```

Więcej: `docs/INSTALL.md`, `docs/BUILD.md`, `docs/UPDATES.md`.
