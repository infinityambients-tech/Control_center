from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MetricBase(BaseModel):
    date: datetime
    mrr: float
    arr: float
    active_subscriptions: int
    failed_payments: int
    revenue_today: float

class Metric(MetricBase):
    id: int
    project_id: str

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    type: Optional[str] = None
    api_base_url: Optional[str] = None
    payment_provider: Optional[str] = None
    status: Optional[str] = "active"

class ProjectCreate(ProjectBase):
    api_key: Optional[str] = None

class ProjectUpdate(ProjectBase):
    api_key: Optional[str] = None

class Project(ProjectBase):
    id: str
    created_at: datetime
    metrics: List[Metric] = []

    class Config:
        from_attributes = True
