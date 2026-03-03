from __future__ import annotations
from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field


def now_utc() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="USER", index=True)


class Language(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    macroarea: Optional[str] = Field(default=None, index=True)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    glottocode: Optional[str] = Field(default=None, index=True)
    iso_code: Optional[str] = Field(default=None, index=True)
    level: Optional[str] = Field(default=None, index=True)
    countries: Optional[str] = None
    family_id: Optional[str] = Field(default=None, index=True)
    language_id: Optional[str] = Field(default=None, index=True)
    closest_iso_code: Optional[str] = None
    first_year_of_documentation: Optional[int] = None
    last_year_of_documentation: Optional[int] = None
    is_isolate: Optional[bool] = None


class LanguageName(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: str = Field(index=True)
    language_id: str = Field(foreign_key="language.id", index=True)
    name: str = Field(index=True)
    provider: Optional[str] = None
    lang: Optional[str] = None


class Parameter(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    column_spec: Optional[str] = None
    type: Optional[str] = Field(default=None, index=True)
    info_url: Optional[str] = None
    datatype: Optional[str] = None
    source: Optional[str] = None


class Code(SQLModel, table=True):
    id: str = Field(primary_key=True)
    parameter_id: Optional[str] = Field(
        default=None, foreign_key="parameter.id", index=True
    )
    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None
    numerical_value: Optional[float] = None


class ParameterValue(SQLModel, table=True):
    id: str = Field(primary_key=True)
    language_id: str = Field(foreign_key="language.id", index=True)
    parameter_id: str = Field(foreign_key="parameter.id", index=True)
    value: Optional[str] = None
    code_id: Optional[str] = Field(default=None, foreign_key="code.id", index=True)
    comment: Optional[str] = None
    source: Optional[str] = None
    code_reference: Optional[str] = None


class Media(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: Optional[str] = None
    description: Optional[str] = None
    media_type: Optional[str] = Field(default=None, index=True)
    download_url: Optional[str] = None
    path_in_zip: Optional[str] = None


class Tree(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None
    tree_is_rooted: Optional[bool] = None
    tree_type: Optional[str] = Field(default=None, index=True)
    tree_branch_length_unit: Optional[str] = None
    media_id: Optional[str] = Field(default=None, foreign_key="media.id", index=True)
    source: Optional[str] = None


class LanguageSet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)


class LanguageSetItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    language_set_id: int = Field(foreign_key="languageset.id", index=True)
    language_id: str = Field(foreign_key="language.id", index=True)


class SetComparison(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    set_a_id: int = Field(foreign_key="languageset.id", index=True)
    set_b_id: int = Field(foreign_key="languageset.id", index=True)
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=now_utc)
