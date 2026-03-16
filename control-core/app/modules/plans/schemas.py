from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class PlanBase(BaseModel):
    name: str = Field(..., title="Plan Name", description="Name of the plan (e.g. Free, Pro, Enterprise)")
    monthly_price: float = Field(0.0, title="Monthly Price")
    yearly_price: float = Field(0.0, title="Yearly Price")
    max_projects: int = Field(1, title="Maximum Projects Limit")
    max_users: int = Field(1, title="Maximum Users Limit")
    max_storage_gb: int = Field(1, title="Storage Limit in GB")
    max_deployments_per_month: int = Field(50, title="Maximum Deployments Per Month")
    priority_support: bool = Field(False, title="Priority Support Flag")

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    monthly_price: Optional[float] = None
    yearly_price: Optional[float] = None
    max_projects: Optional[int] = None
    max_users: Optional[int] = None
    max_storage_gb: Optional[int] = None
    max_deployments_per_month: Optional[int] = None
    priority_support: Optional[bool] = None

class PlanResponse(PlanBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

