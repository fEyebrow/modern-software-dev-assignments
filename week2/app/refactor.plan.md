# Week2 后端代码重构方案

> **重要提示**：在执行任何命令行操作（如运行 mypy）之前，请确保已激活 conda 环境：
> ```bash
> conda activate cs146
> ```

## 任务列表

| 任务 | 说明 | 状态 |
|------|------|------|
| setup-mypy | 安装 mypy 并添加配置到 pyproject.toml | pending |
| create-schemas | 创建 schemas.py 定义 Pydantic 请求/响应模型 | pending |
| refactor-db | 重构 db.py：添加 dataclass 模型，新增 get_action_item() | pending |
| refactor-main | 修改 main.py 使用 lifespan 管理应用生命周期 | pending |
| refactor-notes-router | 重构 notes.py 路由使用 Schema 类型 | pending |
| refactor-action-items-router | 重构 action_items.py 路由并增强错误处理 | pending |
| run-mypy | 运行 mypy 验证类型（**需先激活环境**） | pending |

---

## 详细步骤

### 第一步：创建 Pydantic Schemas

创建 [`week2/app/schemas.py`](week2/app/schemas.py)，定义所有请求和响应的强类型模型。

### 第二步：改进数据库层

修改 [`week2/app/db.py`](week2/app/db.py)：
1. 定义 `Note` 和 `ActionItem` dataclasses
2. 实现 Row 到 dataclass 的转换函数
3. 将所有数据库函数返回值改为 dataclass 类型
4. 新增 `get_action_item()` 函数

### 第三步：优化应用生命周期

修改 [`week2/app/main.py`](week2/app/main.py)，使用 `lifespan` 上下文管理器替代模块级别的 `init_db()` 调用。

### 第四步：增强错误处理

重构路由文件：
- [`week2/app/routers/notes.py`](week2/app/routers/notes.py)
- [`week2/app/routers/action_items.py`](week2/app/routers/action_items.py)

使用 Schemas 作为参数和返回值，并添加明确的 HTTPException 处理（如 404 Not Found）。

### 第五步：配置 mypy

在 [`pyproject.toml`](pyproject.toml) 中添加 mypy 依赖和配置：

```toml
[tool.poetry.group.dev.dependencies]
mypy = ">=1.8.0"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
ignore_missing_imports = true
exclude = ["tests/"]
```

### 第六步：运行 mypy 验证

**关键步骤**：
1. 打开终端
2. 运行 `conda activate cs146`
3. 运行 `poetry install`
4. 运行 `poetry run mypy week2/app/`
