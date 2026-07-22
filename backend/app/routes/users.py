from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, RoleAssign, PasswordReset
from app.core.dependencies import get_current_user, require_role
from app.services import user_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/admin/users", tags=["Admin - User Management"])

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    new_user = user_service.create_user(db, user_data)
    log_action(db, current_user.id, "USER_CREATED", f"Created user {new_user.email}")
    return new_user

@router.get("/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return db.query(User).all()

@router.put("/{user_id}", response_model=UserResponse)
def edit_user(
    user_id: int,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    updated_user = user_service.update_user(db, user_id, updates)
    log_action(db, current_user.id, "USER_UPDATED", f"Updated user id {user_id}")
    return updated_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user_service.delete_user(db, user_id)
    log_action(db, current_user.id, "USER_DELETED", f"Deleted user id {user_id}")
    return {"message": "User deleted successfully"}

@router.patch("/{user_id}/activate", response_model=UserResponse)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = user_service.set_active_status(db, user_id, True)
    log_action(db, current_user.id, "USER_ACTIVATED", f"Activated user id {user_id}")
    return user

@router.patch("/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = user_service.set_active_status(db, user_id, False)
    log_action(db, current_user.id, "USER_DEACTIVATED", f"Deactivated user id {user_id}")
    return user

@router.patch("/{user_id}/role", response_model=UserResponse)
def change_role(
    user_id: int,
    role_data: RoleAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = user_service.assign_role(db, user_id, role_data.role)
    log_action(db, current_user.id, "ROLE_CHANGED", f"Changed role of user id {user_id} to {role_data.role}")
    return user

@router.patch("/{user_id}/reset-password")
def admin_reset_password(
    user_id: int,
    password_data: PasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user_service.reset_password(db, user_id, password_data.new_password)
    log_action(db, current_user.id, "PASSWORD_RESET", f"Reset password for user id {user_id}")
    return {"message": "Password reset successfully"}

@router.get("/audit-logs")
def view_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    from app.models.audit_log import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "details": log.details,
            "timestamp": log.timestamp
        }
        for log in logs
    ]