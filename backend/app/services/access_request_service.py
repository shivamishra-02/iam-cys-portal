from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.access_request import AccessRequest

def create_request(db: Session, employee_id: int, resource_name: str, reason: str):
    req = AccessRequest(employee_id=employee_id, resource_name=resource_name, reason=reason)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def get_request_by_id(db: Session, request_id: int):
    req = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access request not found")
    return req

def review_request(db: Session, request_id: int, reviewer_id: int, new_status: str):
    if new_status not in ["approved", "rejected"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status must be 'approved' or 'rejected'")
    req = get_request_by_id(db, request_id)
    req.status = new_status
    req.reviewed_by = reviewer_id
    db.commit()
    db.refresh(req)
    return req