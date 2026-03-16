from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.modules.auth import models, schemas

logger = logging.getLogger(__name__)


async def get_token_from_request(request: Request) -> Optional[str]:
    auth = request.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1]
    return request.cookies.get("access_token")


async def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(get_token_from_request),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if not token:
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise credentials_exception
        _ = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    try:
        user_pk = uuid.UUID(str(user_id))
    except Exception:
        user_pk = user_id
    user = db.query(models.User).filter(models.User.id == user_pk).first()
    if not user:
        raise credentials_exception
    return user


async def get_current_admin(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user


async def get_current_developer(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role in (models.UserRole.admin, models.UserRole.developer, models.UserRole.manager):
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
