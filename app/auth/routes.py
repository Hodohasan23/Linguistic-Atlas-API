from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["Authorisation"])


class AuthRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "researcher@linguisticatlas.com",
                "password": "yourpassword123",
            }
        }
    )
    email: str
    password: str


@router.post("/register")
def register(payload: AuthRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == payload.email)).first()

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    first_user = session.exec(select(User)).first()
    role = "ADMIN" if first_user is None else "USER"

    user = User(
        email=payload.email,
        username=payload.email,
        password_hash=hash_password(payload.password),
        role=role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User created"}


@router.post("/login")
def login(payload: AuthRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role, "id": user.id})

    return {"access_token": token}


@router.get("/me")
def me(token: str):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
