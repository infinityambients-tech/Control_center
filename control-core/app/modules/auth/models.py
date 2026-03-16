from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base
import uuid
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    developer = "developer"
    manager = "manager"
    client = "client"

class UserStatus(str, enum.Enum):
    pending_email = "pending_email"
    pending_company = "pending_company"
    active = "active"
    suspended = "suspended"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    street = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.client)
    status = Column(Enum(UserStatus), default=UserStatus.pending_email)
    email_verified = Column(Boolean, default=False)
    is_company = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company_details = relationship("CompanyDetails", back_populates="user", uselist=False)
    email_tokens = relationship("EmailToken", back_populates="user")


class EmailToken(Base):
    __tablename__ = "email_tokens"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="email_tokens")


class CompanyDetails(Base):
    __tablename__ = "company_details"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    company_name = Column(String, nullable=False)
    nip = Column(String, unique=True, nullable=False, index=True)
    regon = Column(String, nullable=True)
    krs = Column(String, nullable=True)
    company_address = Column(String, nullable=False)
    company_postal_code = Column(String, nullable=True)
    company_city = Column(String, nullable=True)
    company_country = Column(String, nullable=True)
    contact_person = Column(String, nullable=False)
    company_phone = Column(String, nullable=True)
    company_email = Column(String, nullable=True)
    document_path = Column(String, nullable=True)
    company_verified = Column(Boolean, default=False)
    verification_status = Column(String, default="pending")
    rejected_reason = Column(Text, nullable=True)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=True)  # Link to Plans
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="company_details")
    plan = relationship("Plan", foreign_keys=[plan_id])
