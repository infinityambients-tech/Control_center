from __future__ import annotations

from datetime import datetime, date

from sqlalchemy import Column, Date, DateTime, Numeric, String, Text, func, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False, index=True)
    company_id = Column(String, ForeignKey("company_details.id", ondelete="SET NULL"), nullable=True, index=True)
    plan_id = Column(String, ForeignKey("plans.id", ondelete="SET NULL"), nullable=True)
    currency = Column(String, nullable=False, default="PLN")
    net_amount = Column(Numeric(10, 2), nullable=False, default=0)
    vat_rate = Column(Numeric(5, 2), nullable=False, default=23)
    vat_amount = Column(Numeric(10, 2), nullable=False, default=0)
    gross_amount = Column(Numeric(10, 2), nullable=False, default=0)
    issue_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    company = relationship("CompanyDetails", foreign_keys=[company_id])
    plan = relationship("Plan", foreign_keys=[plan_id])

