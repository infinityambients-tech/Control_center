from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.modules.deployments import crud, schemas, models
from app.modules.auth.deps import get_current_user
from app.modules.auth.models import User, UserRole
from app.modules.audit.crud import log_action
from app.modules.limit_logic.service import ensure_deployments_limit_for_project

router = APIRouter()

@router.get("/", response_model=List[schemas.DeploymentResponse])
def read_deployments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all recent deployments."""
    return crud.get_deployments(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.DeploymentResponse)
def trigger_deployment(
    *, db: Session = Depends(get_db), deployment_in: schemas.DeploymentCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Trigger a new deployment.
    RBAC: CLIENT (read-only), DEVELOPER/ADMIN (can deploy)
    """
    # Simple RBAC check
    if current_user.role == UserRole.client:
        raise HTTPException(status_code=403, detail="Clients cannot trigger deployments.")

    # Non-admin users can deploy only within their company
    if current_user.role != UserRole.admin:
        if not current_user.company_details:
            raise HTTPException(status_code=400, detail="User must be associated with a company to deploy.")
        from app.modules.projects.models import Project
        project = db.query(Project).filter(Project.id == deployment_in.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        if project.company_id != str(current_user.company_details.id):
            raise HTTPException(status_code=403, detail="Not enough permissions for this project")

        plan = current_user.company_details.plan
        if plan and getattr(plan, "max_deployments_per_month", None) is not None:
            try:
                ensure_deployments_limit_for_project(db, deployment_in.project_id, int(plan.max_deployments_per_month))
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

    # In a real app, this would trigger a background task (Celery/RQ) 
    # to call GitHub/GitLab APIs or run a local script.
    # For now, we seed a 'queued' record correctly.
    
    deployment = crud.create_deployment(db=db, deployment=deployment_in, user_id=str(current_user.id))
    
    log_action(db, "TRIGGER_DEPLOYMENT", user_id=current_user.id, entity="Deployment", entity_id=deployment.id)
    
    # MOCK INTEGRATION: In a real scenario, the backend would now call a webhook.
    # We could simulate a state change here or via a dedicated background task.
    
    return deployment
