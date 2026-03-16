from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    type: str
    title: str
    message: Optional[str] = None
    metadata_json: Optional[dict[str, Any]] = None
    read_at: Optional[datetime] = None
    created_at: datetime

