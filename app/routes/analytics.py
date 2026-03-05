from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.models import Language, LanguageSetItem

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/similarity")
def language_similarity(
    lang1: str, lang2: str, session: Session = Depends(get_session)
):
    l1 = session.get(Language, lang1)
    l2 = session.get(Language, lang2)

    if not l1 or not l2:
        raise HTTPException(status_code=404, detail="Language not found")

    same_family = l1.family_id == l2.family_id
    same_macroarea = l1.macroarea == l2.macroarea

    score = 0
    if same_family:
        score += 0.5
    if same_macroarea:
        score += 0.3
    if l1.is_isolate or l2.is_isolate:
        score -= 0.2

    score = max(0, min(score, 1))

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
    }


@router.post("/compare-sets")
def compare_sets(set1_id: int, set2_id: int, session: Session = Depends(get_session)):
    items1 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set1_id)
    ).all()

    items2 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set2_id)
    ).all()

    ids1 = {i.language_id for i in items1}
    ids2 = {i.language_id for i in items2}

    shared = ids1 & ids2
    unique1 = ids1 - ids2
    unique2 = ids2 - ids1

    return {
        "shared_count": len(shared),
        "unique_set1": len(unique1),
        "unique_set2": len(unique2),
        "overlap_ratio": len(shared) / max(len(ids1), 1),
    }
