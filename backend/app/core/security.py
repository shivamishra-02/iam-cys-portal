from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict) -> str:
    """User data ko JWT token mein encode karta hai, expiry ke saath"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """JWT token ko verify karke uske andar ka data return karta hai"""
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload

# bcrypt algorithm use karenge hashing ke liye
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Plain password ko bcrypt hash mein convert karta hai"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login ke time plain password ko stored hash se match karta hai"""
    return pwd_context.verify(plain_password, hashed_password)