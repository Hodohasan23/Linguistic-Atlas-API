from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.models.models import Language, LanguageName, ParameterValue, Parameter, Code
from app.core.security import verify_api_key

router = APIRouter(tags=["Languages"], dependencies=[Depends(verify_api_key)])

CURRENT_YEAR = datetime.now().year

_LANGUAGE_EXAMPLE = {
    "id": "stan1295",
    "name": "Somali",
    "macroarea": "Africa",
    "latitude": 6.0,
    "longitude": 46.0,
    "glottocode": "soma1255",
    "iso_code": "som",
    "level": "language",
    "countries": "SO ET KE DJ",
    "family_id": "afro1255",
    "language_id": None,
    "closest_iso_code": "som",
    "first_year_of_documentation": 1900,
    "last_year_of_documentation": 2020,
    "is_isolate": False,
    "endangerment": "Not Endangered",
    "at_risk": False,
}

AES_LEVELS = {
    "aes-not_endangered": {"label": "Not Endangered", "severity": 1, "at_risk": False, "description": "EGIDS: <=6a; UNESCO: safe; ElCat: safe"},
    "aes-threatened":     {"label": "Threatened",     "severity": 2, "at_risk": True,  "description": "EGIDS: 6b; UNESCO: vulnerable; ElCat: vulnerable"},
    "aes-shifting":       {"label": "Shifting",        "severity": 3, "at_risk": True,  "description": "EGIDS: 7; UNESCO: definitely endangered; ElCat: definitely endangered"},
    "aes-moribund":       {"label": "Moribund",        "severity": 4, "at_risk": True,  "description": "EGIDS: 8a; UNESCO: severely endangered; ElCat: severely endangered"},
    "aes-nearly_extinct": {"label": "Nearly Extinct",  "severity": 5, "at_risk": True,  "description": "EGIDS: 8b; UNESCO: critically endangered; ElCat: critically endangered"},
    "aes-extinct":        {"label": "Extinct",         "severity": 6, "at_risk": True,  "description": "EGIDS: >=9; UNESCO: extinct; ElCat: extinct"},
}


def _documentation_status(last_year: int | None) -> str:
    if not last_year:
        return "Never formally documented"
    years_ago = CURRENT_YEAR - last_year
    if years_ago <= 5:
        return "Recently studied"
    if years_ago <= 20:
        return "Studied within the last two decades"
    if years_ago <= 50:
        return "Decades since last study"
    return "Last documented over 50 years ago"


def _with_endangerment(lang: Language, session: Session) -> dict:
    pv = session.exec(
        select(ParameterValue).where(
            ParameterValue.language_id == lang.id,
            ParameterValue.parameter_id == "aes",
        )
    ).first()
    aes = AES_LEVELS.get(pv.code_id) if pv and pv.code_id else None
    return {
        **lang.model_dump(),
        "endangerment": aes["label"] if aes else "Unknown",
        "at_risk": aes["at_risk"] if aes else None,
    }


@router.get(
    "/languages",
    summary="Explore the world’s languages",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [_LANGUAGE_EXAMPLE]
                    }
                }
            }
        }
    },
)
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
    results = session.exec(statement).all()
    return [_with_endangerment(lang, session) for lang in results]


@router.get(
    "/languages/map",
    summary="Visualise languages geographically",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "ID": "stan1295",
                                "Name": "Somali",
                                "Macroarea": "Africa",
                                "Latitude": 6.0,
                                "Longitude": 46.0,
                                "Level": "language",
                                "ISO639P3code": "som",
                            }
                        ]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/languages/search",
    summary="Search languages by name",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [_LANGUAGE_EXAMPLE]
                    }
                }
            }
        }
    },
)
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
    results = session.exec(statement).all()
    return [_with_endangerment(lang, session) for lang in results]


@router.get(
    "/languages/random",
    summary="Discover a random language",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": _LANGUAGE_EXAMPLE
                    }
                }
            }
        }
    },
)
def get_random_language(session: Session = Depends(get_session)):
    statement = select(Language).order_by(func.random()).limit(1)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="No languages found")
    return _with_endangerment(result, session)


