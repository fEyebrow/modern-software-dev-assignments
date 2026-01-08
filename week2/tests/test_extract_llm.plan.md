# 单元测试计划：`extract_action_items_llm()`

## 概述

为 `week2/app/services/extract.py` 中的 `extract_action_items_llm()` 函数编写单元测试，覆盖多种输入场景。

## 文件结构

```
week2/
├── app/
│   └── services/
│       └── extract.py          # 被测代码（已存在）
├── tests/
│   ├── __init__.py             # 已存在
│   ├── test_extract.py         # 测试文件（在此添加）
│   └── test_extract_llm.plan.md # 本计划文件
└── pytest.ini                  # pytest 标记配置（新建）
```

## 测试策略

### 分层测试

1. **单元测试（Mock）**：测试代码逻辑（去重、异常处理），快速、确定性
2. **集成测试（真实 LLM）**：验证 prompt 效果，需要 Ollama 运行

### Mock 路径

```python
@patch("week2.app.services.extract.chat")
```

## 测试用例列表

| 类别 | 测试函数 | Mock? | 描述 |
|-----|---------|-------|------|
| 去重 | `test_removes_duplicates` | 否 | 去重基本功能 |
| 去重 | `test_case_insensitive` | 否 | 大小写不敏感去重 |
| 去重 | `test_preserves_order` | 否 | 保持原始顺序 |
| 单元 | `test_llm_error_raises_exception` | 是 | 异常处理 |
| 集成 | `test_bullet_list` | 否 | Bullet list 输入 |
| 集成 | `test_keyword_prefixed` | 否 | TODO/ACTION 前缀 |
| 集成 | `test_empty_input` | 否 | 空输入 |

## 代码结构

```python
# week2/tests/test_extract.py

import json
import pytest
from unittest.mock import patch, MagicMock

from ..app.services.extract import (
    extract_action_items_llm,
    ActionItemExtractionError,
    _deduplicate,
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
```

## pytest.ini 配置

```ini
# week2/pytest.ini
[pytest]
markers =
    integration: marks tests as integration tests (require Ollama running)
```

## 运行命令

```bash
# 在 week2 目录下运行
cd week2

# 只跑单元测试（快速，不需要 Ollama）
pytest tests/test_extract.py -m "not integration"

# 跑所有测试（包括集成测试，需要 Ollama 运行）
pytest tests/test_extract.py

# 只跑集成测试
pytest tests/test_extract.py -m integration
```

## 集成测试断言策略

由于 LLM 输出有不确定性，断言需要更灵活：

```python
# ❌ 不好：精确匹配（LLM 可能改写措辞）
assert result == ["Set up database", "Implement API endpoint"]

# ✅ 好：验证关键内容存在
assert any("database" in item.lower() for item in result)

# ✅ 好：验证数量在合理范围
assert len(result) >= 2

# ✅ 好：验证返回类型正确
assert all(isinstance(item, str) for item in result)
```

## 实现步骤

| 步骤 | 任务 | 状态 |
|-----|------|------|
| 1 | 在 test_extract.py 中添加 import 和 helper | pending |
| 2 | 实现 TestDeduplicate 测试类 | pending |
| 3 | 实现 TestExtractActionItemsLLMUnit 测试类 | pending |
| 4 | 实现 TestExtractActionItemsLLMIntegration 测试类 | pending |
| 5 | 创建 pytest.ini 配置文件 | pending |
| 6 | 运行测试验证 | pending |
