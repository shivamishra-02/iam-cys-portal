from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.db.database import Base

class AccessRequest(Base):
    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_name = Column(String, nullable=False)  # e.g. "Production Database", "AWS Console"
    reason = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending / approved / rejected
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())