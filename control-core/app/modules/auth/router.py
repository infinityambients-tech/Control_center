from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from datetime import timedelta
from typing import Any, Optional
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from urllib.parse import quote_plus
from app.core import security
from app.core.config import settings
from app.core.db import get_db
from app.modules.auth import crud, schemas, models, validators, emails
from app.modules.auth.deps import get_current_admin, get_current_user, get_token_from_request
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token")

# ============== Dependency Functions ==============
# Moved to app.modules.auth.deps (re-exported imports above).

# ============== Registration Endpoints ==============

@router.post("/register", response_model=schemas.RegisterResponse)
def register_user(
    *,
    db: Session = Depends(get_db),
    registration_data: schemas.UserRegister,
):
    """
    Register new user (private or company account).
    
    - Validates all input data
    - Creates user account
    - Sends verification email
    - Returns registration status
    """
    # Validate form data
    is_valid, errors = validators.validate_registration_form(registration_data)
    if not is_valid:
        logger.warning(f"Registration validation failed: {errors}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )
    
    # Check if user already exists
    if crud.user_exists(db, registration_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check NIP uniqueness for company accounts
    if registration_data.is_company and registration_data.company_details:
        existing_company = db.query(models.CompanyDetails).filter(
            models.CompanyDetails.nip == registration_data.company_details.nip
        ).first()
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company NIP already registered"
            )
    
    # Create user
    try:
        user = crud.register_user(db, registration_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        # Create verification token
        token = crud.create_email_token(
            db, 
            user.id,
            hours=getattr(settings, 'VERIFICATION_TOKEN_EXPIRE_HOURS', 24)
        )
        
        # Send verification email
        email_sent = emails.email_service.send_verification_email(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            token=token
        )
        
        if not email_sent:
            logger.warning(f"Failed to send verification email to {user.email}")
        
        # If company account, send company pending email
        if user.is_company and user.company_details:
            emails.email_service.send_company_pending_email(
                email=user.email,
                contact_person=user.company_details.contact_person,
                company_name=user.company_details.company_name,
                nip=user.company_details.nip
            )
        
        return schemas.RegisterResponse(
            success=True,
            message="Account created successfully. Please check your email to verify your account.",
            status=user.status.value,
            user_id=user.id
        )
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create account"
        )

@router.post("/check-email", response_model=schemas.CheckEmailResponse)
def check_email_availability(
    *,
    db: Session = Depends(get_db),
    check_data: schemas.CheckEmailRequest,
):
    """
    Check if email is available for registration.
    Prevents duplicate email registration.
    """
    exists = crud.user_exists(db, check_data.email)
    return schemas.CheckEmailResponse(
        available=not exists,
        message="Email is available" if not exists else "Email already registered"
    )

# ============== Email Verification Endpoints ==============

@router.post("/verify-email", response_model=schemas.EmailVerifyResponse)
def verify_email(
    *,
    db: Session = Depends(get_db),
    verify_data: schemas.EmailVerifyRequest,
):
    """
    Verify email with token.
    Sets email_verified=true and updates status.
    """
    user = crud.verify_email_token(db, verify_data.token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    return schemas.EmailVerifyResponse(
        success=True,
        message="Email verified successfully",
        status=user.status.value
    )

@router.get("/verify-email/{token}")
def verify_email_link(
    token: str,
    db: Session = Depends(get_db),
):
    """
    Verify email via link (from email).
    Redirects to frontend with status.
    """
    user = crud.verify_email_token(db, token)
    
    frontend = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')

    if not user:
        return RedirectResponse(
            # Use hash route so frontend HashRouter handles the route and query params
            url=f"{frontend}/#/verify-email-error",
            status_code=status.HTTP_302_FOUND
        )

    # Build redirect params; include email so frontend can prefill
    params = f"status={quote_plus(user.status.value)}&email={quote_plus(user.email)}"

    # If the user is active and fully verified (private account or approved company)
    # create a short-lived access token and refresh token to allow seamless sign-in
    try:
        if user.email_verified and user.status == models.UserStatus.active:
            access_token_expires = timedelta(minutes=getattr(settings, 'AUTO_LOGIN_EXPIRE_MINUTES', 5))
            access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
            refresh_token = security.create_refresh_token(user.id)
            params += f"&access_token={quote_plus(access_token)}&refresh_token={quote_plus(refresh_token)}"
    except Exception:
        # Don't break the redirect if token generation fails; continue without tokens
        logger.exception('Failed to create auto-login tokens for user %s', getattr(user, 'id', None))

    # Build RedirectResponse and set HttpOnly cookies for tokens (safer for production)
    redirect_url = f"{frontend}/#/verify-email-success?{params}"
    resp = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)

    try:
        if 'access_token' in params:
            # Set cookies; for dev we set secure=False, samesite='lax'
            resp.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                max_age=getattr(settings, 'AUTO_LOGIN_EXPIRE_MINUTES', 5) * 60,
                samesite='lax',
                secure=getattr(settings, 'COOKIE_SECURE', False),
                path='/'
            )
            resp.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                max_age=7 * 24 * 3600,
                samesite='lax',
                secure=getattr(settings, 'COOKIE_SECURE', False),
                path='/'
            )
    except Exception:
        logger.exception('Failed to set auth cookies on redirect')

    return resp

