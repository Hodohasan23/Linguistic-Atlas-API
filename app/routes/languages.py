from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter(tags=["Languages"])

languages_df = pd.read_csv("data/raw/languages.csv")
names_df = pd.read_csv("data/raw/names.csv")


@router.get("/languages")
def get_languages(limit: int = 20, offset: int = 0):
    result = languages_df.iloc[offset: offset + limit]
    return result.to_dict(orient="records")


@router.get("/languages/{language_id}")
def get_language(language_id: str):
    result = languages_df[languages_df["ID"] == language_id]

    if result.empty:
        raise HTTPException(status_code=404, detail="Language not found")

    return result.iloc[0].to_dict()