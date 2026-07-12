from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import jwt
from .config import SECRET_KEY, ALGORITHM
from app.db.models.user import User
from app.core.database import get_db
from app.core.security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Генерируем токен
    expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}
