from sqlalchemy import Column, String, Numeric, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from app.core.db import Base

def generate_uuid():
    return str(uuid4())

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True, nullable=False)
    monthly_price = Column(Numeric(10, 2), nullable=False, default=0)
    yearly_price = Column(Numeric(10, 2), nullable=False, default=0)
    max_projects = Column(Integer, nullable=False, default=1)
    max_users = Column(Integer, nullable=False, default=1)
    max_storage_gb = Column(Integer, nullable=False, default=1)
    max_deployments_per_month = Column(Integer, nullable=False, default=50)
    priority_support = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Optional relationships back to subscriptions or companies if needed later
    # subscriptions = relationship("Subscription", back_populates="plan")
