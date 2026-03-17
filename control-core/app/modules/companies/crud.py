from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.auth import models as auth_models


def get_company_by_id(db: Session, company_id: str) -> auth_models.CompanyDetails | None:
    return db.query(auth_models.CompanyDetails).filter(auth_models.CompanyDetails.id == company_id).first()


def get_company_by_user_id(db: Session, user_id: str) -> auth_models.CompanyDetails | None:
    return (
        db.query(auth_models.CompanyDetails)
        .filter(auth_models.CompanyDetails.user_id == user_id)
        .first()
    )


def list_companies(db: Session, skip: int = 0, limit: int = 100) -> list[auth_models.CompanyDetails]:
    return db.query(auth_models.CompanyDetails).offset(skip).limit(limit).all()


def update_company(db: Session, company: auth_models.CompanyDetails, data: dict) -> auth_models.CompanyDetails:
    for key, value in data.items():
        setattr(company, key, value)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def set_company_plan(db: Session, company: auth_models.CompanyDetails, plan_id: str | None) -> auth_models.CompanyDetails:
    company.plan_id = plan_id
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

