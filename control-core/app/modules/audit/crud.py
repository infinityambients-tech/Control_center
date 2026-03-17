from sqlalchemy.orm import Session
from app.modules.audit import models, schemas
from typing import Any, Optional
import uuid

def log_action(
    db: Session,
    action: str,
    user_id: Optional[uuid.UUID] = None,
    entity: str = None,
    entity_id: str = None,
    ip_address: str = None,
    metadata: Any = None
):
    db_log = models.AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        ip_address=ip_address,
        metadata_json=metadata
    )
    db.add(db_log)
    db.commit()
    return db_log
