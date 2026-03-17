from app.core.db import SessionLocal
from app.modules.deployments import crud, schemas, models
from app.modules.projects.models import Project

def seed():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        if not projects:
            print("No projects found to associate deployments with.")
            return
            
        project = projects[0]
        
        # Seed a few deployments
        mock_data = [
            {"env": models.EnvironmentType.production, "status": models.DeploymentStatus.deployed, "ver": "1.2.0"},
            {"env": models.EnvironmentType.staging, "status": models.DeploymentStatus.failed, "ver": "1.3.0-rc1"},
            {"env": models.EnvironmentType.development, "status": models.DeploymentStatus.building, "ver": "1.3.0-beta"}
        ]
        
        for data in mock_data:
            dep_in = schemas.DeploymentCreate(
                project_id=project.id,
                environment=data["env"],
                version=data["ver"],
                commit_hash="abc" + str(hash(data["ver"]))[:4]
            )
            dep = crud.create_deployment(db, dep_in, user_id="system")
            crud.update_deployment_status(db, dep.id, data["status"], logs="Initial seed logs...")
            
        print(f"Successfully seeded {len(mock_data)} deployments for project '{project.name}'.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
