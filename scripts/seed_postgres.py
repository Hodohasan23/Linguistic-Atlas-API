import pandas as pd
from sqlmodel import Session
from dotenv import load_dotenv

from app.db.session import get_engine
from app.models.models import (
    Language,
    LanguageName,
    Parameter,
    Code,
    ParameterValue,
    Media,
    Tree,
)

# THEN load env
load_dotenv()

engine = get_engine()

LANGUAGES_CSV = "data/raw/languages.csv"
NAMES_CSV = "data/raw/names.csv"
PARAMETERS_CSV = "data/raw/parameters.csv"
CODES_CSV = "data/raw/codes.csv"
VALUES_CSV = "data/raw/values.csv"
MEDIA_CSV = "data/raw/media.csv"
TREES_CSV = "data/raw/trees.csv"


def clean_str(v):
    if pd.isna(v):
        return None
    t = str(v).strip()
    return t if t else None


def clean_float(v):
    if pd.isna(v):
        return None
    try:
        return float(v)
    except Exception:
        return None


def clean_int(v):
    if pd.isna(v):
        return None
    try:
        return int(v)
    except Exception:
        return None


def clean_bool(v):
    if pd.isna(v):
        return None
    t = str(v).strip().lower()
    if t in {"true", "1", "yes"}:
        return True
    if t in {"false", "0", "no"}:
        return False
    return None


def seed_languages(session):
    df = pd.read_csv(LANGUAGES_CSV)
    for _, r in df.iterrows():
        session.merge(
            Language(
                id=str(r["ID"]),
                name=str(r["Name"]),
                macroarea=clean_str(r.get("Macroarea")),
                latitude=clean_float(r.get("Latitude")),
                longitude=clean_float(r.get("Longitude")),
                glottocode=clean_str(r.get("Glottocode")),
                iso_code=clean_str(r.get("ISO639P3code")),
                level=clean_str(r.get("Level")),
                countries=clean_str(r.get("Countries")),
                family_id=clean_str(r.get("Family_ID")),
                language_id=clean_str(r.get("Language_ID")),
                closest_iso_code=clean_str(r.get("Closest_ISO369P3code")),
                first_year_of_documentation=clean_int(
                    r.get("First_Year_Of_Documentation")
                ),
                last_year_of_documentation=clean_int(
                    r.get("Last_Year_Of_Documentation")
                ),
                is_isolate=clean_bool(r.get("Is_Isolate")),
            )
        )
    session.commit()
    print(f"Seeded languages: {len(df)}")


def seed_names(session):
    df = pd.read_csv(NAMES_CSV)
    for _, r in df.iterrows():
        session.add(
            LanguageName(
                source_id=str(r["ID"]),
                language_id=str(r["Language_ID"]),
                name=str(r["Name"]),
                provider=clean_str(r.get("Provider")),
                lang=clean_str(r.get("lang")),
            )
        )
    session.commit()
    print(f"Seeded names: {len(df)}")


def seed_parameters(session):
    df = pd.read_csv(PARAMETERS_CSV)
    for _, r in df.iterrows():
        session.merge(
            Parameter(
                id=str(r["ID"]),
                name=str(r["Name"]),
                description=clean_str(r.get("Description")),
                column_spec=clean_str(r.get("ColumnSpec")),
                type=clean_str(r.get("type")),
                info_url=clean_str(r.get("infoUrl")),
                datatype=clean_str(r.get("datatype")),
                source=clean_str(r.get("Source")),
            )
        )
    session.commit()
    print(f"Seeded parameters: {len(df)}")


def seed_codes(session):
    df = pd.read_csv(CODES_CSV)
    for _, r in df.iterrows():
        session.merge(
            Code(
                id=str(r["ID"]),
                parameter_id=clean_str(r.get("Parameter_ID")),
                name=clean_str(r.get("Name")),
                description=clean_str(r.get("Description")),
                numerical_value=clean_float(r.get("numerical_value")),
            )
        )
    session.commit()
    print(f"Seeded codes: {len(df)}")


def seed_values(session):
    df = pd.read_csv(VALUES_CSV)
    for _, r in df.iterrows():
        session.merge(
            ParameterValue(
                id=str(r["ID"]),
                language_id=str(r["Language_ID"]),
                parameter_id=str(r["Parameter_ID"]),
                value=clean_str(r.get("Value")),
                code_id=clean_str(r.get("Code_ID")),
                comment=clean_str(r.get("Comment")),
                source=clean_str(r.get("Source")),
                code_reference=clean_str(r.get("codeReference")),
            )
        )
    session.commit()
    print(f"Seeded values: {len(df)}")


def seed_media(session):
    df = pd.read_csv(MEDIA_CSV)
    if df.empty:
        print("media.csv empty, skipping")
        return
    for _, r in df.iterrows():
        session.merge(
            Media(
                id=str(r["ID"]),
                name=clean_str(r.get("Name")),
                description=clean_str(r.get("Description")),
                media_type=clean_str(r.get("Media_Type")),
                download_url=clean_str(r.get("Download_URL")),
                path_in_zip=clean_str(r.get("Path_In_Zip")),
            )
        )
    session.commit()
    print(f"Seeded media: {len(df)}")


def seed_trees(session):
    df = pd.read_csv(TREES_CSV)
    for _, r in df.iterrows():
        session.merge(
            Tree(
                id=str(r["ID"]),
                name=clean_str(r.get("Name")),
                description=clean_str(r.get("Description")),
                tree_is_rooted=clean_bool(r.get("Tree_Is_Rooted")),
                tree_type=clean_str(r.get("Tree_Type")),
                tree_branch_length_unit=clean_str(r.get("Tree_Branch_Length_Unit")),
                media_id=clean_str(r.get("Media_ID")),
                source=clean_str(r.get("Source")),
            )
        )
    session.commit()
    print(f"Seeded trees: {len(df)}")


def main():
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        seed_languages(session)
        seed_names(session)
        seed_parameters(session)
        seed_codes(session)
        seed_values(session)
        seed_media(session)
        seed_trees(session)
    print("\nDone.")


if __name__ == "__main__":
    main()
