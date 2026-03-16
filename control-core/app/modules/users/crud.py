from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.auth import models as auth_models


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[auth_models.User]:
    return db.query(auth_models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: str) -> auth_models.User | None:
    return db.query(auth_models.User).filter(auth_models.User.id == user_id).first()


def update_user_admin(db: Session, user: auth_models.User, data: dict) -> auth_models.User:
    for key, value in data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

