from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteResponse])
def list_all_notes() -> list[NoteResponse]:
    notes = db.list_notes()
    return [NoteResponse(id=n.id, content=n.content, created_at=n.created_at) for n in notes]


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreate) -> NoteResponse:
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    if not note:
        raise HTTPException(status_code=500, detail="Failed to create note")

    return NoteResponse(
        id=note.id,
        content=note.content,
        created_at=note.created_at,
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    note = db.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="note not found")

    return NoteResponse(
        id=note.id,
        content=note.content,
        created_at=note.created_at,
    )
