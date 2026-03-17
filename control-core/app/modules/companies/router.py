from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.deps import get_current_admin, get_current_user
from app.modules.auth.models import User
from app.modules.companies import crud, schemas

router = APIRouter()


@router.get("/me", response_model=schemas.CompanyResponse)
def get_my_company(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.company_details:
        raise HTTPException(status_code=404, detail="Company details not found")
    return current_user.company_details


@router.put("/me", response_model=schemas.CompanyResponse)
def update_my_company(
    payload: schemas.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = current_user.company_details
    if not company:
        raise HTTPException(status_code=404, detail="Company details not found")
    return crud.update_company(db, company, payload.model_dump(exclude_unset=True))


@router.get("/", response_model=list[schemas.CompanyListResponse])
def admin_list_companies(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    return crud.list_companies(db, skip=skip, limit=limit)


@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def admin_get_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    company = crud.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.patch("/{company_id}/plan", response_model=schemas.CompanyResponse)
def admin_set_company_plan(
    company_id: str,
    payload: schemas.SetCompanyPlanRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    company = crud.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.set_company_plan(db, company, payload.plan_id)

