from datetime import datetime, UTC
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.models import LanguageSet, LanguageSetItem, Language
from app.security import verify_api_key, require_user, require_admin

router = APIRouter(
    prefix="/language-sets",
    tags=["Language Sets"],
    dependencies=[Depends(verify_api_key)],
)


def now_utc():
    return datetime.now(UTC)


# -----------------------
# SCHEMAS
# -----------------------


class LanguageSetCreate(BaseModel):
    title: str
    description: Optional[str] = None
    notes: Optional[str] = None


class LanguageSetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class LanguageSetItemCreate(BaseModel):
    language_id: str


# -----------------------
# CRUD
# -----------------------


@router.post("")
def create_language_set(
    payload: LanguageSetCreate,
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


@router.get("")
def list_language_sets(session: Session = Depends(get_session)):
    return session.exec(select(LanguageSet)).all()


@router.get("/{set_id}")
def get_language_set(set_id: int, session: Session = Depends(get_session)):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Language set not found")
    return obj


@router.patch("/{set_id}")
def update_language_set(
    set_id: int,
    payload: LanguageSetUpdate,
    session: Session = Depends(get_session),
):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Language set not found")

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


@router.delete("/{set_id}")
def delete_language_set(
    set_id: int,
    session: Session = Depends(get_session),
    token: dict = Depends(require_admin),  # 🔐 ADMIN REQUIRED
):
    obj = session.get(LanguageSet, set_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Language set not found")

    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    for item in items:
        session.delete(item)

    session.delete(obj)
    session.commit()

    return {"message": "Language set deleted"}


# -----------------------
# ITEMS
# -----------------------


@router.post("/{set_id}/items")
def add_item(
    set_id: int,
    payload: LanguageSetItemCreate,
    session: Session = Depends(get_session),
):
    if not session.get(LanguageSet, set_id):
        raise HTTPException(status_code=404, detail="Language set not found")

    if not session.get(Language, payload.language_id):
        raise HTTPException(status_code=404, detail="Language not found")

    exists = session.exec(
        select(LanguageSetItem).where(
            LanguageSetItem.language_set_id == set_id,
            LanguageSetItem.language_id == payload.language_id,
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Language already in set")

    item = LanguageSetItem(language_set_id=set_id, language_id=payload.language_id)

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


@router.get("/{set_id}/items")
def list_items(set_id: int, session: Session = Depends(get_session)):
    if not session.get(LanguageSet, set_id):
        raise HTTPException(status_code=404, detail="Language set not found")

    items = session.exec(
        select(LanguageSetItem).where(LanguageSetItem.language_set_id == set_id)
    ).all()

    result = []

    for item in items:
        lang = session.get(Language, item.language_id)
        if lang:
            result.append(
                {
                    "item_id": item.id,
                    "language_id": lang.id,
                    "name": lang.name,
                    "macroarea": lang.macroarea,
                    "level": lang.level,
                }
            )

    return result


@router.delete("/{set_id}/items/{item_id}")
def delete_item(set_id: int, item_id: int, session: Session = Depends(get_session)):
    item = session.get(LanguageSetItem, item_id)

    if not item or item.language_set_id != set_id:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(item)
    session.commit()

    return {"message": "Language removed from set"}
