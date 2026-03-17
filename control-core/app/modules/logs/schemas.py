from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SystemLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    level: str
    message: str
    context: Optional[str] = None
    created_at: datetime

