# Instalacja (Windows/macOS)

## Backend (FastAPI)
1. Przejdź do `control-core/`
2. Zainstaluj zależności: `pip install -r requirements.txt`
3. Skonfiguruj `DATABASE_URL`:
   - szybki start (SQLite): `sqlite:///./control_core.db`
   - produkcja (PostgreSQL): `postgresql://user:pass@host/dbname`
4. Uruchom: `uvicorn app.main:app --reload --port 8000`

## Desktop GUI (PySide6)
1. Przejdź do `desktop-qt/`
2. Zainstaluj zależności: `pip install -r requirements.txt`
3. Uruchom: `python main.py`
4. W oknie logowania ustaw `API URL` (domyślnie `http://127.0.0.1:8000`).

