from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.auth import models, schemas
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timedelta
import uuid

# ============== User Queries ==============

def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id):
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def user_exists(db: Session, email: str) -> bool:
    """Check if user with email already exists"""
    return db.query(models.User).filter(models.User.email == email).first() is not None

# ============== User Creation & Registration ==============

def create_user(db: Session, user: schemas.UserCreate):
    """Create basic user (legacy method)"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        street=user.street,
        postal_code=user.postal_code,
        city=user.city,
        country=user.country,
        is_superuser=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def register_user(db: Session, reg_data: schemas.UserRegister):
    """Register new user (private or company account)"""
    # Check if user already exists
    if user_exists(db, reg_data.email):
        return None
    
    # Hash password
    hashed_password = get_password_hash(reg_data.password)
    
    # Determine if company account
    is_company = reg_data.is_company
    status = models.UserStatus.pending_email
    
    # Create user
    db_user = models.User(
        email=reg_data.email,
        hashed_password=hashed_password,
        first_name=reg_data.first_name,
        last_name=reg_data.last_name,
        phone=reg_data.phone,
        street=reg_data.street,
        postal_code=reg_data.postal_code,
        city=reg_data.city,
        country=reg_data.country,
        is_company=is_company,
        status=status,
        email_verified=False,
        is_active=True,
        is_superuser=False,
        role=models.UserRole.client
    )
    
    db.add(db_user)
    db.flush()
    
    # If company account, create company details
    if is_company and reg_data.company_details:
        db_company = models.CompanyDetails(
            user_id=db_user.id,
            company_name=reg_data.company_details.company_name,
            nip=reg_data.company_details.nip,
            regon=reg_data.company_details.regon,
            krs=reg_data.company_details.krs,
            company_address=reg_data.company_details.company_address,
            company_postal_code=reg_data.company_details.company_postal_code,
            company_city=reg_data.company_details.company_city,
            company_country=reg_data.company_details.company_country,
            contact_person=reg_data.company_details.contact_person,
            company_phone=reg_data.company_details.company_phone,
            company_email=reg_data.company_details.company_email,
            company_verified=False,
            verification_status="pending"
        )
        db.add(db_company)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# ============== Email Token Management ==============

def create_email_token(db: Session, user_id, hours: int = 24) -> str:
    """Create email verification token"""
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    # Delete any existing tokens for this user (keep only 1 active)
    db.query(models.EmailToken).filter(
        models.EmailToken.user_id == user_id,
        models.EmailToken.verified_at == None
    ).delete()
    
    email_token = models.EmailToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(email_token)
    db.commit()
    return token

def verify_email_token(db: Session, token: str):
    """Verify email token and return user"""
    email_token = db.query(models.EmailToken).filter(
        models.EmailToken.token == token
    ).first()
    
    if not email_token:
        return None
    
    if email_token.expires_at < datetime.utcnow():
        return None  # Token expired
    
    if email_token.verified_at:
        return None  # Token already used
    
    # Mark as verified
    email_token.verified_at = datetime.utcnow()
    
    # Update user status
    user = email_token.user
    user.email_verified = True
    
    # If private account, mark as active
    if not user.is_company:
        user.status = models.UserStatus.active
    else:
        # If company, move to pending_company
        user.status = models.UserStatus.pending_company
    
    db.commit()
    db.refresh(user)
    return user

def get_valid_email_token(db: Session, user_id):
    """Get valid email token for user"""
    token = db.query(models.EmailToken).filter(
        models.EmailToken.user_id == user_id,
        models.EmailToken.verified_at == None,
        models.EmailToken.expires_at > datetime.utcnow()
    ).first()
    return token

# ============== Authentication ==============

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# ============== Company Management ==============

def get_company_details(db: Session, user_id):
    """Get company details for user"""
    return db.query(models.CompanyDetails).filter(
        models.CompanyDetails.user_id == user_id
    ).first()

def get_pending_companies(db: Session, skip: int = 0, limit: int = 10):
    """Get pending company verifications"""
    return db.query(models.CompanyDetails).filter(
        models.CompanyDetails.verification_status == "pending"
    ).offset(skip).limit(limit).all()

def verify_company(db: Session, user_id, approved: bool, reason: str = None):
    """Approve or reject company verification"""
    company = get_company_details(db, user_id)
    if not company:
        return None
    
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if approved:
        company.company_verified = True
        company.verification_status = "approved"
        user.status = models.UserStatus.active
    else:
        company.company_verified = False
        company.verification_status = "rejected"
        company.rejected_reason = reason
        user.status = models.UserStatus.rejected
    
    db.commit()
    db.refresh(user)
    return user
