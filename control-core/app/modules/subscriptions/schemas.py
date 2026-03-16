from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.modules.subscriptions.models import SubscriptionStatus

class SubscriptionSnapshotBase(BaseModel):
    project_id: str
    external_id: str
    plan: str
    status: str
    current_period_end: datetime

class SubscriptionSnapshotCreate(SubscriptionSnapshotBase):
    pass

class SubscriptionSnapshot(SubscriptionSnapshotBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SubscriptionSummary(BaseModel):
    total_active: int
    plans_distribution: dict # Plan name -> Count
    churned_count: int


class SubscriptionCreate(BaseModel):
    company_id: str
    plan_id: Optional[str] = None
    status: SubscriptionStatus = SubscriptionStatus.active
    start_date: date = Field(default_factory=date.today)
    end_date: Optional[date] = None


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    plan_id: Optional[str] = None
    status: SubscriptionStatus
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime
