from passlib.context import CryptContext

# bcrypt algorithm use karenge hashing ke liye
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Plain password ko bcrypt hash mein convert karta hai"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login ke time plain password ko stored hash se match karta hai"""
    return pwd_context.verify(plain_password, hashed_password)