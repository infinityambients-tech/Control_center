from app.core.db import SessionLocal
from app.modules.plans import crud, schemas

def seed():
    db = SessionLocal()
    try:
        # Check if plan already exists
        existing = crud.get_plan_by_name(db, "Pro")
        if not existing:
            plan_in = schemas.PlanCreate(
                name="Pro",
                monthly_price=49.0,
                yearly_price=490.0,
                max_projects=10,
                max_users=5,
                max_storage_gb=20,
                priority_support=True
            )
            crud.create_plan(db, plan_in)
            print("Successfully seeded Pro plan.")
        else:
            print("Pro plan already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
