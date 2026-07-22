from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user as user_model, audit_log as audit_log_model
from app.routes import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureIdentity - IAM Portal")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}