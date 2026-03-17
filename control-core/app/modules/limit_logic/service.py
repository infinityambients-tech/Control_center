from __future__ import annotations

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.deployments.models import Deployment
from app.modules.projects.models import Project


def ensure_deployments_limit_for_project(db: Session, project_id: str, max_per_month: int) -> None:
    """
    Raises ValueError if the company owning the project exceeded monthly deployments limit.
    """
    if max_per_month <= 0:
        return

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project or not project.company_id:
        return

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    used = (
        db.query(func.count(Deployment.id))
        .join(Project, Project.id == Deployment.project_id)
        .filter(Project.company_id == project.company_id)
        .filter(Deployment.deployed_at >= month_start)
        .scalar()
        or 0
    )

    if used >= max_per_month:
        raise ValueError(f"Plan limit reached: max {max_per_month} deployments per month.")

