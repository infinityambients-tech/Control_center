from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User
from app.modules.users import crud, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.UserAdminListItem])
def admin_list_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    return crud.list_users(db, skip=skip, limit=limit)


@router.patch("/{user_id}", response_model=schemas.UserAdminListItem)
def admin_update_user(
    user_id: str,
    payload: schemas.UserAdminUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user_admin(db, user, payload.model_dump(exclude_unset=True))

