from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.access_request import AccessRequestCreate, AccessRequestResponse
from app.core.dependencies import get_current_user
from app.core.security import verify_password, hash_password
from app.services import user_service, access_request_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.get("/profile", response_model=UserResponse)
def view_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = user_service.update_user(db, current_user.id, updates)
    log_action(db, current_user.id, "PROFILE_UPDATED", "User updated their own profile")
    return updated

@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(old_password, current_user.hashed_password):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    current_user.hashed_password = hash_password(new_password)
    db.commit()
    log_action(db, current_user.id, "PASSWORD_CHANGED", "User changed their own password")
    return {"message": "Password changed successfully"}

@router.post("/request-access", response_model=AccessRequestResponse)
def request_access(
    request_data: AccessRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = access_request_service.create_request(
        db, current_user.id, request_data.resource_name, request_data.reason
    )
    log_action(db, current_user.id, "ACCESS_REQUESTED", f"Requested access to '{request_data.resource_name}'")
    return req