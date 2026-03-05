from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.models import Language, LanguageName, ParameterValue, Parameter, Code
from app.security import verify_api_key

router = APIRouter(tags=["Languages"], dependencies=[Depends(verify_api_key)])


@router.get("/languages")
def get_languages(
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
    macroarea: str | None = None,
    level: str | None = None,
    country: str | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Language)
    if macroarea:
        statement = statement.where(Language.macroarea.ilike(f"%{macroarea}%"))
    if level:
        statement = statement.where(Language.level.ilike(f"%{level}%"))
    if country:
        statement = statement.where(Language.countries.ilike(f"%{country}%"))
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()


@router.get("/languages/map")
def get_languages_map(
    limit: int = Query(500, ge=1, le=2000),
    session: Session = Depends(get_session),
):
    statement = (
        select(Language)
        .where(Language.latitude.is_not(None))
        .where(Language.longitude.is_not(None))
        .limit(limit)
    )
    results = session.exec(statement).all()
    return [
        {
            "ID": r.id,
            "Name": r.name,
            "Macroarea": r.macroarea,
            "Latitude": r.latitude,
            "Longitude": r.longitude,
            "Level": r.level,
            "ISO639P3code": r.iso_code,
        }
        for r in results
    ]


@router.get("/languages/search")
def search_languages(
    name: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    statement = (
        select(Language)
        .where(Language.name.ilike(f"%{name}%"))
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


@router.get("/languages/random")
def get_random_language(session: Session = Depends(get_session)):
    statement = select(Language).order_by(func.random()).limit(1)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="No languages found")
    return result


@router.get("/languages/iso/{iso_code}")
def get_language_by_iso(iso_code: str, session: Session = Depends(get_session)):
    statement = select(Language).where(
        func.lower(Language.iso_code) == iso_code.lower()
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Language not found")
    return result


@router.get("/languages/{language_id}")
def get_language(language_id: str, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.get("/languages/{language_id}/names")
def get_language_names(language_id: str, session: Session = Depends(get_session)):
    session.get(Language, language_id) or (_ for _ in ()).throw(
        HTTPException(status_code=404, detail="Language not found")
    )
    statement = select(LanguageName).where(LanguageName.language_id == language_id)
    return session.exec(statement).all()


@router.get("/languages/{language_id}/classification")
def get_language_classification(
    language_id: str, session: Session = Depends(get_session)
):
    current = session.get(Language, language_id)
    if not current:
        raise HTTPException(status_code=404, detail="Language not found")

    classification = [{"id": current.id, "name": current.name, "level": current.level}]

    visited = set()
    parent_id = current.family_id

    while parent_id:
        if parent_id in visited:
            break
        visited.add(parent_id)
        parent = session.get(Language, parent_id)
        if not parent:
            break
        classification.append(
            {"id": parent.id, "name": parent.name, "level": parent.level}
        )
        parent_id = parent.family_id

    classification.reverse()
    return {
        "language_id": current.id,
        "language_name": current.name,
        "classification": classification,
    }


@router.get("/languages/{language_id}/parameters")
def get_language_parameters(language_id: str, session: Session = Depends(get_session)):
    if not session.get(Language, language_id):
        raise HTTPException(status_code=404, detail="Language not found")

    values = session.exec(
        select(ParameterValue).where(ParameterValue.language_id == language_id)
    ).all()

    result = []
    for item in values:
        parameter = (
            session.get(Parameter, item.parameter_id) if item.parameter_id else None
        )
        code = session.get(Code, item.code_id) if item.code_id else None
        result.append(
            {
                "parameter_id": item.parameter_id,
                "parameter_name": parameter.name if parameter else None,
                "value": item.value,
                "code_id": item.code_id,
                "code_name": code.name if code else None,
                "code_description": code.description if code else None,
                "comment": item.comment,
                "source": item.source,
            }
        )
    return result


@router.get("/families")
def get_families(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    statement = (
        select(Language)
        .where(func.lower(Language.level) == "family")
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


@router.get("/families/{family_id}")
def get_family(family_id: str, session: Session = Depends(get_session)):
    language = session.get(Language, family_id)
    if not language or (language.level or "").lower() != "family":
        raise HTTPException(status_code=404, detail="Family not found")
    return language


@router.get("/families/{family_id}/languages")
def get_family_languages(
    family_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    family = session.get(Language, family_id)
    if not family or (family.level or "").lower() != "family":
        raise HTTPException(status_code=404, detail="Family not found")

    statement = (
        select(Language)
        .where(Language.family_id == family_id)
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


@router.get("/macroareas")
def get_macroareas(session: Session = Depends(get_session)):
    statement = (
        select(Language.macroarea).where(Language.macroarea.is_not(None)).distinct()
    )
    results = session.exec(statement).all()
    macroareas = set()
    for value in results:
        for part in str(value).split(","):
            part = part.strip()
            if part:
                macroareas.add(part)
    return [{"macroarea": m} for m in sorted(macroareas)]


@router.get("/macroareas/{macroarea}/languages")
def get_macroarea_languages(
    macroarea: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    statement = (
        select(Language)
        .where(Language.macroarea.ilike(f"%{macroarea}%"))
        .offset(offset)
        .limit(limit)
    )
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="Macroarea not found")
    return results


@router.get("/stats/languages-per-macroarea")
def languages_per_macroarea(session: Session = Depends(get_session)):
    statement = (
        select(Language.macroarea, func.count(Language.id).label("count"))
        .where(Language.macroarea.is_not(None))
        .group_by(Language.macroarea)
        .order_by(func.count(Language.id).desc())
    )
    results = session.exec(statement).all()
    return {row[0]: row[1] for row in results}


@router.get("/stats/languages-per-family")
def languages_per_family(session: Session = Depends(get_session)):
    statement = (
        select(Language.family_id, func.count(Language.id).label("count"))
        .where(Language.family_id.is_not(None))
        .group_by(Language.family_id)
        .order_by(func.count(Language.id).desc())
        .limit(50)
    )
    rows = session.exec(statement).all()

    result = {}
    for family_id, count in rows:
        family = session.get(Language, family_id)
        name = family.name if family else family_id
        result[name] = count

    return result
