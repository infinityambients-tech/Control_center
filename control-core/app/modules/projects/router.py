from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.modules.projects import crud, schemas
from app.modules.auth.deps import get_current_user
from app.modules.auth.models import User
from app.modules.audit.crud import log_action

router = APIRouter()

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=schemas.Project)
def create_project(
    *, db: Session = Depends(get_db), project_in: schemas.ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    if not current_user.company_details:
        raise HTTPException(status_code=400, detail="User must be associated with a company to create a project.")

    company = current_user.company_details
    plan = company.plan

    if plan:
        # Check current project count for this company
        from app.modules.projects.models import Project
        current_projects_count = db.query(Project).filter(Project.company_id == str(company.id)).count()
        if current_projects_count >= plan.max_projects:
            raise HTTPException(
                status_code=400, 
                detail=f"Plan limit reached. Your current plan allows a maximum of {plan.max_projects} projects."
            )

    project = crud.create_project(db=db, project=project_in, company_id=company.id)
    log_action(db, "CREATE_PROJECT", user_id=current_user.id, entity="Project", entity_id=project.id)
    return project

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    *, db: Session = Depends(get_db), project_id: str,
    current_user: User = Depends(get_current_user)
):
    project = crud.get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", response_model=schemas.Project)
def delete_project(
    *, db: Session = Depends(get_db), project_id: str,
    current_user: User = Depends(get_current_user)
):
    project = crud.delete_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    log_action(db, "DELETE_PROJECT", user_id=current_user.id, entity="Project", entity_id=project_id)
    return project
