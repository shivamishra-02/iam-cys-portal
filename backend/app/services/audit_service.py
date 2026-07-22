from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_action(db: Session, user_id: int, action: str, details: str = None):
    """Har jagah se ye function call karke audit log create karenge"""
    entry = AuditLog(user_id=user_id, action=action, details=details)
    db.add(entry)
    db.commit()