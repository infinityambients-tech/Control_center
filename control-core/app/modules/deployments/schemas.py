from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.modules.deployments.models import DeploymentStatus, EnvironmentType

class DeploymentBase(BaseModel):
    environment: EnvironmentType = EnvironmentType.development
    version: Optional[str] = None
    commit_hash: Optional[str] = None

class DeploymentCreate(DeploymentBase):
    project_id: str

class DeploymentUpdate(BaseModel):
    status: Optional[DeploymentStatus] = None
    logs: Optional[str] = None

class DeploymentResponse(DeploymentBase):
    id: str
    project_id: str
    status: DeploymentStatus
    logs: Optional[str] = None
    deployed_by: Optional[str] = None
    deployed_at: datetime

    class Config:
        from_attributes = True
