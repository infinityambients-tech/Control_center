from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, func

from app.core.db import Base


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(String, primary_key=True, index=True)
    level = Column(String, nullable=False, default="INFO")
    message = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

