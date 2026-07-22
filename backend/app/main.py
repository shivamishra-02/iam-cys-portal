from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import Base, engine, get_db
from app.models import user as user_model
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureIdentity - IAM Portal")

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}

# Temporary test route - Step 4 mein proper route banayenge
@app.post("/test-create-user", response_model=UserResponse)
def test_create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = user_model.User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user