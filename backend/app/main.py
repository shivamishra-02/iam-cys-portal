from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user  # ensures the model is registered

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureIdentity - IAM Portal")

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}