from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    company_id: str
    plan_id: Optional[str] = None
    currency: str = "PLN"
    net_amount: float = Field(..., ge=0)
    vat_rate: float = Field(23.0, ge=0, le=100)
    issue_date: date = Field(default_factory=date.today)
    due_date: Optional[date] = None
    notes: Optional[str] = None


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    invoice_number: str
    company_id: Optional[str] = None
    plan_id: Optional[str] = None
    currency: str
    net_amount: float
    vat_rate: float
    vat_amount: float
    gross_amount: float
    issue_date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None
    pdf_path: Optional[str] = None
    created_at: datetime

