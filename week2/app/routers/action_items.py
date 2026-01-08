from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import (
    ActionItemBrief,
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
)
from ..services.extract import ActionItemExtractionError, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    try:
        items = extract_action_items_llm(payload.text)
    except ActionItemExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"提取服务暂时不可用: {e}",
        )

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)

    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemBrief(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> List[ActionItemResponse]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r.id,
            note_id=r.note_id,
            text=r.text,
            done=r.done,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=ActionItemResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> ActionItemResponse:
    item = db.get_action_item(action_item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item {action_item_id} not found",
        )

    db.mark_action_item_done(action_item_id, payload.done)
    updated = db.get_action_item(action_item_id)

    # 理论上不会为 None，因为刚才检查过了，且我们没有并发删除
    if updated is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated item")

    return ActionItemResponse(
        id=updated.id,
        note_id=updated.note_id,
        text=updated.text,
        done=updated.done,
        created_at=updated.created_at,
    )