@router.get(
    "/languages/iso/{iso_code}",
    summary="Look up a language by ISO 639-3 code",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": _LANGUAGE_EXAMPLE
                    }
                }
            }
        }
    },
)
def get_language_by_iso(iso_code: str, session: Session = Depends(get_session)):
    statement = select(Language).where(
        func.lower(Language.iso_code) == iso_code.lower()
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Language not found")
    return result


@router.get(
    "/languages/{language_id}",
    summary="Get a language by Glottolog ID",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": _LANGUAGE_EXAMPLE
                    }
                }
            }
        }
    },
)
def get_language(language_id: str, session: Session = Depends(get_session)):
    language = session.get(Language, language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.get(
    "/languages/{language_id}/names",
    summary="List all known names for a language",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": 1,
                                "source_id": "glottolog",
                                "language_id": "stan1295",
                                "name": "Af Soomaali",
                                "provider": "Ethnologue",
                                "lang": "som",
                            },
                            {
                                "id": 2,
                                "source_id": "iso639",
                                "language_id": "stan1295",
                                "name": "Somali",
                                "provider": "ISO 639-3",
                                "lang": "en",
                            },
                        ]
                    }
                }
            }
        }
    },
)
def get_language_names(language_id: str, session: Session = Depends(get_session)):
    session.get(Language, language_id) or (_ for _ in ()).throw(
        HTTPException(status_code=404, detail="Language not found")
    )
    statement = select(LanguageName).where(LanguageName.language_id == language_id)
    return session.exec(statement).all()


@router.get(
    "/languages/{language_id}/classification",
    summary="Trace the genealogical family tree",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "language_id": "stan1295",
                            "language_name": "Somali",
                            "classification": [
                                {"id": "afro1255", "name": "Afro-Asiatic", "level": "family"},
                                {"id": "cush1243", "name": "Cushitic", "level": "family"},
                                {"id": "east2699", "name": "East Cushitic", "level": "family"},
                                {"id": "stan1295", "name": "Somali", "level": "language"},
                            ],
                        }
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/languages/{language_id}/parameters",
    summary="Get typological features",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "parameter_id": "aes",
                                "parameter_name": "Agglomerated Endangerment Status",
                                "value": "1",
                                "code_id": "aes-not_endangered",
                                "code_name": "not endangered",
                                "code_description": "EGIDS: <=6a; UNESCO: safe; ElCat: safe",
                                "comment": None,
                                "source": "Glottolog",
                            },
                            {
                                "parameter_id": "med",
                                "parameter_name": "Most Extensive Description",
                                "value": "1",
                                "code_id": "med-grammar",
                                "code_name": "grammar",
                                "code_description": "Grammar with less than 300 pages",
                                "comment": None,
                                "source": "Glottolog",
                            },
                        ]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/languages/{language_id}/endangerment",
    summary="How at risk is this language?",
    description=(
        "Returns a plain-English endangerment profile for a single language based on Glottolog's "
        "Agglomerated Endangerment Status (AES) — compiled from UNESCO, EGIDS, and ElCat sources. "
        "Includes the status label, what it means, how long the language has been documented, "
        "how many years have passed since it was last studied, and a plain-English risk summary."
    ),
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "language_id": "bura1267",
                            "name": "Burak",
                            "aes_code": "aes-moribund",
                            "status": "Moribund",
                            "at_risk": True,
                            "severity": 4,
                            "what_this_means": "EGIDS: 8a; UNESCO: severely endangered; ElCat: severely endangered",
                            "first_documented": 1932,
                            "last_documented": 1987,
                            "years_documented": 55,
                            "years_since_last_study": 38,
                            "documentation_status": "Decades since last study",
                            "is_isolate": False,
                            "macroarea": "Africa",
                            "risk_summary": "Moribund — only a few elderly speakers remain. Unlikely to survive another generation without active revitalisation.",
                        }
                    }
                }
            }
        }
    },
)
def get_language_endangerment(language_id: str, session: Session = Depends(get_session)):
    lang = session.get(Language, language_id)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")

    pv = session.exec(
        select(ParameterValue).where(
            ParameterValue.language_id == language_id,
            ParameterValue.parameter_id == "aes",
        )
    ).first()

    first_year = lang.first_year_of_documentation
    last_year = lang.last_year_of_documentation
    years_documented = (last_year - first_year) if first_year and last_year else None
    years_since_last_study = (CURRENT_YEAR - last_year) if last_year else None

    if not pv or not pv.code_id or pv.code_id not in AES_LEVELS:
        return {
            "language_id": lang.id,
            "name": lang.name,
            "aes_code": None,
            "status": "Unknown",
            "at_risk": None,
            "severity": None,
            "what_this_means": "No endangerment data recorded for this language in Glottolog.",
            "first_documented": first_year,
            "last_documented": last_year,
            "years_documented": years_documented,
            "years_since_last_study": years_since_last_study,
            "documentation_status": _documentation_status(last_year),
            "is_isolate": lang.is_isolate,
            "macroarea": lang.macroarea,
            "risk_summary": "Endangerment status not recorded.",
        }

    aes = AES_LEVELS[pv.code_id]

    risk_summaries = {
        "aes-not_endangered": "Not endangered — the language is being passed on to children and is in active use.",
        "aes-threatened": "Threatened — still spoken but losing ground, often replaced by a dominant regional language.",
        "aes-shifting": "Shifting — the community is moving away from the language, typically within a generation.",
        "aes-moribund": "Moribund — only a few elderly speakers remain. Unlikely to survive another generation without active revitalisation.",
        "aes-nearly_extinct": "Nearly extinct — fewer than a handful of speakers, all elderly. Extinction is imminent.",
        "aes-extinct": "Extinct — no known living speakers.",
    }

    return {
        "language_id": lang.id,
        "name": lang.name,
        "aes_code": pv.code_id,
        "status": aes["label"],
        "at_risk": aes["at_risk"],
        "severity": aes["severity"],
        "what_this_means": aes["description"],
        "first_documented": first_year,
        "last_documented": last_year,
        "years_documented": years_documented,
        "years_since_last_study": years_since_last_study,
        "documentation_status": _documentation_status(last_year),
        "is_isolate": lang.is_isolate,
        "macroarea": lang.macroarea,
        "risk_summary": risk_summaries.get(pv.code_id, "No summary available."),
    }


