from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.models import User
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(email: str, password: str, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        email=email, username=email, password_hash=hash_password(password), role="USER"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User created"}


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role})

    return {"access_token": token}


@router.get("/me")
def me(token: str):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
