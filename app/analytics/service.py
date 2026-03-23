# analytics/service.py

from sqlmodel import Session, select
from app.models.models import Language, LanguageSetItem
from app.analytics import algorithms


def get_similarity(session: Session, lang1_id: str, lang2_id: str):
    # fetch both languages from DB

    l1 = session.get(Language, lang1_id)
    l2 = session.get(Language, lang2_id)

    if not l1 or not l2:
        return None  # handled in route

    score = algorithms.compute_similarity(l1, l2)
    insight = algorithms.interpret_similarity(score)

    return {
        "language1": l1.name,
        "language2": l2.name,
        "similarity_score": round(score, 2),
        "insight": insight,
    }


def compare_language_sets(session: Session, set1_id: int, set2_id: int):
    # get items for both sets

    items1 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set1_id)
    ).all()

    items2 = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set2_id)
    ).all()

    ids1 = {i.language_id for i in items1}
    ids2 = {i.language_id for i in items2}

    shared = ids1 & ids2  # intersection
    unique1 = ids1 - ids2
    unique2 = ids2 - ids1

    overlap_ratio = len(shared) / max(len(ids1), 1)  # avoid division by zero

    return {
        "shared_count": len(shared),
        "unique_set1": len(unique1),
        "unique_set2": len(unique2),
        "overlap_ratio": round(overlap_ratio, 2),
    }

