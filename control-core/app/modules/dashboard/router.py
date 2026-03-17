from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User
from app.modules.dashboard import schemas
from app.modules.deployments.models import Deployment
from app.modules.invoices.models import Invoice
from app.modules.projects.models import Project
from app.modules.subscriptions.models import Subscription, SubscriptionStatus
from app.modules.audit.models import AuditLog

router = APIRouter()


@router.get("/summary", response_model=schemas.DashboardSummary)
def admin_dashboard_summary(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    projects_count = db.query(func.count(Project.id)).scalar() or 0
    active_subs = (
        db.query(func.count(Subscription.id))
        .filter(Subscription.status == SubscriptionStatus.active)
        .scalar()
        or 0
    )

    today = date.today()
    month_start = date(today.year, today.month, 1)
    revenue = (
        db.query(func.sum(Invoice.gross_amount))
        .filter(Invoice.issue_date >= month_start)
        .scalar()
        or 0
    )

    recent_deployments = (
        db.query(Deployment)
        .order_by(Deployment.deployed_at.desc())
        .limit(10)
        .all()
    )
    deployments_payload = [
        {
            "id": d.id,
            "project_id": d.project_id,
            "environment": getattr(d.environment, "value", str(d.environment)),
            "status": getattr(d.status, "value", str(d.status)),
            "commit_hash": d.commit_hash,
            "deployed_at": d.deployed_at.isoformat() if d.deployed_at else None,
        }
        for d in recent_deployments
    ]

    recent_activity = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(10).all()
    activity_payload = [
        {
            "id": a.id,
            "action": a.action,
            "user_id": str(a.user_id) if a.user_id else None,
            "entity": a.entity,
            "entity_id": a.entity_id,
            "timestamp": a.timestamp.isoformat() if a.timestamp else None,
        }
        for a in recent_activity
    ]

    return schemas.DashboardSummary(
        projects_count=projects_count,
        active_subscriptions_count=active_subs,
        monthly_revenue_gross=float(revenue),
        recent_deployments=deployments_payload,
        recent_activity=activity_payload,
    )

