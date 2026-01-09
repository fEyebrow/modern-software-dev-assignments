# Implementation Plan: Add Search Endpoint for Notes (Case-Insensitive)

## Task Overview
Extend the existing `GET /notes/search?q=...` endpoint to support case-insensitive search, add frontend search UI, and ensure comprehensive test coverage using TDD approach.

## Environment Setup
This project uses **Poetry** for dependency management. The `pyproject.toml` is located in the parent directory (`../pyproject.toml`).

All commands must be run with the correct environment:
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run <command>
```

Examples:
- Run tests: `/opt/miniconda3/bin/conda run -n cs146s poetry run make test`
- Format code: `/opt/miniconda3/bin/conda run -n cs146s poetry run make format`
- Run linter: `/opt/miniconda3/bin/conda run -n cs146s poetry run make lint`
- Start server: `/opt/miniconda3/bin/conda run -n cs146s poetry run make run`

## Implementation Steps (TDD Approach)

### Step 1: Write Failing Tests First
**File**: `backend/tests/test_notes.py`

Add tests for:
1. Case-insensitive search (e.g., search "hello" finds "HELLO")
2. Search matching title only
3. Search matching content only
4. Search with no results (returns empty list)
5. Search with empty query (returns all notes)

### Step 2: Implement Case-Insensitive Search
**File**: `backend/app/routers/notes.py`

Modify the search endpoint to use SQLAlchemy's `func.lower()` for case-insensitive matching:
```python
from sqlalchemy import func

# Change from:
Note.title.contains(q) | Note.content.contains(q)

# To:
func.lower(Note.title).contains(q.lower()) | func.lower(Note.content).contains(q.lower())
```

### Step 3: Add Frontend Search UI
**File**: `frontend/index.html`

Add search input and button in the Notes section (above the notes list):
```html
<div class="search-container">
  <input type="text" id="note-search" placeholder="Search notes...">
  <button id="search-btn">Search</button>
  <button id="clear-search-btn">Clear</button>
</div>
```

**File**: `frontend/app.js`

Add search functionality (复用现有列表，不创建新列表):
1. `searchNotes(query)` - fetch from `/notes/search?q={query}`，结果渲染到现有的 `<ul id="notes">`
2. `renderNotes(notes)` - 提取渲染逻辑为独立函数，供 `loadNotes()` 和 `searchNotes()` 复用
3. Event listener for search button - 调用 `searchNotes()`
4. Event listener for clear button - 调用 `loadNotes()` 恢复显示所有笔记
5. Event listener for Enter key on search input - 支持按Enter键快速搜索
6. 搜索无结果时显示提示信息（"No results found"）

**渲染逻辑模块化**:
```javascript
// 提取渲染函数
function renderNotes(notes) {
  const ul = document.getElementById('notes');
  ul.innerHTML = '';
  if (notes.length === 0) {
    ul.innerHTML = '<li>无结果</li>';
    return;
  }
  notes.forEach(note => {
    const li = document.createElement('li');
    li.textContent = `${note.title}: ${note.content}`;
    ul.appendChild(li);
  });
}

// loadNotes 复用 renderNotes
async function loadNotes() {
  const notes = await fetchJSON('/notes/');
  renderNotes(notes);
}

// searchNotes 复用 renderNotes
async function searchNotes(query) {
  const notes = await fetchJSON(`/notes/search?q=${encodeURIComponent(query)}`);
  renderNotes(notes);
}
```

### Step 4: 验证

#### 4.1 运行测试
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make test
```

**如果测试失败：**
1. 查看错误信息，定位失败的测试用例
2. 分析失败原因（断言错误、异常、逻辑问题）
3. 修复对应的代码
4. 重新运行测试，重复直到通过

#### 4.2 代码质量检查
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make format
/opt/miniconda3/bin/conda run -n cs146s poetry run make lint
```

**如果 lint 失败：**
1. `make format` 已自动修复格式问题
2. 手动修复 lint 报告的剩余警告
3. 重新运行 `make lint`，重复直到通过

#### 4.3 API 手动测试
启动服务器：
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make run
```

在另一个终端测试API：
```bash
# 测试大小写不敏感搜索
curl "http://localhost:8000/notes/search/?q=hello"

# 测试空查询返回所有笔记
curl "http://localhost:8000/notes/search/?q="

# 测试不存在的查询返回空数组
curl "http://localhost:8000/notes/search/?q=NonExistentQuery123"
```

**如果 API 行为不符合预期：**
1. 检查返回的错误信息或响应内容
2. 查看终端中的服务器日志
3. 定位并修复 `backend/app/routers/notes.py` 中的问题
4. 重新运行测试确保测试仍通过
5. 再次执行 curl 测试，重复直到通过
