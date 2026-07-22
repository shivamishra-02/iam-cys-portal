from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def create_user(db: Session, user_data: UserCreate):
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, updates: UserUpdate):
    user = get_user_by_id(db, user_id)
    if updates.full_name is not None:
        user.full_name = updates.full_name
    if updates.email is not None:
        user.email = updates.email
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()

def set_active_status(db: Session, user_id: int, is_active: bool):
    user = get_user_by_id(db, user_id)
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user

def assign_role(db: Session, user_id: int, role: str):
    valid_roles = ["admin", "manager", "employee"]
    if role not in valid_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role must be one of {valid_roles}")
    user = get_user_by_id(db, user_id)
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def reset_password(db: Session, user_id: int, new_password: str):
    user = get_user_by_id(db, user_id)
    user.hashed_password = hash_password(new_password)
    db.commit()
    return user