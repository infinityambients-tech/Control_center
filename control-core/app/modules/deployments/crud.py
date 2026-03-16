from sqlalchemy.orm import Session
from app.modules.deployments import models, schemas
from typing import List, Optional

def get_deployments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Deployment]:
    return db.query(models.Deployment).order_by(models.Deployment.deployed_at.desc()).offset(skip).limit(limit).all()

def get_project_deployments(db: Session, project_id: str) -> List[models.Deployment]:
    return db.query(models.Deployment).filter(models.Deployment.project_id == project_id).order_by(models.Deployment.deployed_at.desc()).all()

def create_deployment(db: Session, deployment: schemas.DeploymentCreate, user_id: str) -> models.Deployment:
    db_deployment = models.Deployment(
        **deployment.model_dump(),
        deployed_by=user_id
    )
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment

def update_deployment_status(db: Session, deployment_id: str, status: models.DeploymentStatus, logs: str = None) -> Optional[models.Deployment]:
    db_deployment = db.query(models.Deployment).filter(models.Deployment.id == deployment_id).first()
    if db_deployment:
        db_deployment.status = status
        if logs:
            db_deployment.logs = (db_deployment.logs or "") + "\n" + logs
        db.commit()
        db.refresh(db_deployment)
    return db_deployment
