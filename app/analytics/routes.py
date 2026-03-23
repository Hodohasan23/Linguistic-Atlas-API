from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.models import Language, LanguageSetItem, ParameterValue, Parameter

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/similarity",
    summary="How closely related are two languages?",
    description="Estimate how closely two languages are related based on family, region, and isolate status.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "language1": "Somali",
                            "language2": "Oromo",
                            "similarity_score": 0.8,
                            "insight": "Closely related languages",
                            "explanation": ["Same language family", "Same macroarea"],
                        }
                    }
                }
            }
        }
    },
)
def language_similarity(
    lang1: str, lang2: str, session: Session = Depends(get_session)
):
    # fetch both languages from the database using their IDs
    l1 = session.get(Language, lang1)
    l2 = session.get(Language, lang2)

    # return 404 if either language does not exist
    if not l1 or not l2:
        raise HTTPException(status_code=404, detail="Language not found")

    # check if they share the same family or macroarea
    same_family = l1.family_id == l2.family_id
    same_macroarea = l1.macroarea == l2.macroarea

    score = 0
    reasons = []

    # same family is the strongest indicator of similarity
    if same_family:
        score += 0.5
        reasons.append("Same language family")

    # same macroarea suggests some regional similarity
    if same_macroarea:
        score += 0.3
        reasons.append("Same macroarea")

    # isolates are less likely to be related to anything
    if getattr(l1, "is_isolate", False) or getattr(l2, "is_isolate", False):
        score -= 0.2
        reasons.append("One or both languages are isolates")

    # ensure score stays within a valid range
    score = max(0, min(score, 1))

    # convert numeric score into a readable interpretation
    insight = (
        "Closely related languages"
        if score > 0.7
        else "Moderately related"
        if score > 0.4
        else "Distantly related"
    )

    return {
        "language1": l1.name,
        "language2": l2.name,
        "similarity_score": round(score, 2),
        "insight": insight,
        "explanation": reasons,
    }


@router.post(
    "/compare-sets",
    summary="Where do two Testimonies overlap?",
    description="Measure overlap and differences between two language sets, including shared and unique languages.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "shared_count": 4,
                            "unique_set1": 6,
                            "unique_set2": 3,
                            "overlap_ratio": 0.4,
                        }
                    }
                }
            }
        }
    },
)
def compare_sets(set1_id: int, set2_id: int, session: Session = Depends(get_session)):
    # retrieve all items for both language sets
    items1 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set1_id)
    ).all()

    items2 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set2_id)
    ).all()

    # extract just the language IDs into sets for easy comparison
    ids1 = {i.language_id for i in items1}
    ids2 = {i.language_id for i in items2}

    # compute overlap and differences between sets
    shared = ids1 & ids2
    unique1 = ids1 - ids2
    unique2 = ids2 - ids1

    return {
        "shared_count": len(shared),
        "unique_set1": len(unique1),
        "unique_set2": len(unique2),
        "overlap_ratio": round(len(shared) / max(len(ids1), 1), 2),
    }


@router.get(
    "/outliers",
    summary="Languages that slipped through the cracks",
    description="Identify languages that stand out due to missing data, isolate status, or limited parameter coverage.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "count": 2,
                            "outliers": [
                                {
                                    "language_id": "basq1248",
                                    "name": "Basque",
                                    "coverage": 3,
                                    "is_isolate": True,
                                    "reasons": [
                                        "Language isolate",
                                        "Very low parameter coverage",
                                    ],
                                },
                                {
                                    "language_id": "unkn1234",
                                    "name": "Unknown Language",
                                    "coverage": 0,
                                    "is_isolate": False,
                                    "reasons": [
                                        "Missing family classification",
                                        "Very low parameter coverage",
                                    ],
                                },
                            ],
                        }
                    }
                }
            }
        }
    },
)
def get_outliers(session: Session = Depends(get_session)):
    languages = session.exec(select(Language)).all()

    outliers = []

    for lang in languages:
        reasons = []

        # isolate = unusual by definition
        if lang.is_isolate:
            reasons.append("Language isolate")

        # missing classification is suspicious
        if not lang.family_id:
            reasons.append("Missing family classification")

        # check how many parameters exist
        param_count = session.exec(
            select(ParameterValue).where(ParameterValue.language_id == lang.id)
        ).all()

        coverage = len(param_count)

        if coverage < 10:
            reasons.append("Very low parameter coverage")

        if reasons:
            outliers.append(
                {
                    "language_id": lang.id,
                    "name": lang.name,
                    "coverage": coverage,
                    "is_isolate": lang.is_isolate,
                    "reasons": reasons,
                }
            )

    return {
        "count": len(outliers),
        "outliers": outliers[:50],
    }


