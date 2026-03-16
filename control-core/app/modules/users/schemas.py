from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.modules.auth.models import UserRole, UserStatus
from uuid import UUID


class UserAdminListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    is_company: bool
    is_active: bool
    created_at: datetime


class UserAdminUpdate(BaseModel):
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_active: Optional[bool] = None
