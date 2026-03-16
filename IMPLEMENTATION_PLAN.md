# Control Center - Registration Module Implementation Plan

## Project Analysis

### Frontend Stack
- **Framework**: React 19.2.0 with TypeScript
- **Bundler**: Vite
- **Desktop**: Electron 40.6.0
- **Routing**: React Router v7.13.0
- **UI Icons**: Lucide React
- **Architecture**: Modular with src/modules structure

### Backend Stack
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL (with SQLite fallback for dev)
- **Authentication**: JWT (python-jose) + bcrypt (passlib)
- **Task Queue**: Celery + Redis
- **Architecture**: Modular with app/modules structure

### Current State
- ✅ Basic login/authentication endpoints exist
- ✅ User model exists but needs enhancement
- ❌ Company details table missing
- ❌ Email verification not implemented
- ❌ Account statuses not implemented
- ❌ Registration endpoint missing
- ❌ Registration UI missing

---

## Implementation Phases

### Phase 1: Database Schema Update
**Status**: TODO
**Files to modify/create**:
- `control-core/app/modules/auth/models.py` - Enhance User model
- `control-core/app/modules/auth/models.py` - Create CompanyDetails model

**Changes**:
1. Update User table:
   - Add: `first_name`, `last_name`, `phone`, `street`, `postal_code`, `city`, `country`
   - Add: `role` (enum: admin/manager/client) - default: client
   - Add: `status` (enum: pending_email/pending_company/active/suspended/rejected)
   - Add: `email_verified` (bool) - default: False
   - Add: `is_company` (bool) - default: False
   - Rename: `full_name` → `first_name` + `last_name`

2. Create CompanyDetails table:
   - `id` (UUID PK)
   - `user_id` (FK User)
   - `company_name` (string)
   - `nip` (string, unique)
   - `regon` (string)
   - `krs` (string, optional)
   - `company_address`, `company_city`, `company_country`
   - `contact_person`, `company_verified` (bool)
   - `document_path` (for verification document)

### Phase 2: Authentication Schemas & Utilities
**Status**: TODO
**Files to create**:
- `control-core/app/modules/auth/validators.py` - Validation utilities
- `control-core/app/modules/auth/emails.py` - Email service

**Validators**:
- Email format & duplicate check
- Password strength (min 8 chars, 1 uppercase, 1 digit, 1 special char)
- NIP validation (10 digits + checksum algorithm)
- Document upload validation (PDF/JPG/PNG, max 5MB)

### Phase 3: Backend Registration Endpoints
**Status**: TODO
**File**: `control-core/app/modules/auth/router.py`
**Endpoints**:
1. `POST /api/v1/auth/register` - Create account (private or company)
2. `POST /api/v1/auth/verify-email` - Email verification
3. `POST /api/v1/auth/resend-verification` - Resend verification email
4. `GET /api/v1/auth/verify-email/{token}` - Click link from email

**Process**:
- Validate all inputs
- Hash password with bcrypt
- Create User (status=pending_email)
- Store verification token (UUID with 24h expiry)
- Send email with verification link
- Return: {success: true, status: pending_email, message: "..."}

### Phase 4: Admin Company Verification Endpoints
**Status**: TODO
**File**: `control-core/app/modules/admin/router.py` (new)
**Endpoints**:
1. `GET /api/v1/admin/companies/pending` - List pending companies
2. `POST /api/v1/admin/companies/{user_id}/verify` - Approve company
3. `POST /api/v1/admin/companies/{user_id}/reject` - Reject company

### Phase 5: Frontend Registration Component
**Status**: TODO
**Files to create**:
- `src/modules/auth/Register.tsx` - Main registration form
- `src/modules/auth/EmailVerification.tsx` - Email verification page
- `src/components/RegisterForm.tsx` - Form component
- `src/services/registrationService.ts` - API calls

**Features**:
- Two-step form (toggle: private/company)
- Client-side validation with regex
- Async email check
- Password strength indicator
- Conditional company fields
- File upload widget
- Success/Error messages
- Loading states

### Phase 6: Email Service
**Status**: TODO
**File**: `control-core/app/modules/auth/emails.py`
**Services**:
- Email template rendering
- Send verification email (can use: SendGrid, AWS SES, or SMTP)

---

## Database Schema Details

### users table (MODIFIED)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    phone VARCHAR,
    street VARCHAR,
    postal_code VARCHAR,
    city VARCHAR,
    country VARCHAR,
    role VARCHAR CHECK (role IN ('admin', 'manager', 'client')) DEFAULT 'client',
    status VARCHAR CHECK (status IN ('pending_email', 'pending_company', 'active', 'suspended', 'rejected')) DEFAULT 'pending_email',
    email_verified BOOLEAN DEFAULT FALSE,
    is_company BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### company_details table (NEW)
