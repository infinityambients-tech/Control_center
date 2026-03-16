from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.subscriptions import models


def list_active_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> list[models.Subscription]:
    return (
        db.query(models.Subscription)
        .order_by(models.Subscription.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_subscription(
    db: Session,
    company_id: str,
    plan_id: str | None,
    status: models.SubscriptionStatus,
    start_date,
    end_date,
) -> models.Subscription:
    sub = models.Subscription(
        company_id=company_id,
        plan_id=plan_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def get_subscription(db: Session, subscription_id: str) -> models.Subscription | None:
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

