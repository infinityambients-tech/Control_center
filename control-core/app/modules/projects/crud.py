from sqlalchemy.orm import Session
from app.modules.projects import models, schemas
import uuid

from app.core.security import encrypt_secret

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def create_project(db: Session, project: schemas.ProjectCreate, company_id: str = None):
    db_project = models.Project(
        id=str(uuid.uuid4()),
        company_id=company_id,
        name=project.name,
        type=project.type,
        api_base_url=project.api_base_url,
        api_key_encrypted=encrypt_secret(project.api_key) if project.api_key else None,
        payment_provider=project.payment_provider,
        status=project.status
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: str):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

def create_metric(db: Session, metric: schemas.MetricBase, project_id: str):
    db_metric = models.ProjectMetric(
        **metric.model_dump(),
        project_id=project_id
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric
