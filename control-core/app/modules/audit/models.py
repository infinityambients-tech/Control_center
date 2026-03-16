from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # user_id must match users.id type (UUID) so the FK can be enforced
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    entity = Column(String)  # e.g., "Project", "Payment"
    entity_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    metadata_json = Column(JSON)  # Renamed from metadata to avoid conflict with SQLAlchemy metadata