@router.post("/resend-verification", response_model=schemas.EmailVerifyResponse)
def resend_verification_email(
    *,
    db: Session = Depends(get_db),
    email_data: schemas.EmailResendRequest,
):
    """
    Resend verification email to user.
    """
    user = crud.get_user_by_email(db, email_data.email)
    
    if not user:
        # Don't reveal if email exists for security
        return schemas.EmailVerifyResponse(
            success=True,
            message="If the email is registered, you will receive a verification link"
        )
    
    # If already verified, return error
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    # Create new token and send email
    token = crud.create_email_token(db, user.id)
    
    email_sent = emails.email_service.send_verification_email(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        token=token
    )
    
    if not email_sent:
        logger.warning(f"Failed to resend verification email to {user.email}")
    
    return schemas.EmailVerifyResponse(
        success=True,
        message="Verification email sent. Please check your inbox."
    )

# ============== Authentication Endpoints ==============

@router.post("/login/access-token", response_model=schemas.LoginResponse)
def login_access_token(
    response: Response,
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login. Sets HttpOnly cookies for access and refresh tokens.
    Tokens are NOT returned in response body; stored in HttpOnly cookies instead.
    """
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if email is verified
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email first."
        )
    
    # Check if company account is verified (if applicable)
    if user.is_company and user.status == models.UserStatus.pending_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Company account pending verification"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = security.create_refresh_token(user.id)

    # Set HttpOnly cookies for tokens (cookie-only auth)
    try:
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite='lax',
            secure=getattr(settings, 'COOKIE_SECURE', False),
            path='/'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            max_age=7 * 24 * 3600,
            samesite='lax',
            secure=getattr(settings, 'COOKIE_SECURE', False),
            path='/'
        )
    except Exception as e:
        logger.exception('Failed to set auth cookies on login')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set authentication cookies"
        )

    return {
        "token_type": "bearer",
        "user": schemas.UserResponse.from_orm(user),
        "message": "Login successful"
    }

@router.post("/refresh", response_model=schemas.Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired or invalid")
    
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": schemas.UserResponse.from_orm(user)
    }

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(
    current_user: models.User = Depends(get_current_user),
):
    """
    Get current authenticated user.
    """
    return current_user

@router.post("/logout")
def logout(response: Response):
    """
    Logout user by clearing authentication cookies.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=getattr(settings, 'COOKIE_SECURE', False),
        httponly=True,
        samesite="lax"
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=getattr(settings, 'COOKIE_SECURE', False),
        httponly=True,
        samesite="lax"
    )
    return {"success": True, "message": "Logged out successfully"}

# ============== Admin Company Verification Endpoints ==============

@router.get("/admin/companies/pending", response_model=list[schemas.CompanyPendingResponse])
def get_pending_companies(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """
    Get list of pending company verifications.
    Admin only.
    """
    companies = crud.get_pending_companies(db, skip=skip, limit=limit)
    
    result = []
    for company in companies:
        result.append(schemas.CompanyPendingResponse(
            id=company.id,
            user_id=company.user_id,
            user_email=company.user.email,
            user_name=f"{company.user.first_name} {company.user.last_name}",
            company_name=company.company_name,
            nip=company.nip,
            document_path=company.document_path,
            created_at=company.created_at,
            status=company.verification_status
        ))
    
    return result

@router.post("/admin/companies/{user_id}/verify", response_model=schemas.CompanyVerifyResponse)
def verify_company(
    user_id: str,
    verify_data: schemas.CompanyVerifyRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin),
):
    """
    Approve or reject company verification.
    Admin only.
    """
    user = crud.verify_company(db, user_id, verify_data.approved, verify_data.reason)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or company not found"
        )
    
    # Send email notification
    if verify_data.approved:
        emails.email_service.send_company_verified_email(
            email=user.email,
            contact_person=user.company_details.contact_person,
            company_name=user.company_details.company_name
        )
        message = "Company verified successfully"
    else:
        emails.email_service.send_company_rejected_email(
            email=user.email,
            contact_person=user.company_details.contact_person,
            company_name=user.company_details.company_name,
            reason=verify_data.reason or "No reason provided"
        )
        message = "Company rejected"

    # Notify connected realtime clients (if any) about the status change
    try:
        from app.main import app as main_app  # local import to avoid circular dependency
        conns = getattr(main_app.state, 'connections', {}).get(str(user.id), set())
        payload = {"type": "company_verification", "status": user.status.value, "user_id": user.id}
        for ws in list(conns):
            try:
                asyncio.create_task(ws.send_json(payload))
            except Exception:
                logger.exception('Failed to send realtime notification to websocket')
    except Exception:
        logger.exception('Realtime notification error')
    
    return schemas.CompanyVerifyResponse(
        success=True,
        message=message,
        new_status=user.status.value
    )
