import os
from dotenv import load_dotenv

# load environment variables before anything else
load_dotenv()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from sqlmodel import Session, select  # noqa: E402

from app.db.session import get_engine  # noqa: E402
from app.models.models import User  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.auth.routes import router as auth_router  # noqa: E402
from app.languages.routes import router as languages_router  # noqa: E402
from app.language_sets.routes import router as language_sets_router  # noqa: E402
from app.analytics.routes import router as analytics_router  # noqa: E402
from app.ask.routes import router as ask_router  # noqa: E402


def seed_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("ADMIN_EMAIL or ADMIN_PASSWORD not set - skipping admin seed")
        return

    with Session(get_engine()) as session:
        existing = session.exec(select(User).where(User.role == "ADMIN")).first()
        if not existing:
            session.add(User(
                email=admin_email,
                username="admin",
                password_hash=hash_password(admin_password),
                role="ADMIN",
            ))
            session.commit()
            print(f"Admin account created: {admin_email}")
        else:
            print(f"Admin already exists: {existing.email}")


app = FastAPI(
    title="Linguistic Atlas API",
    description="A data-driven API for exploring, analysing, and preserving the world’s languages. Discover linguistic relationships, uncover hidden patterns, and interact with the Atlas through intelligent insights.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    seed_admin()


@app.get("/", tags=["Core"])
def root():
    return {"message": "Linguistic Atlas API is running"}


@app.get("/health", tags=["Core"])
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(languages_router)
app.include_router(language_sets_router)
app.include_router(analytics_router)
app.include_router(ask_router)