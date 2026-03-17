from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# ============== Base Schemas ==============

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class CompanyDetailsBase(BaseModel):
    company_name: str
    nip: str
    regon: Optional[str] = None
    krs: Optional[str] = None
    company_address: str
    company_postal_code: Optional[str] = None
    company_city: Optional[str] = None
    company_country: Optional[str] = None
    contact_person: str
    company_phone: Optional[str] = None
    company_email: Optional[str] = None

# ============== Registration Schemas ==============

class UserRegister(UserBase):
    password: str = Field(..., min_length=8)
    password_confirm: str
    is_company: bool = False
    company_details: Optional[CompanyDetailsBase] = None
    accept_terms: bool
    accept_gdpr: bool

class CompanyDetailsCreate(CompanyDetailsBase):
    document_path: Optional[str] = None

# ============== Response Schemas ==============

class CompanyDetailsResponse(CompanyDetailsBase):
    id: UUID
    company_verified: bool
    verification_status: str
    rejected_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: UUID
    role: str
    status: str
    email_verified: bool
    is_company: bool
    is_active: bool
    is_superuser: bool
    company_details: Optional[CompanyDetailsResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============== Auth Schemas ==============

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: Optional[UserResponse] = None

class LoginResponse(BaseModel):
    """Response for cookie-based login (tokens in HttpOnly cookies, not in body)."""
    token_type: str
    user: UserResponse
    message: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    id: Optional[str] = None

# ============== Email Verification Schemas ==============

class EmailVerifyRequest(BaseModel):
    token: str

class EmailVerifyResponse(BaseModel):
    success: bool
    message: str
    status: Optional[str] = None

class EmailResendRequest(BaseModel):
    email: EmailStr

# ============== Registration Response Schemas ==============

class RegisterResponse(BaseModel):
    success: bool
    message: str
    status: str
    user_id: Optional[UUID] = None

class CheckEmailRequest(BaseModel):
    email: EmailStr

class CheckEmailResponse(BaseModel):
    available: bool
    message: str

# ============== Admin Company Verification Schemas ==============

class CompanyPendingResponse(BaseModel):
    id: UUID
    user_id: UUID
    user_email: str
    user_name: str
    company_name: str
    nip: str
    document_path: Optional[str] = None
    created_at: datetime
    status: str

class CompanyVerifyRequest(BaseModel):
    approved: bool
    reason: Optional[str] = None

class CompanyVerifyResponse(BaseModel):
    success: bool
    message: str
    new_status: str
