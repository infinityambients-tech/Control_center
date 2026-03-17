from sqlalchemy.orm import Session
from app.modules.plans import models, schemas
from typing import List, Optional

def get_plan(db: Session, plan_id: str) -> Optional[models.Plan]:
    return db.query(models.Plan).filter(models.Plan.id == plan_id).first()

def get_plan_by_name(db: Session, name: str) -> Optional[models.Plan]:
    return db.query(models.Plan).filter(models.Plan.name == name).first()

def get_plans(db: Session, skip: int = 0, limit: int = 100) -> List[models.Plan]:
    return db.query(models.Plan).offset(skip).limit(limit).all()

def create_plan(db: Session, plan: schemas.PlanCreate) -> models.Plan:
    db_plan = models.Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def update_plan(db: Session, plan_id: str, plan_update: schemas.PlanUpdate) -> Optional[models.Plan]:
    db_plan = get_plan(db, plan_id)
    if not db_plan:
        return None
        
    update_data = plan_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
        
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_plan(db: Session, plan_id: str) -> bool:
    db_plan = get_plan(db, plan_id)
    if not db_plan:
        return False
        
    db.delete(db_plan)
    db.commit()
    return True
