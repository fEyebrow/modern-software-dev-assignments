from __future__ import annotations

import json

from ollama import chat


class ActionItemExtractionError(Exception):
    """待办事项提取失败"""

    pass


def _extract_with_llm(text: str) -> list[str]:
    prompt = f"""从以下文本中提取所有待办事项/行动项。
返回 JSON 对象，格式为: {{"items": ["待办事项1", "待办事项2"]}}
如果没有待办事项，返回: {{"items": []}}

文本：
{text}
"""
    try:
        response = chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0},
            format="json",
        )
        content = response.message.content
        if content is None:
            raise ValueError("LLM response content is None")

        result = json.loads(content)
        items: list[str] = result.get("items", [])
        return items
    except Exception as e:
        raise ActionItemExtractionError(f"LLM 提取失败: {e}") from e


def _deduplicate(items: list[str]) -> list[str]:
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> list[str]:
    items = _extract_with_llm(text)
    return _deduplicate(items)