```sql
CREATE TABLE company_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR NOT NULL,
    nip VARCHAR UNIQUE NOT NULL,
    regon VARCHAR,
    krs VARCHAR,
    company_address VARCHAR NOT NULL,
    company_postal_code VARCHAR,
    company_city VARCHAR,
    company_country VARCHAR,
    contact_person VARCHAR NOT NULL,
    company_phone VARCHAR,
    company_email VARCHAR,
    document_path VARCHAR,
    company_verified BOOLEAN DEFAULT FALSE,
    verification_status VARCHAR DEFAULT 'pending',
    rejected_reason VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### email_tokens table (NEW)
```sql
CREATE TABLE email_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints Summary

### Registration & Verification
| Method | Endpoint | Body | Response | Auth |
|--------|----------|------|----------|------|
| POST | `/api/v1/auth/register` | RegisterRequest | {success, status, message} | No |
| POST | `/api/v1/auth/verify-email` | {token} | {success, status} | No |
| GET | `/api/v1/auth/verify-email/{token}` | - | Redirect to app | No |
| POST | `/api/v1/auth/resend-verification` | {email} | {success, message} | No |

### Admin Management
| Method | Endpoint | Body | Response | Auth |
|--------|----------|------|----------|------|
| GET | `/api/v1/admin/companies/pending` | Filter/Pagination | PaginatedList | Yes (Admin) |
| POST | `/api/v1/admin/companies/{id}/verify` | {approved: true} | {success, status} | Yes (Admin) |
| POST | `/api/v1/admin/companies/{id}/reject` | {reason: string} | {success, status} | Yes (Admin) |

---

## Frontend Validation Rules

### Email
- Format: RFC 5322 regex
- Async check: `POST /api/v1/auth/check-email?email=...` (prevent duplicates in real-time)

### Password (Client-side display only, server-side REQUIRED)
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 digit (0-9)
- At least 1 special character (!@#$%^&*)

### NIP (Poland only for demo)
- 10 digits only
- Checksum validation (luhn-like algorithm)
- Format: XXXXXXXXXX or XX-XXX-XXX-XXX

### Document Upload
- Allowed: PDF, JPG, PNG
- Max size: 5 MB
- Preview before upload

---

## Environment Variables Required

### Backend (.env)
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/control_core
REDIS_URL=redis://localhost:6379/0
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FRONTEND_URL=http://localhost:5173
EMAIL_FROM=noreply@control-center.pl
VERIFICATION_TOKEN_EXPIRE_HOURS=24
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_FRONTEND_URL=http://localhost:5173
```

---

## Startup Instructions

### Backend
```bash
cd control-core
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
npm install
npm run dev  # Vite dev server on http://localhost:5173
```

### Database Migration
```bash
# Create migrations
alembic revision --autogenerate -m "Add registration schema"

# Apply migrations
alembic upgrade head
```

---

## Testing Checklist

- [ ] Private account registration + email verification
- [ ] Company account registration (all fields)
- [ ] Email validation (duplicate check)
- [ ] Password strength validation
- [ ] NIP validation
- [ ] Document upload (5MB limit)
- [ ] Email verification token expiry
- [ ] Company approval flow
- [ ] Status transitions
- [ ] Login after registration
- [ ] Rate limiting on registration
- [ ] CAPTCHA (optional enhancement)

---

## Security Considerations

1. **Password Hashing**: bcrypt with salt (already configured)
2. **Email Tokens**: UUID + 24h expiry + single-use
3. **CORS**: Configure for production (currently `["*"]`)
4. **Rate Limiting**: Add on registration endpoint
5. **Validation**: Server-side + client-side
6. **HTTPS**: Required in production
7. **SQL Injection**: SQLAlchemy ORM prevents it
8. **CSRF**: Added by default in FastAPI
9. **File Upload**: Validate type + size server-side
10. **2FA**: Prepare infrastructure (TOTP optional)

---

## Timeline Estimate
- Database Schema: 1 hour
- Backend Endpoints: 3 hours
- Email Service: 1 hour
- Frontend Components: 3 hours
- Testing & QA: 2 hours
**Total**: ~10 hours

---

## Next Steps
1. Execute Phase 1: Database schema update
2. Execute Phase 2: Validation utilities
3. Execute Phase 3: Backend endpoints
4. Execute Phase 4: Admin endpoints
5. Execute Phase 5: Frontend components
6. Test end-to-end flow
7. Deploy & document
