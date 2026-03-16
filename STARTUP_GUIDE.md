# Control Center - Registration Module Startup Guide

Complete guide to set up and run the Control Center application with the new registration module.

---

## Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **PostgreSQL 12+** (or SQLite for development)
- **Redis 6+** (for Celery task queue)

---

## Project Structure

```
Control_center/
├── control-core/          # FastAPI Backend
│   ├── app/
│   │   ├── modules/
│   │   │   ├── auth/      # Authentication & Registration
│   │   │   ├── projects/
│   │   │   ├── analytics/
│   │   │   ├── finance/
│   │   │   └── ...
│   │   ├── core/          # Configuration & Database
│   │   ├── workers/       # Celery Tasks
│   │   └── main.py        # App Entry Point
│   ├── requirements.txt
│   └── .env               # Environment variables
├── src/                   # React Frontend
│   ├── modules/
│   │   ├── auth/          # Registration & Login
│   │   ├── portfolio/
│   │   └── ...
│   ├── services/          # API Services
│   ├── styles/            # CSS Files
│   └── main.tsx           # Entry Point
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## Part 1: Backend Setup

### Step 1.1: Navigate to Backend Directory

```bash
cd c:\Users\igorz\Desktop\Control_center\control-core
```

### Step 1.2: Create Python Virtual Environment

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 1.3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Output should show:**
```
Successfully installed fastapi, uvicorn, sqlalchemy, pydantic, 
python-jose, passlib, psycopg2-binary, jinja2, and other packages...
```

### Step 1.4: Create `.env` File

Create a file named `.env` in the `control-core` directory with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/control_core
# OR for SQLite (development only)
# DATABASE_URL=sqlite:///./control_core.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-12345abcde
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Email Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use app password, not account password
EMAIL_FROM=noreply@control-center.pl

# Frontend URL (for email verification links)
FRONTEND_URL=http://localhost:5173

# Verification Settings
VERIFICATION_TOKEN_EXPIRE_HOURS=24

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Project Settings
PROJECT_NAME=Control Core API
VERSION=1.0.0
```

**Important Security Notes:**
- **NEVER** commit `.env` file to git
- Use strong `SECRET_KEY` (minimum 32 characters)
- For Gmail: Enable 2FA and generate app-specific password
- Use environment variables for production secrets

### Step 1.5: Initialize Database

**Option A: Using PostgreSQL (Recommended)**

```bash
# Create database manually first
# psql -U postgres -h localhost -c "CREATE DATABASE control_core;"

# Then run migrations (if using Alembic)
alembic upgrade head
```

**Option B: Using SQLite (Development Only)**

Database will be created automatically on first run.

### Step 1.6: Start Backend Server

```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Access points:**
- API: http://localhost:8000/api/v1
- API Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

### Step 1.7: Verify Backend Health

```bash
curl http://localhost:8000/health
# Response: {"status":"healthy"}
```

---

## Part 2: Frontend Setup

### Step 2.1: Navigate to Frontend Directory

```bash
cd c:\Users\igorz\Desktop\Control_center
```

### Step 2.2: Install Dependencies

```bash
npm install
```

**Expected output:**
```
added XXX packages in X.XXs
```

### Step 2.3: Create `.env` File (Optional)

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_FRONTEND_URL=http://localhost:5173
```

### Step 2.4: Start Frontend Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  build X.XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

### Step 2.5: Access Frontend

Open your browser and navigate to:
- **Application**: http://localhost:5173
- **Registration**: http://localhost:5173/register

---

## Part 3: Testing the Registration Flow

### Test 1: Private Account Registration

1. Go to http://localhost:5173/register
2. Click "Private Account"
3. Fill in the form:
   - Name: John Doe
   - Email: john@example.com
   - Password: SecurePass123!
   - Address: 123 Main St, 00-001, Warsaw, PL
   - Accept terms and GDPR
4. Click "Create Account"
5. **Expected:** Email verification page with success message

### Test 2: Check Email Verification

**Backend Console Output:**
```
[EMAIL] To: john@example.com, Subject: Verify Your Email - Control Center
(Email would be sent if SMTP is configured)
```

### Test 3: Company Account Registration

1. Go to http://localhost:5173/register
2. Click "Company Account"
3. Fill in:
   - Personal Info: Same as above
   - Company Name: ABC Corporation
   - NIP: 1234567890 (must pass checksum validation)
   - Company Address: 456 Business Ave
   - Contact Person: John Owner
4. Click "Create Account"
5. **Expected:** Company pending verification message

### Test 4: Database Verification

Check if data was saved in database:

```bash
# Option A: PostgreSQL Client
psql -U postgres -d control_core -c "SELECT id, email, status, is_company FROM users;"

# Option B: SQLite
sqlite3 control_core.db "SELECT id, email, status, is_company FROM users;"
```

---

## Troubleshooting

### Issue: Database Connection Error

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check if PostgreSQL is running: `pg_isready`
2. Verify DATABASE_URL in `.env`
3. Create database: `createdb control_core`
4. Or use SQLite: `DATABASE_URL=sqlite:///./control_core.db`

### Issue: SMTP Email Error

**Error:** `smtplib.SMTPAuthenticationError`

