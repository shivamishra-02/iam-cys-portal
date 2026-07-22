from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token

from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.audit_service import log_action




router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role,
        "full_name": current_user.full_name
    }

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated. Contact your administrator.")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    log_action(db, user_id=user.id, action="LOGIN", details=f"{user.email} logged in")

    return TokenResponse(access_token=access_token)

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Step 1: User ko email se dhoondo
    user = db.query(User).filter(User.email == credentials.email).first()

    # Step 2: User exist karta hai aur password sahi hai, dono check karo
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 3: Deactivated user ko login na karne do
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact your administrator."
        )

    # Step 4: Token generate karo (email aur role encode karke)
    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return TokenResponse(access_token=access_token)