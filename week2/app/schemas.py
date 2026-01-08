from typing import Optional

from pydantic import BaseModel, Field

# === 请求 Schemas（前端发送给后端的数据格式）===


class NoteCreate(BaseModel):
    """创建笔记的请求格式"""

    content: str = Field(..., min_length=1, description="笔记内容，不能为空")


class ExtractRequest(BaseModel):
    """提取待办事项的请求格式"""

    text: str = Field(..., min_length=1, description="要提取的文本")
    save_note: bool = Field(default=False, description="是否同时保存为笔记")


class MarkDoneRequest(BaseModel):
    """标记完成状态的请求格式"""

    done: bool = Field(default=True, description="是否已完成")


# === 响应 Schemas（后端返回给前端的数据格式）===


class NoteResponse(BaseModel):
    """笔记响应格式"""

    id: int
    content: str
    created_at: str


class ActionItemBrief(BaseModel):
    """提取结果中的简略待办事项"""

    id: int
    text: str


class ActionItemResponse(BaseModel):
    """完整的待办事项响应格式"""

    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class ExtractResponse(BaseModel):
    """提取结果响应格式"""

    note_id: Optional[int]
    items: list[ActionItemBrief]