**Solutions:**
1. For Gmail: Use app-specific password (not account password)
2. Enable "Less secure app access" (if using regular password)
3. Check SMTP_USER and SMTP_PASSWORD in `.env`
4. Verify SMTP_SERVER and SMTP_PORT are correct

### Issue: Frontend Cannot Connect to Backend

**Error:** `Failed to fetch http://localhost:8000/api/v1/...`

**Solutions:**
1. Ensure backend is running on port 8000
2. Check CORS settings in `app/main.py`
3. Verify `VITE_API_BASE_URL` environment variable
4. Check browser Console for CORS errors

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solutions:**

For Backend (port 8000):
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows, replace PID)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

For Frontend (port 5173):
```bash
# Find process using port 5173
netstat -ano | findstr :5173

# Kill process
taskkill /PID <PID> /F

# Or use different port (Vite will suggest automatically)
```

### Issue: Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
1. Activate virtual environment
2. Re-install requirements: `pip install -r requirements.txt`
3. Ensure you're in `control-core` directory

### Issue: TypeScript/React Compilation Errors

**Error:** `Cannot find module` in frontend

**Solution:**
1. Clear `node_modules`: `rm -r node_modules package-lock.json`
2. Reinstall: `npm install`
3. Start dev server: `npm run dev`

---

## Usage Guide

### Registration Endpoints (Backend)

**POST** `/api/v1/auth/register`
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "street": "123 Main St",
    "postal_code": "00-001",
    "city": "Warsaw",
    "country": "PL",
    "is_company": false,
    "accept_terms": true,
    "accept_gdpr": true
  }'
```

**POST** `/api/v1/auth/verify-email`
```bash
curl -X POST http://localhost:8000/api/v1/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"token": "uuid-token-here"}'
```

**POST** `/api/v1/auth/check-email`
```bash
curl -X POST http://localhost:8000/api/v1/auth/check-email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

---

## Development Workflow

### Backend Development

```bash
# Terminal 1: Start backend
cd control-core
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Run Celery (optional for tasks)
celery -A app.workers.celery_app worker --loglevel=info
```

### Frontend Development

```bash
# Terminal 3: Start frontend
npm run dev
```

### Making Changes

- **Backend**: Changes in `app/modules/auth/` auto-reload with `--reload`
- **Frontend**: Changes in `src/` hot-reload via Vite
- **Database**: Migrations via Alembic (when needed)

---

## Production Deployment

### Backend (Production Settings)

```env
# Update .env
DEBUG=false
ALLOWED_HOSTS=["yourdomain.com", "www.yourdomain.com"]
CORS_ORIGINS=["https://yourdomain.com"]
DATABASE_URL=postgresql://user:password@prod-db.com/control_core
SECRET_KEY=<strong-random-key-here>
```

Start with Gunicorn:
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Frontend (Production Build)

```bash
npm run build
# Generated in dist/ folder
```

Deploy with:
- Vercel, Netlify, GitHub Pages
- Or static hosting (S3, CloudFront, etc.)

---

## Admin Panel

To verify companies as admin:

**GET** `/api/v1/admin/companies/pending`
- Requires admin authentication
- Returns list of pending company verifications

**POST** `/api/v1/admin/companies/{user_id}/verify`
```bash
curl -X POST http://localhost:8000/api/v1/admin/companies/user-id-here/verify \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"approved": true, "reason": null}'
```

---

## Next Steps

1. **Email Service Integration**: Configure real SMTP provider (SendGrid, AWS SES, etc.)
2. **Rate Limiting**: Add rate limiting to registration endpoint
3. **CAPTCHA**: Add reCAPTCHA v3 to prevent abuse
4. **2FA Setup**: Configure TOTP-based two-factor authentication
5. **Testing**: Run automated tests for all endpoints
6. **Monitoring**: Set up logging and error tracking (Sentry)
7. **SSL/TLS**: Deploy with HTTPS in production

---

## Support

For issues or questions:
- Check logs in backend console
- Check browser DevTools Console (F12) for frontend errors
- Review [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for architecture details
- GitHub Issues: [if using version control]

---

## Security Checklist

- [ ] SECRET_KEY is strong (32+ characters)
- [ ] SMTP credentials are app-specific passwords
- [ ] DATABASE_URL doesn't use default credentials
- [ ] CORS is restricted to your domain
- [ ] HTTPS enabled in production
- [ ] Environment variables stored securely
- [ ] Input validation enabled on all endpoints
- [ ] Rate limiting configured
- [ ] Database backups scheduled
- [ ] Error logs don't expose sensitive data

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m venv venv` | Create Python environment |
| `.\venv\Scripts\Activate.ps1` | Activate environment (Windows) |
| `source venv/bin/activate` | Activate environment (Linux/macOS) |
| `pip install -r requirements.txt` | Install dependencies |
| `python -m uvicorn app.main:app --reload` | Start backend |
| `npm install` | Install frontend dependencies |
| `npm run dev` | Start frontend dev server |
| `npm run build` | Build frontend for production |
| `alembic upgrade head` | Run database migrations |
| `curl http://localhost:8000/health` | Check backend health |

---

**Last Updated**: March 2026
**Version**: 1.0.0 - Registration Module
