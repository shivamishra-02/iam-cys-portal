from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.access_request import AccessRequest
from app.schemas.user import UserResponse
from app.schemas.access_request import AccessRequestResponse, AccessRequestReview
from app.core.dependencies import require_role
from app.services import access_request_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/employees", response_model=List[UserResponse])
def view_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("manager", "admin"))
):
    return db.query(User).filter(User.role == "employee").all()

@router.get("/access-requests", response_model=List[AccessRequestResponse])
def view_access_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("manager", "admin"))
):
    return db.query(AccessRequest).order_by(AccessRequest.created_at.desc()).all()

@router.patch("/access-requests/{request_id}", response_model=AccessRequestResponse)
def review_access_request(
    request_id: int,
    review: AccessRequestReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("manager", "admin"))
):
    req = access_request_service.review_request(db, request_id, current_user.id, review.status)
    log_action(
        db, current_user.id,
        f"ACCESS_REQUEST_{review.status.upper()}",
        f"Request id {request_id} for '{req.resource_name}'"
    )
    return req