
from fastapi import APIRouter, HTTPException
from prepwise2 import db
from models import UserCreate, LoginIn
from auth import hash_password, verify_password, create_access_token
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_pw = hash_password(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password_hash": hashed_pw,
        "preferences": {},
    }
    result = db.users.insert_one(new_user)
    return {"user_id": str(result.inserted_id), "email": user.email}

@router.post("/login")
def login(credentials: LoginIn):
    user = db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": str(user["_id"]), "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}
