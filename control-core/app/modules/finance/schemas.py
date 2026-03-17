from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PaymentSnapshotBase(BaseModel):
    project_id: str
    external_payment_id: str
    amount: float
    currency: str
    status: str

class PaymentSnapshotCreate(PaymentSnapshotBase):
    pass

class PaymentSnapshot(PaymentSnapshotBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FinanceSummary(BaseModel):
    total_revenue: float
    mrr: float
    mrr_growth: float
    churn_rate: float
    ltv: float
