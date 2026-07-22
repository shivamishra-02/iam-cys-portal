from fastapi import FastAPI

app = FastAPI(title="SecureIdentity - IAM Portal")

@app.get("/")
def health_check():
    return {"status": "SecureIdentity backend is running"}