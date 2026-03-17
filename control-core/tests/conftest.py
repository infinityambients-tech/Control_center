import os
import pathlib

# tests should use sqlite file so multiple connections share schema
db_path = pathlib.Path("./test.db")
if db_path.exists():
    db_path.unlink()
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
