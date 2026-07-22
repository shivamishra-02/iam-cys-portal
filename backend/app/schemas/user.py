from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# Jab naya user create karte hain, ye fields chahiye (request body)
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "employee"  # default role

# Jab API response deta hai, ye fields dikhenge (password kabhi nahi!)
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy object ko directly Pydantic mein convert karne ke liye