@router.get(
    "/families",
    summary="Browse language families",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "id": "afro1255",
                                "name": "Afro-Asiatic",
                                "macroarea": "Africa",
                                "latitude": None,
                                "longitude": None,
                                "level": "family",
                                "countries": None,
                                "family_id": None,
                            }
                        ]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/families/{family_id}",
    summary="Get a family by Glottolog ID",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "id": "afro1255",
                            "name": "Afro-Asiatic",
                            "macroarea": "Africa",
                            "latitude": None,
                            "longitude": None,
                            "level": "family",
                            "countries": None,
                            "family_id": None,
                        }
                    }
                }
            }
        }
    },
)
def get_family(family_id: str, session: Session = Depends(get_session)):
    language = session.get(Language, family_id)
    if not language or (language.level or "").lower() != "family":
        raise HTTPException(status_code=404, detail="Family not found")
    return language


@router.get(
    "/families/{family_id}/languages",
    summary="List languages within a family",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [_LANGUAGE_EXAMPLE]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/macroareas",
    summary="List all geographic macroareas",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [
                            {"macroarea": "Africa"},
                            {"macroarea": "Australia"},
                            {"macroarea": "Eurasia"},
                            {"macroarea": "North America"},
                            {"macroarea": "Papunesia"},
                            {"macroarea": "South America"},
                        ]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/macroareas/{macroarea}/languages",
    summary="Browse languages by macroarea",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": [_LANGUAGE_EXAMPLE]
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/stats/languages-per-macroarea",
    summary="Language distribution by macroarea",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "Africa": 2148,
                            "Papunesia": 1984,
                            "South America": 1058,
                            "North America": 912,
                            "Eurasia": 890,
                            "Australia": 387,
                        }
                    }
                }
            }
        }
    },
)
def languages_per_macroarea(session: Session = Depends(get_session)):
    statement = (
        select(Language.macroarea, func.count(Language.id).label("count"))
        .where(Language.macroarea.is_not(None))
        .group_by(Language.macroarea)
        .order_by(func.count(Language.id).desc())
    )
    results = session.exec(statement).all()
    return {row[0]: row[1] for row in results}


