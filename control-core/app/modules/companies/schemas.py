from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyBase(BaseModel):
    company_name: str = Field(..., min_length=2)
    nip: str = Field(..., min_length=5)
    regon: Optional[str] = None
    krs: Optional[str] = None
    company_address: str
    company_postal_code: Optional[str] = None
    company_city: Optional[str] = None
    company_country: Optional[str] = None
    contact_person: str
    company_phone: Optional[str] = None
    company_email: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    regon: Optional[str] = None
    krs: Optional[str] = None
    company_address: Optional[str] = None
    company_postal_code: Optional[str] = None
    company_city: Optional[str] = None
    company_country: Optional[str] = None
    contact_person: Optional[str] = None
    company_phone: Optional[str] = None
    company_email: Optional[str] = None


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    plan_id: Optional[str] = None
    company_verified: bool
    verification_status: str
    rejected_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SetCompanyPlanRequest(BaseModel):
    plan_id: Optional[str] = None


class CompanyListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    company_name: str
    nip: str
    verification_status: str
    plan_id: Optional[str] = None
    created_at: datetime

