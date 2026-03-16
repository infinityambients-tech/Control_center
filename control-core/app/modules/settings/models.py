from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, func

from app.core.db import Base


class AppSetting(Base):
    __tablename__ = "app_settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

