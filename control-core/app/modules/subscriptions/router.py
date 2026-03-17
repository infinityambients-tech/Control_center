from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User
from app.modules.subscriptions import crud, schemas
from app.modules.projects.models import SubscriptionSnapshot
from sqlalchemy import func

router = APIRouter()

@router.get("/", response_model=List[schemas.SubscriptionSnapshot])
def get_subscriptions(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(SubscriptionSnapshot).offset(skip).limit(limit).all()

@router.get("/summary", response_model=schemas.SubscriptionSummary)
def get_subscription_summary(db: Session = Depends(get_db)):
    active_count = db.query(func.count(SubscriptionSnapshot.id)).filter(SubscriptionSnapshot.status == "active").scalar() or 0
    churned_count = db.query(func.count(SubscriptionSnapshot.id)).filter(SubscriptionSnapshot.status == "cancelled").scalar() or 0
    
    # Plans distribution
    dist = db.query(SubscriptionSnapshot.plan, func.count(SubscriptionSnapshot.id)).group_by(SubscriptionSnapshot.plan).all()
    plans_dist = {plan: count for plan, count in dist}
    
    return {
        "total_active": active_count,
        "plans_distribution": plans_dist,
        "churned_count": churned_count
    }


@router.get("/active", response_model=list[schemas.SubscriptionResponse])
def admin_list_active_subscriptions(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    return crud.list_active_subscriptions(db, skip=skip, limit=limit)


@router.post("/active", response_model=schemas.SubscriptionResponse)
def admin_create_subscription(
    payload: schemas.SubscriptionCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return crud.create_subscription(
        db=db,
        company_id=payload.company_id,
        plan_id=payload.plan_id,
        status=payload.status,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
