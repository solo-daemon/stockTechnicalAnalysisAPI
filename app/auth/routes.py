from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # For demo: hardcoded user check
    if form_data.username != "admin" or form_data.password != "admin":
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    data = {"sub": form_data.username}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data = {"sub": form_data.username}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data["exp"] = expire
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}