from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.modules.plans import crud, schemas
from app.modules.auth.deps import get_current_admin, get_current_user
from app.modules.auth import models as auth_models

router = APIRouter()

@router.get("/", response_model=List[schemas.PlanResponse])
def read_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all plans.
    """
    plans = crud.get_plans(db, skip=skip, limit=limit)
    return plans

@router.get("/{plan_id}", response_model=schemas.PlanResponse)
def read_plan(plan_id: str, db: Session = Depends(get_db)):
    """
    Get a specific plan by ID.
    """
    plan = crud.get_plan(db, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.post("/", response_model=schemas.PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    plan: schemas.PlanCreate, 
    db: Session = Depends(get_db),
    current_admin: auth_models.User = Depends(get_current_admin)
):
    """
    Create a new plan. Requires admin privileges.
    """
    db_plan = crud.get_plan_by_name(db, name=plan.name)
    if db_plan:
        raise HTTPException(status_code=400, detail="Plan with this name already exists")
    return crud.create_plan(db=db, plan=plan)

@router.put("/{plan_id}", response_model=schemas.PlanResponse)
def update_plan(
    plan_id: str, 
    plan: schemas.PlanUpdate, 
    db: Session = Depends(get_db),
    current_admin: auth_models.User = Depends(get_current_admin)
):
    """
    Update a plan. Requires admin privileges.
    """
    db_plan = crud.update_plan(db, plan_id, plan)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return db_plan

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: str, 
    db: Session = Depends(get_db),
    current_admin: auth_models.User = Depends(get_current_admin)
):
    """
    Delete a plan. Requires admin privileges.
    """
    success = crud.delete_plan(db, plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return None
