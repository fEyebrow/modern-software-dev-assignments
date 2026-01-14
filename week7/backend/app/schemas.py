from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip_whitespace(v: str | None) -> str | None:
    """Strip whitespace from string fields. Returns None unchanged."""
    if v is None:
        return None
    stripped = v.strip()
    if not stripped:
        raise ValueError("Field cannot be empty or whitespace only")
    return stripped


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)

    _strip_fields = field_validator("title", "content")(_strip_whitespace)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1, max_length=10000)

    _strip_fields = field_validator("title", "content")(_strip_whitespace)


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)

    _strip_fields = field_validator("description")(_strip_whitespace)


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(BaseModel):
    description: str | None = Field(None, min_length=1, max_length=500)
    completed: bool | None = None

    _strip_fields = field_validator("description")(_strip_whitespace)
