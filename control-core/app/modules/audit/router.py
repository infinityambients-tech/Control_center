from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.modules.audit import schemas, models

router = APIRouter()

@router.get("/", response_model=List[schemas.AuditLog])
def get_audit_logs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
