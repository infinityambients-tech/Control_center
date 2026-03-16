from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User
from app.modules.invoices import crud, schemas
from app.modules.invoices.pdf_service import generate_invoice_pdf

router = APIRouter()


@router.get("/", response_model=list[schemas.InvoiceResponse])
def admin_list_invoices(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    return crud.list_invoices(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.InvoiceResponse)
def admin_create_invoice(
    payload: schemas.InvoiceCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    inv = crud.create_invoice(
        db=db,
        company_id=payload.company_id,
        plan_id=payload.plan_id,
        currency=payload.currency,
        net_amount=payload.net_amount,
        vat_rate=payload.vat_rate,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
        notes=payload.notes,
    )

    # Best-effort PDF generation (optional dependency).
    try:
        out = generate_invoice_pdf(inv, Path(__file__).resolve().parents[2] / "static" / "invoices")
        inv.pdf_path = str(out)
        db.add(inv)
        db.commit()
        db.refresh(inv)
    except ImportError:
        pass

    return inv


@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)
def admin_get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    inv = crud.get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

