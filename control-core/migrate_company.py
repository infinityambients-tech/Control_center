from sqlalchemy import text
from app.core.db import engine

def migrate():
    with engine.connect() as conn:
        print("Starting migration for company_details...")
        try:
            conn.execute(text("ALTER TABLE company_details ADD COLUMN plan_id VARCHAR"))
            print("Added plan_id column to company_details.")
        except Exception as e:
            print(f"Skipping plan_id: {e}")
            
        conn.commit()
        print("Migration committed.")

if __name__ == "__main__":
    migrate()
