from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.connectors.service import sync_all_projects

router = APIRouter()

@router.post("/sync")
def trigger_sync(db: Session = Depends(get_db)):
    """
    Manually trigger a synchronization for all projects.
    """
    results = sync_all_projects(db)
    return {"status": "success", "results": results}

@router.get("/summary")
def get_global_summary(db: Session = Depends(get_db)):
    """
    Get aggregated metrics across all projects.
    """
    # Simple aggregation for now
    from app.modules.projects.models import ProjectMetric
    from sqlalchemy import func
    
    summary = db.query(
        func.sum(ProjectMetric.mrr).label("total_mrr"),
        func.sum(ProjectMetric.revenue_today).label("total_revenue_today"),
        func.sum(ProjectMetric.active_subscriptions).label("total_active_subs")
    ).first()
    
    return {
        "total_mrr": summary.total_mrr or 0.0,
        "total_revenue_today": summary.total_revenue_today or 0.0,
        "total_active_subs": summary.total_active_subs or 0
    }
