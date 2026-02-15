from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter(tags=["Languages"])

languages_df = pd.read_csv("data/raw/languages.csv")
names_df = pd.read_csv("data/raw/names.csv")

# Replace NaN with None so JSON can handle it
languages_df = languages_df.replace({np.nan: None})
names_df = names_df.replace({np.nan: None})

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

    def paginate(df: pd.DataFrame, limit: int, offset: int) -> pd.DataFrame:
    return df.iloc[offset: offset + limit]


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
            result["Macroarea"].fillna("").str.contains(
                rf"(^|,\s*){macroarea}(\s*,|$)",
                case=False,
                regex=True
            )
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
