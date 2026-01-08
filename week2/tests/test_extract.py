import json
from unittest.mock import MagicMock, patch

import pytest

from ..app.services.extract import (
    ActionItemExtractionError,
    _deduplicate,
    extract_action_items_llm,
)


def _mock_llm_response(items: list[str]):
    """创建模拟的 ollama.chat 响应对象"""
    mock_response = MagicMock()
    mock_response.message.content = json.dumps({"items": items})
    return mock_response


# ============ 单元测试 ============


class TestDeduplicate:
    """_deduplicate 纯函数测试"""

    def test_removes_duplicates(self):
        items = ["Task A", "Task B", "Task A"]
        result = _deduplicate(items)
        assert result == ["Task A", "Task B"]

    def test_case_insensitive(self):
        items = ["Task A", "task a", "TASK A"]
        result = _deduplicate(items)
        assert result == ["Task A"]  # 保留第一个

    def test_preserves_order(self):
        items = ["C", "A", "B"]
        result = _deduplicate(items)
        assert result == ["C", "A", "B"]


class TestExtractActionItemsLLMUnit:
    """extract_action_items_llm 单元测试（mock LLM）"""

    @patch("week2.app.services.extract.chat")
    def test_llm_error_raises_exception(self, mock_chat):
        """验证 LLM 调用失败时抛出自定义异常"""
        mock_chat.side_effect = Exception("Connection failed")

        with pytest.raises(ActionItemExtractionError) as exc_info:
            extract_action_items_llm("Some text")

        assert "LLM 提取失败" in str(exc_info.value)


# ============ 集成测试（真实 LLM） ============


@pytest.mark.integration
class TestExtractActionItemsLLMIntegration:
    """真实调用 LLM 的集成测试"""

    def test_bullet_list(self):
        """验证 LLM 能正确识别 bullet list"""
        text = """
        Meeting notes:
        - Set up database
        - Implement API endpoint
        - Write documentation
        """
        result = extract_action_items_llm(text)

        assert len(result) >= 2
        result_lower = [item.lower() for item in result]
        assert any("database" in item for item in result_lower)

    def test_keyword_prefixed(self):
        """验证 LLM 能识别 TODO/ACTION 等关键词"""
        text = """
        TODO: Review pull request
        ACTION: Schedule meeting
        Some random text here.
        """
        result = extract_action_items_llm(text)

        assert len(result) >= 1
        result_lower = [item.lower() for item in result]
        assert any("review" in item or "pull request" in item for item in result_lower)

    def test_empty_input(self):
        """验证空输入返回空列表"""
        result = extract_action_items_llm("")
        assert result == []
