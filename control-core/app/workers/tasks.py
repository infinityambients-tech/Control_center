from app.workers.celery_app import celery_app
from app.core.db import SessionLocal
from app.modules.connectors.service import sync_all_projects
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="app.workers.tasks.sync_projects_task")
def sync_projects_task():
    """
    Background task to synchronize all projects in the database.
    """
    db = SessionLocal()
    try:
        logger.info("Starting automated project synchronization")
        results = sync_all_projects(db)
        logger.info(f"Sync completed: {results}")
        return results
    except Exception as e:
        logger.error(f"Automated sync failed: {e}")
        return {"error": str(e)}
    finally:
        db.close()