@router.get(
    "/stats/languages-per-family",
    summary="Top 50 families by language count",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "Niger-Congo": 1540,
                            "Austronesian": 1248,
                            "Trans-New Guinea": 478,
                            "Sino-Tibetan": 456,
                            "Indo-European": 437,
                            "Afro-Asiatic": 371,
                        }
                    }
                }
            }
        }
    },
)
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


@router.get(
    "/stats/endangerment-breakdown",
    summary="How many of the world's languages are at risk?",
    description=(
        "Returns a count of all languages in the dataset grouped by their Glottolog AES "
        "(Agglomerated Endangerment Status) level — from not endangered through to extinct. "
        "Compiled from UNESCO, EGIDS, and ElCat sources."
    ),
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "total_with_aes_data": 6842,
                            "breakdown": {
                                "Not Endangered": 3201,
                                "Threatened": 964,
                                "Shifting": 748,
                                "Moribund": 591,
                                "Nearly Extinct": 412,
                                "Extinct": 926,
                            },
                            "at_risk_total": 2715,
                            "source": "Glottolog AES — compiled from UNESCO, EGIDS, and ElCat",
                        }
                    }
                }
            }
        }
    },
)
def endangerment_breakdown(session: Session = Depends(get_session)):
    rows = session.exec(
        select(ParameterValue.code_id, func.count(ParameterValue.id).label("count"))
        .where(ParameterValue.parameter_id == "aes")
        .where(ParameterValue.code_id.is_not(None))
        .group_by(ParameterValue.code_id)
    ).all()

    breakdown = {}
    at_risk_total = 0
    total = 0

    for code_id, count in rows:
        if code_id in AES_LEVELS:
            label = AES_LEVELS[code_id]["label"]
            breakdown[label] = count
            total += count
            if AES_LEVELS[code_id]["at_risk"]:
                at_risk_total += count

    return {
        "total_with_aes_data": total,
        "breakdown": breakdown,
        "at_risk_total": at_risk_total,
        "source": "Glottolog AES — compiled from UNESCO, EGIDS, and ElCat",
    }


@router.get(
    "/stats/underdocumented",
    summary="Languages going silent: at risk and unstudied for decades",
    description=(
        "Returns languages that are endangered and have not been studied since before a given year. "
        "These are voices that were already dying when linguists last looked, and haven't been "
        "looked at since. Defaults to languages last documented before 1970."
    ),
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "count": 3,
                            "threshold_year": 1970,
                            "languages": [
                                {
                                    "language_id": "xyz1234",
                                    "name": "Taurap",
                                    "macroarea": "Papunesia",
                                    "last_documented": 1953,
                                    "years_of_silence": 72,
                                    "endangerment": "Nearly Extinct",
                                },
                            ],
                        }
                    }
                }
            }
        }
    },
)
def underdocumented_languages(
    before: int = Query(1970, description="Only include languages last documented before this year."),
    session: Session = Depends(get_session),
):
    at_risk_code_ids = [k for k, v in AES_LEVELS.items() if v["at_risk"]]

    languages = session.exec(
        select(Language)
        .where(Language.last_year_of_documentation.is_not(None))
        .where(Language.last_year_of_documentation < before)
        .where(Language.level == "language")
    ).all()

    result = []
    for lang in languages:
        pv = session.exec(
            select(ParameterValue).where(
                ParameterValue.language_id == lang.id,
                ParameterValue.parameter_id == "aes",
            )
        ).first()

        if not pv or pv.code_id not in at_risk_code_ids:
            continue

        aes = AES_LEVELS[pv.code_id]
        result.append({
            "language_id": lang.id,
            "name": lang.name,
            "macroarea": lang.macroarea,
            "last_documented": lang.last_year_of_documentation,
            "years_of_silence": CURRENT_YEAR - lang.last_year_of_documentation,
            "endangerment": aes["label"],
        })

    result.sort(key=lambda x: x["last_documented"])

    return {
        "count": len(result),
        "threshold_year": before,
        "languages": result,
    }