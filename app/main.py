from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.languages import router as languages_router
from app.routes.language_sets import router as language_sets_router
from app.routes.analytics import router as analytics_router
from app.routes.auth import router as auth_router

app = FastAPI(title="Linguistic Atlas API", version="0.1.0")

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


@app.get("/")
def root():
    return {"message": "Linguistic Atlas API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(languages_router)
app.include_router(language_sets_router)
app.include_router(analytics_router)
app.include_router(auth_router)
