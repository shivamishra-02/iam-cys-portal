from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user as user_model
from app.routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureIdentity - IAM Portal")

app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}