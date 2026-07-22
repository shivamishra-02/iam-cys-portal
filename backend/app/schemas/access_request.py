from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccessRequestCreate(BaseModel):
    resource_name: str
    reason: Optional[str] = None

class AccessRequestResponse(BaseModel):
    id: int
    employee_id: int
    resource_name: str
    reason: Optional[str]
    status: str
    reviewed_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class AccessRequestReview(BaseModel):
    status: str  # "approved" or "rejected"