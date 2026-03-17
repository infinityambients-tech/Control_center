from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.settings import models


def get_setting(db: Session, key: str) -> models.AppSetting | None:
    return db.query(models.AppSetting).filter(models.AppSetting.key == key).first()


def upsert_setting(db: Session, key: str, value: str | None) -> models.AppSetting:
    existing = get_setting(db, key)
    if existing:
        existing.value = value
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    setting = models.AppSetting(key=key, value=value)
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def list_settings(db: Session, skip: int = 0, limit: int = 200) -> list[models.AppSetting]:
    return db.query(models.AppSetting).offset(skip).limit(limit).all()

