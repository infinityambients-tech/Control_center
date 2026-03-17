from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: Optional[str] = None
    updated_at: datetime
    created_at: datetime


class SettingUpsert(BaseModel):
    value: Optional[str] = None

