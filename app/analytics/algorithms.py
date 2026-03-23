# analytics/algorithms.py

from app.models.models import Language


def compute_similarity(l1: Language, l2: Language) -> float:
    # simple scoring based on shared attributes

    score = 0.0

    if l1.family_id and l2.family_id and l1.family_id == l2.family_id:
        score += 0.5  # same family is the strongest signal

    if l1.macroarea and l2.macroarea and l1.macroarea == l2.macroarea:
        score += 0.3  # same region gives moderate similarity

    if l1.level and l2.level and l1.level == l2.level:
        score += 0.1  # same classification level adds a bit

    if getattr(l1, "is_isolate", False) or getattr(l2, "is_isolate", False):
        score -= 0.2  # isolates are less likely to be related

    return max(0.0, min(score, 1.0))  # keep score between 0 and 1


def interpret_similarity(score: float) -> str:
    # convert score into something more readable

    if score > 0.7:
        return "Closely related languages"
    elif score > 0.4:
        return "Moderately related"
    else:
        return "Distantly related"