@router.get(
    "/lineage/{language_id}",
    summary="Trace a language back to its oldest known ancestor",
    description="Follow a language up its classification tree to reveal its full linguistic ancestry.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "language_id": "stan1295",
                            "lineage": [
                                {"id": "afro1255", "name": "Afro-Asiatic"},
                                {"id": "cush1243", "name": "Cushitic"},
                                {"id": "east2699", "name": "East Cushitic"},
                                {"id": "stan1295", "name": "Somali"},
                            ],
                        }
                    }
                }
            }
        }
    },
)
def get_lineage(language_id: str, session: Session = Depends(get_session)):
    lineage = []

    current = session.get(Language, language_id)

    if not current:
        raise HTTPException(status_code=404, detail="Language not found")

    # walk up the tree until no parent exists
    while current:
        lineage.append(
            {
                "id": current.id,
                "name": current.name,
            }
        )

        if not current.family_id:
            break

        current = session.get(Language, current.family_id)

    lineage.reverse()

    return {
        "language_id": language_id,
        "lineage": lineage,
    }


@router.get(
    "/coverage/{language_id}",
    summary="How well documented is this language?",
    description="Evaluate how complete a language is based on how many typological parameters are recorded.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "language_id": "stan1295",
                            "parameter_count": 42,
                            "total_parameters": 200,
                            "coverage_score": 0.21,
                        }
                    }
                }
            }
        }
    },
)
def get_coverage(language_id: str, session: Session = Depends(get_session)):
    lang = session.get(Language, language_id)

    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")

    values = session.exec(
        select(ParameterValue).where(ParameterValue.language_id == language_id)
    ).all()

    total_parameters = session.exec(select(Parameter)).all()

    coverage_score = len(values) / max(len(total_parameters), 1)

    return {
        "language_id": language_id,
        "parameter_count": len(values),
        "total_parameters": len(total_parameters),
        "coverage_score": round(coverage_score, 3),
    }


@router.get(
    "/language-sets/{set_id}/profile",
    summary="The DNA of a Testimony — families, regions, diversity",
    description="Generate a breakdown of a language set including family distribution, macroareas, and diversity score.",
    openapi_extra={
        "responses": {
            "200": {
                "content": {
                    "application/json": {
                        "example": {
                            "set_id": 1,
                            "total_languages": 10,
                            "family_distribution": {
                                "afro1255": 4,
                                "indo1319": 3,
                                "Unknown": 3,
                            },
                            "macroarea_distribution": {
                                "Africa": 5,
                                "Eurasia": 3,
                                "North America": 2,
                            },
                            "diversity_score": 0.3,
                        }
                    }
                }
            }
        }
    },
)
def get_set_profile(set_id: int, session: Session = Depends(get_session)):
    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    if not items:
        raise HTTPException(status_code=404, detail="Set not found or empty")

    family_counts = {}
    macroarea_counts = {}

    for item in items:
        lang = session.get(Language, item.language_id)

        if not lang:
            continue

        family = lang.family_id or "Unknown"
        family_counts[family] = family_counts.get(family, 0) + 1

        macro = lang.macroarea or "Unknown"
        macroarea_counts[macro] = macroarea_counts.get(macro, 0) + 1

    total = len(items)
    diversity = len(family_counts) / max(total, 1)

    return {
        "set_id": set_id,
        "total_languages": total,
        "family_distribution": family_counts,
        "macroarea_distribution": macroarea_counts,
        "diversity_score": round(diversity, 3),
    }
