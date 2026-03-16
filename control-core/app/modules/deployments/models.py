from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from uuid import uuid4

from app.core.db import Base

class DeploymentStatus(str, enum.Enum):
    queued = "queued"
    building = "building"
    deployed = "deployed"
    failed = "failed"
    rolled_back = "rolled_back"

class EnvironmentType(str, enum.Enum):
    development = "development"
    staging = "staging"
    production = "production"

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    environment = Column(SQLEnum(EnvironmentType), default=EnvironmentType.development)
    version = Column(String, nullable=True)
    commit_hash = Column(String, nullable=True)
    status = Column(SQLEnum(DeploymentStatus), default=DeploymentStatus.queued)
    logs = Column(Text, nullable=True)
    
    deployed_by = Column(String, nullable=True)  # User ID
    deployed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", backref="deployments")
