from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import uuid

class AuditLogBase(BaseModel):
    action: str
    entity: Optional[str] = None
    entity_id: Optional[str] = None
    ip_address: Optional[str] = None
    metadata_json: Optional[Any] = None

class AuditLogCreate(AuditLogBase):
    user_id: Optional[uuid.UUID] = None

class AuditLog(AuditLogBase):
    id: uuid.UUID
    user_id: Optional[uuid.UUID]
    timestamp: datetime

    class Config:
        from_attributes = True
