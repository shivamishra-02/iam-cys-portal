from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user as user_model, audit_log as audit_log_model, access_request as access_request_model
from app.routes import auth, users, manager, employee
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SecureIdentity - IAM Portal")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://iam-cys-portal.vercel.app",  #Actual frontend deployed on vercel (Security k liye)
        "http://127.0.0.1:5500",              # local testing ke liye
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(manager.router)
app.include_router(employee.router)

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}