from fastapi import FastAPI
from app.routes.languages import router as languages_router

app = FastAPI(title="Glottolog Language Explorer API")

app.include_router(languages_router)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
