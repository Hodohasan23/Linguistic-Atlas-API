from datetime import datetime, UTC
from typing import Optional
from collections import Counter

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import LanguageSet, LanguageSetItem, Language, ParameterValue, LanguageName
from app.core.security import verify_api_key, require_user, require_admin

router = APIRouter(
    prefix="/language-sets",
    tags=["Testimonies: Used to testify existence of endangered languages"],
    dependencies=[Depends(verify_api_key)],
)

AES_LEVELS = {
    "aes-not_endangered": {"label": "Not Endangered", "severity": 1, "at_risk": False},
    "aes-threatened":     {"label": "Threatened",     "severity": 2, "at_risk": True},
    "aes-shifting":       {"label": "Shifting",        "severity": 3, "at_risk": True},
    "aes-moribund":       {"label": "Moribund",        "severity": 4, "at_risk": True},
    "aes-nearly_extinct": {"label": "Nearly Extinct",  "severity": 5, "at_risk": True},
    "aes-extinct":        {"label": "Extinct",         "severity": 6, "at_risk": True},
}

EXTINCTION_RISK_CODES = {"aes-moribund", "aes-nearly_extinct", "aes-extinct"}


def now_utc():
    return datetime.now(UTC)


def _get_aes(language_id: str, session: Session) -> Optional[dict]:
    pv = session.exec(
        select(ParameterValue).where(
            ParameterValue.language_id == language_id,
            ParameterValue.parameter_id == "aes",
        )
    ).first()
    if not pv or not pv.code_id:
        return None
    return AES_LEVELS.get(pv.code_id)


def _get_aes_code_id(language_id: str, session: Session) -> Optional[str]:
    pv = session.exec(
        select(ParameterValue).where(
            ParameterValue.language_id == language_id,
            ParameterValue.parameter_id == "aes",
        )
    ).first()
    return pv.code_id if pv else None


# SCHEMAS

class TestimonyCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Voices on the Edge",
                "description": "Languages classified as moribund or nearly extinct across Sub-Saharan Africa",
                "notes": "Focus on languages with fewer than 100 remaining speakers",
            }
        }
    )
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None


class TestimonyUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Voices on the Edge — Revised",
                "description": "Expanded to include languages from the Horn of Africa",
                "notes": None,
            }
        }
    )
    title: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class TestimonyItemCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language_id": "hdzl1234",
            }
        }
    )
    language_id: str


# CRUD

