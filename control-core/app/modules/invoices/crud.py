from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.invoices import models


def _format_invoice_number(today: date, seq: int) -> str:
    return f"INV/{today.year:04d}/{today.month:02d}/{seq:04d}"


def next_invoice_number(db: Session, today: date) -> str:
    prefix = f"INV/{today.year:04d}/{today.month:02d}/"
    latest = (
        db.query(models.Invoice.invoice_number)
        .filter(models.Invoice.invoice_number.like(f"{prefix}%"))
        .order_by(models.Invoice.invoice_number.desc())
        .first()
    )
    if not latest:
        return _format_invoice_number(today, 1)
    last = latest[0].split("/")[-1]
    try:
        last_int = int(last)
    except ValueError:
        last_int = 0
    return _format_invoice_number(today, last_int + 1)


def create_invoice(
    db: Session,
    company_id: str,
    plan_id: str | None,
    currency: str,
    net_amount: float,
    vat_rate: float,
    issue_date: date,
    due_date: date | None,
    notes: str | None,
) -> models.Invoice:
    vat_amount = (Decimal(str(net_amount)) * Decimal(str(vat_rate)) / Decimal("100")).quantize(Decimal("0.01"))
    gross_amount = (Decimal(str(net_amount)) + vat_amount).quantize(Decimal("0.01"))

    number = next_invoice_number(db, issue_date)
    inv = models.Invoice(
        id=str(uuid4()),
        invoice_number=number,
        company_id=company_id,
        plan_id=plan_id,
        currency=currency,
        net_amount=Decimal(str(net_amount)).quantize(Decimal("0.01")),
        vat_rate=Decimal(str(vat_rate)).quantize(Decimal("0.01")),
        vat_amount=vat_amount,
        gross_amount=gross_amount,
        issue_date=issue_date,
        due_date=due_date,
        notes=notes,
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def list_invoices(db: Session, skip: int = 0, limit: int = 100) -> list[models.Invoice]:
    return db.query(models.Invoice).order_by(models.Invoice.created_at.desc()).offset(skip).limit(limit).all()


def get_invoice(db: Session, invoice_id: str) -> models.Invoice | None:
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
