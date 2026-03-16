from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base
import uuid

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("company_details.id", ondelete="CASCADE"), nullable=True) # Changed from True to True manually as existing db entries might not have this, then can migrate
    subscription_id = Column(String, nullable=True) # Will become a FK when we build subscriptions
    name = Column(String, nullable=False)
    type = Column(String)
    api_base_url = Column(String)
    api_key_encrypted = Column(String)
    payment_provider = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    metrics = relationship("ProjectMetric", back_populates="project", cascade="all, delete-orphan")

class ProjectMetric(Base):
    __tablename__ = "project_metrics"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    date = Column(DateTime, default=datetime.utcnow)
    mrr = Column(Float, default=0.0)
    arr = Column(Float, default=0.0)
    active_subscriptions = Column(Integer, default=0)
    failed_payments = Column(Integer, default=0)
    revenue_today = Column(Float, default=0.0)

    project = relationship("Project", back_populates="metrics")

class SubscriptionSnapshot(Base):
    __tablename__ = "subscription_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    external_id = Column(String)
    plan = Column(String)
    status = Column(String)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project")

class PaymentSnapshot(Base):
    __tablename__ = "payment_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"))
    external_payment_id = Column(String)
    amount = Column(Float)
    currency = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project")