@router.post(
    "",
    summary="What will be lost: the full portrait of a Testimony",
    description=(
        "Generate a structured analytical summary of the languages in this testimony"
    ),
)
def create_testimony(
    payload: TestimonyCreate,
    session: Session = Depends(get_session),
    token: dict = Depends(require_user),
):
    obj = LanguageSet(
        user_id=token["id"],
        title=payload.title,
        description=payload.description,
        notes=payload.notes,
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get(
    "",
    summary="Every Testimony ever recorded",
    description="Returns all saved Testimonies. Each is a curated collection of languages built around a theme, study, or cause.",
)
def list_testimonies(session: Session = Depends(get_session)):
    return session.exec(select(LanguageSet)).all()


@router.get(
    "/{set_id}",
    summary="Open a Testimony and read its intent",
    description="Retrieve a single Testimony by ID, including its title, description, and notes.",
)
def get_testimony(set_id: int, session: Session = Depends(get_session)):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimony not found")
    return obj


@router.patch(
    "/{set_id}",
    summary="Revise the record: update a Testimony",
    description="Rename or redescribe a Testimony. All fields are optional — only the ones you provide will be updated.",
)
def update_testimony(
    set_id: int,
    payload: TestimonyUpdate,
    session: Session = Depends(get_session),
):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimony not found")

    if payload.title is not None:
        obj.title = payload.title
    if payload.description is not None:
        obj.description = payload.description
    if payload.notes is not None:
        obj.notes = payload.notes

    obj.updated_at = now_utc()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete(
    "/{set_id}",
    summary="Silence a Testimony: erase it permanently",
    description="Permanently removes a Testimony and all its languages. Requires admin privileges.",
)
def delete_testimony(
    set_id: int,
    session: Session = Depends(get_session),
    token: dict = Depends(require_admin),
):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimony not found")

    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    for item in items:
        session.delete(item)

    session.delete(obj)
    session.commit()

    return {"message": "Testimony deleted"}



# ITEMS

@router.post(
    "/{set_id}/languages",
    summary="Add a voice to the record",
    description="Adds a language by Glottolog ID. Returns 400 if it is already present in the collection.",
)
def add_language(
    set_id: int,
    payload: TestimonyItemCreate,
    session: Session = Depends(get_session),
):
    if not session.get(LanguageSet, set_id):
        raise HTTPException(status_code=404, detail="Testimony not found")

    if not session.get(Language, payload.language_id):
        raise HTTPException(status_code=404, detail="Language not found")

    exists = session.exec(
        select(LanguageSetItem).where(
            LanguageSetItem.language_set_id == set_id,
            LanguageSetItem.language_id == payload.language_id,
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Language already in this Testimony")

    item = LanguageSetItem(language_set_id=set_id, language_id=payload.language_id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get(
    "/{set_id}/languages",
    summary="The voices: every language in collection",
    description=(
        "Returns every language in the collection with its endangerment status, "
        "macroarea, and how many distinct names it has been recorded under across sources. "
        "A language with only one recorded name has almost slipped through undocumented."
    ),
)
def list_languages(set_id: int, session: Session = Depends(get_session)):
    if not session.get(LanguageSet, set_id):
        raise HTTPException(status_code=404, detail="Testimony not found")

    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    result = []
    for item in items:
        lang = session.get(Language, item.language_id)
        if not lang:
            continue

        aes = _get_aes(lang.id, session)
        name_count = session.exec(
            select(LanguageName).where(LanguageName.language_id == lang.id)
        ).all()

        result.append({
            "item_id": item.id,
            "language_id": lang.id,
            "name": lang.name,
            "macroarea": lang.macroarea,
            "level": lang.level,
            "endangerment": aes["label"] if aes else "Unknown",
            "at_risk": aes["at_risk"] if aes else None,
            "recorded_names_count": len(name_count),
        })

    return result


@router.delete(
    "/{set_id}/languages/{item_id}",
    summary="Remove a voice from this Testimony",
    description="Removes a single language entry by item ID. The language itself is not deleted from the database.",
)
def remove_language(set_id: int, item_id: int, session: Session = Depends(get_session)):
    item = session.get(LanguageSetItem, item_id)

    if not item or item.language_set_id != set_id:
        raise HTTPException(status_code=404, detail="Language not found in this Testimony")

    session.delete(item)
    session.commit()

    return {"message": "Language removed from Testimony"}


# INSIGHTS

@router.get(
    "/{set_id}/insights",
    summary="What will be lost: the full portrait of a Testimony",
    description=(
        "Runs a full analysis across every language in the collection. "
        "Returns an endangerment breakdown, which families are represented, "
        "geographic spread across macroareas, how many voices are likely lost before 2100, "
        "and which language in the collection is the most isolated from its nearest living relatives. "
        "This is the story your Testimony is telling."
    ),
)
def get_testimony_insights(set_id: int, session: Session = Depends(get_session)):
    testimony = session.get(LanguageSet, set_id)
    if not testimony:
        raise HTTPException(status_code=404, detail="Testimony not found")

    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    if not items:
        return {
            "testimony": testimony.title,
            "language_count": 0,
            "message": "This Testimony has no languages yet. Add some to see what story they tell.",
        }

    languages = [session.get(Language, item.language_id) for item in items]
    languages = [lang for lang in languages if lang]  # filter out any missing records

    endangerment_counts = Counter()
    at_risk = []
    extinction_risk = []

    for lang in languages:
        code_id = _get_aes_code_id(lang.id, session)
        if code_id and code_id in AES_LEVELS:
            label = AES_LEVELS[code_id]["label"]
            endangerment_counts[label] += 1
            if AES_LEVELS[code_id]["at_risk"]:
                at_risk.append(lang.name)
            if code_id in EXTINCTION_RISK_CODES:
                extinction_risk.append({
                    "language_id": lang.id,
                    "name": lang.name,
                    "status": AES_LEVELS[code_id]["label"],
                    "macroarea": lang.macroarea,
                })
        else:
            endangerment_counts["Unknown"] += 1

    family_counts = Counter()
    for lang in languages:
        if lang.family_id:
            family = session.get(Language, lang.family_id)
            family_counts[family.name if family else lang.family_id] += 1
        else:
            family_counts["Isolate (no family)"] += 1

    macroarea_counts = Counter()
    for lang in languages:
        if lang.macroarea:
            for part in lang.macroarea.split(","):
                part = part.strip()
                if part:
                    macroarea_counts[part] += 1
        else:
            macroarea_counts["Unknown"] += 1

    obscurity = []
    for lang in languages:
        name_count = len(session.exec(
            select(LanguageName).where(LanguageName.language_id == lang.id)
        ).all())
        obscurity.append((lang, name_count))

    obscurity.sort(key=lambda x: x[1])
    most_obscure = obscurity[0] if obscurity else None

    # languages with no known relatives — if lost, an entire branch disappears
    isolates = [lang for lang in languages if not lang.family_id and (lang.is_isolate or lang.level == "language")]

    return {
        "testimony": testimony.title,
        "language_count": len(languages),
        "endangerment_breakdown": dict(endangerment_counts),
        "at_risk_count": len(at_risk),
        "likely_extinct_before_2100": {
            "count": len(extinction_risk),
            "languages": extinction_risk,
            "note": "Classified as moribund, nearly extinct, or already extinct per Glottolog AES data.",
        },
        "families_represented": {
            "count": len(family_counts),
            "breakdown": dict(family_counts.most_common()),
        },
        "geographic_spread": {
            "macroareas_covered": len([k for k in macroarea_counts if k != "Unknown"]),
            "breakdown": dict(macroarea_counts.most_common()),
        },
        "language_isolates": {
            "count": len(isolates),
            "languages": [{"id": lang.id, "name": lang.name, "macroarea": lang.macroarea} for lang in isolates],
            "note": "Isolates have no known relatives — if lost, their entire branch of human language disappears.",
        },
        "most_undocumented": {
            "language_id": most_obscure[0].id if most_obscure else None,
            "name": most_obscure[0].name if most_obscure else None,
            "recorded_names": most_obscure[1] if most_obscure else None,
            "note": "The language in this Testimony recorded under the fewest distinct names across all sources.",
        },
    }
