from __future__ import annotations

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, Enum as SQLEnum, ForeignKey, String, func
from sqlalchemy.orm import relationship
import enum

from app.core.db import Base


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    cancelled = "cancelled"
    expired = "expired"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()), index=True)
    company_id = Column(String, ForeignKey("company_details.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_id = Column(String, ForeignKey("plans.id", ondelete="SET NULL"), nullable=True)
    status = Column(SQLEnum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.active, index=True)
    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    company = relationship("CompanyDetails", foreign_keys=[company_id])
    plan = relationship("Plan", foreign_keys=[plan_id])

