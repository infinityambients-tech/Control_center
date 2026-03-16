from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.modules.finance import schemas
from app.modules.projects.models import PaymentSnapshot, ProjectMetric
from sqlalchemy import func

router = APIRouter()

@router.get("/payments", response_model=List[schemas.PaymentSnapshot])
def get_payments(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(PaymentSnapshot).offset(skip).limit(limit).all()

@router.get("/summary", response_model=schemas.FinanceSummary)
def get_finance_summary(db: Session = Depends(get_db)):
    # Aggregated metrics calculation
    total_rev = db.query(func.sum(PaymentSnapshot.amount)).scalar() or 0.0
    
    # Get latest MRR from metrics
    latest_metrics = db.query(
        func.sum(ProjectMetric.mrr).label("total_mrr")
    ).first()
    
    return {
        "total_revenue": total_rev,
        "mrr": latest_metrics.total_mrr or 0.0,
        "mrr_growth": 15.5, # Placeholder for growth calculation
        "churn_rate": 2.1,  # Placeholder
        "ltv": 450.0        # Placeholder
    }
