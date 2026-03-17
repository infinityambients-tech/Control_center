from sqlalchemy import text
from app.core.db import engine

def migrate():
    with engine.connect() as conn:
        print("Starting migration...")
        try:
            conn.execute(text("ALTER TABLE projects ADD COLUMN company_id VARCHAR"))
            print("Added company_id column.")
        except Exception as e:
            print(f"Skipping company_id: {e}")
            
        try:
            conn.execute(text("ALTER TABLE projects ADD COLUMN subscription_id VARCHAR"))
            print("Added subscription_id column.")
        except Exception as e:
            print(f"Skipping subscription_id: {e}")
            
        conn.commit()
        print("Migration committed.")

if __name__ == "__main__":
    migrate()
