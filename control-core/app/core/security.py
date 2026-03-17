from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

from cryptography.fernet import Fernet

# Use bcrypt_sha256 to avoid the 72-byte input limitation of raw bcrypt
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# Generate a key if not provided, for production this MUST be in .env
ENCRYPTION_KEY = settings.SECRET_KEY[:32].encode().rjust(32, b'0')
fernet = Fernet(Fernet.generate_key() if settings.SECRET_KEY == "your-super-secret-key-change-it-in-prod" else Fernet.generate_key())
# Simplified for now using Fernet, but in real prod we would use a fixed key from ENV

def encrypt_secret(content: str) -> str:
    if not content: return ""
    f = Fernet(settings.SECRET_KEY.encode()[:32].rjust(32, b'=')) # Mocking key gen for demo
    # Correct way is to have a dedicated FERNET_KEY in settings
    return f.encrypt(content.encode()).decode()

def decrypt_secret(encrypted_content: str) -> str:
    if not encrypted_content: return ""
    f = Fernet(settings.SECRET_KEY.encode()[:32].rjust(32, b'='))
    return f.decrypt(encrypted_content.encode()).decode()

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=7  # Refresh token lasts 7 days
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    try:
        # passlib will handle the hashing and salt generation
        return pwd_context.hash(password)
    except Exception as e:
        # Provide a clearer error message for the caller and log underlying exception
        raise RuntimeError(f"Error hashing password: {e}") from e
