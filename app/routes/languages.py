from fastapi import APIRouter, HTTPException, Query, Depends
import pandas as pd
from pathlib import Path
import numpy as np
from app.security import verify_api_key

router = APIRouter(tags=["Languages"], dependencies=[Depends(verify_api_key)])

BASE_DIR = Path(__file__).resolve().parents[2]

languages_df = pd.read_csv(BASE_DIR / "data/raw/languages.csv")
names_df = pd.read_csv(BASE_DIR / "data/raw/names.csv")

# Replace NaN with None so JSON can handle it
languages_df = languages_df.replace({np.nan: None})
names_df = names_df.replace({np.nan: None})


def paginate(df: pd.DataFrame, limit: int, offset: int) -> pd.DataFrame:
    return df.iloc[offset : offset + limit]


def get_language_row(language_id: str) -> pd.Series:
    result = languages_df[languages_df["ID"] == language_id]
    if result.empty:
        raise HTTPException(status_code=404, detail="Language not found")
    return result.iloc[0]


@router.get("/languages")
def get_languages(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    macroarea: str | None = None,
    level: str | None = None,
    country: str | None = None,
):
    result = languages_df.copy()

    if macroarea:
        result = result[
            result["Macroarea"]
            .fillna("")
            .str.contains(rf"(^|,\s*){macroarea}(\s*,|$)", case=False, regex=True)
        ]

    if level:
        result = result[
            result["Level"].fillna("").str.contains(level, case=False, na=False)
        ]

    if country:
        result = result[
            result["Countries"].fillna("").str.contains(country, case=False, na=False)
        ]

    result = paginate(result, limit, offset)
    return result.to_dict(orient="records")


@router.get("/languages/search")
def search_languages(
    name: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    result = languages_df[
        languages_df["Name"].fillna("").str.contains(name, case=False, na=False)
    ]

    result = paginate(result, limit, offset)
    return result.to_dict(orient="records")


@router.get("/languages/iso/{iso_code}")
def get_language_by_iso(iso_code: str):
    result = languages_df[
        languages_df["ISO639P3code"].fillna("").str.lower() == iso_code.lower()
    ]

    if result.empty:
        raise HTTPException(status_code=404, detail="Language not found")

    return result.iloc[0].to_dict()


@router.get("/languages/random")
def get_random_language():
    random_language = languages_df.sample(1).iloc[0]
    return random_language.to_dict()


@router.get("/languages/{language_id}")
def get_language(language_id: str):
    row = get_language_row(language_id)
    return row.to_dict()


@router.get("/languages/{language_id}/names")
def get_language_names(language_id: str):
    _ = get_language_row(language_id)

    result = names_df[names_df["Language_ID"] == language_id]
    return result.to_dict(orient="records")


@router.get("/languages/{language_id}/classification")
def get_language_classification(language_id: str):
    current = get_language_row(language_id)

    classification = [
        {
            "id": current["ID"],
            "name": current["Name"],
            "level": current["Level"],
        }
    ]

    visited = set()
    parent_id = current["Family_ID"]

    while parent_id is not None:
        if parent_id in visited:
            break
        visited.add(parent_id)

        parent_rows = languages_df[languages_df["ID"] == parent_id]
        if parent_rows.empty:
            break

        parent = parent_rows.iloc[0]
        classification.append(
            {
                "id": parent["ID"],
                "name": parent["Name"],
                "level": parent["Level"],
            }
        )
        parent_id = parent["Family_ID"]

    classification.reverse()

    return {
        "language_id": current["ID"],
        "language_name": current["Name"],
        "classification": classification,
    }


@router.get("/families")
def get_families(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    result = languages_df[languages_df["Level"].fillna("").str.lower() == "family"]
    result = paginate(result, limit, offset)
    return result.to_dict(orient="records")


@router.get("/families/{family_id}")
def get_family(family_id: str):
    result = languages_df[
        (languages_df["ID"] == family_id)
        & (languages_df["Level"].fillna("").str.lower() == "family")
    ]

    if result.empty:
        raise HTTPException(status_code=404, detail="Family not found")

    return result.iloc[0].to_dict()


@router.get("/families/{family_id}/languages")
def get_family_languages(
    family_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    family_check = languages_df[
        (languages_df["ID"] == family_id)
        & (languages_df["Level"].fillna("").str.lower() == "family")
    ]

    if family_check.empty:
        raise HTTPException(status_code=404, detail="Family not found")

    result = languages_df[languages_df["Family_ID"] == family_id]
    result = paginate(result, limit, offset)
    return result.to_dict(orient="records")


@router.get("/macroareas")
def get_macroareas():
    macroareas = set()

    for value in languages_df["Macroarea"].dropna():
        parts = [part.strip() for part in str(value).split(",")]
        for part in parts:
            if part:
                macroareas.add(part)

    return [{"macroarea": macroarea} for macroarea in sorted(macroareas)]


@router.get("/macroareas/{macroarea}/languages")
def get_macroarea_languages(
    macroarea: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    result = languages_df[
        languages_df["Macroarea"]
        .fillna("")
        .str.contains(rf"(^|,\s*){macroarea}(\s*,|$)", case=False, regex=True)
    ]

    if result.empty:
        raise HTTPException(status_code=404, detail="Macroarea not found")

    result = paginate(result, limit, offset)
    return result.to_dict(orient="records")


@router.get("/stats/languages-per-macroarea")
def languages_per_macroarea():
    counts = (
        languages_df["Macroarea"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
    )

    return counts.to_dict()


@router.get("/stats/languages-per-family")
def languages_per_family():

    families = languages_df[languages_df["Level"].fillna("").str.lower() == "family"][
        ["ID", "Name"]
    ]

    counts = (
        languages_df["Family_ID"]
        .value_counts()
        .rename_axis("Family_ID")
        .reset_index(name="language_count")
    )

    merged = counts.merge(families, left_on="Family_ID", right_on="ID", how="left")

    result = {
        row["Name"]: int(row["language_count"])
        for _, row in merged.iterrows()
        if pd.notna(row["Name"])
    }

    return result
