from app.core.db import SessionLocal
from app.modules.projects import crud, schemas, models
from app.modules.auth.models import CompanyDetails, User
from app.modules.plans.models import Plan

def seed():
    db = SessionLocal()
    try:
        # Check if project exists
        existing = db.query(models.Project).first()
        if not existing:
            project_in = schemas.ProjectCreate(
                name="Storefront API",
                type="Standard",
                api_base_url="https://api.storefront.example.com",
                payment_provider="PayPal",
                status="active"
            )
            # Find a company to link to
            from app.modules.auth.models import CompanyDetails
            company = db.query(CompanyDetails).first()
            company_id = company.id if company else None
            
            project = crud.create_project(db, project_in, company_id=company_id)
            print(f"Successfully seeded project '{project.name}'.")
        else:
            print(f"Project '{existing.name}' already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
