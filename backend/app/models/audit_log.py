from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # kisne action kiya
    action = Column(String, nullable=False)  # e.g. "USER_CREATED", "LOGIN", "ROLE_CHANGED"
    details = Column(String, nullable=True)  # extra context
    timestamp = Column(DateTime(timezone=True), server_default=func.now())