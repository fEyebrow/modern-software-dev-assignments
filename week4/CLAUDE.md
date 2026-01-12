# Week 4 Developer's Command Center - Repository Guide

This is a minimal full-stack FastAPI + SQLite application designed as a "developer's command center" for practicing agent-driven workflows.

## Environment Setup

**IMPORTANT**: All commands must be run from the `week4/` directory.

- **Conda environment**: `cs146s` (path: `/opt/miniconda3/envs/cs146s`)
- **Dependency management**: Poetry (`pyproject.toml` in parent directory)

### Running Commands

所有命令统一格式：
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run <command>
```

示例：
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make test
/opt/miniconda3/bin/conda run -n cs146s poetry run make run
/opt/miniconda3/bin/conda run -n cs146s poetry run make format
/opt/miniconda3/bin/conda run -n cs146s poetry run make lint
/opt/miniconda3/bin/conda run -n cs146s poetry run pre-commit run --all-files
```

### Initial Setup
1. (Optional) Install pre-commit: `/opt/miniconda3/bin/conda run -n cs146s poetry run pre-commit install`
2. Verify: `/opt/miniconda3/bin/conda run -n cs146s poetry run make run` → http://localhost:8000

## Project Structure

```
backend/
  app/
    routers/          # API route handlers (notes, action_items)
    services/         # Business logic (extract.py)
    main.py          # FastAPI app entry point
    db.py            # Database setup and seeding
    models.py        # SQLAlchemy models
    schemas.py       # Pydantic schemas
  tests/             # Pytest test suite

frontend/            # Static HTML/JS/CSS (no build step)
  index.html        # Main UI
  app.js            # Frontend logic
  styles.css        # Styling

data/
  seed.sql          # Database seed data
  dev.db            # SQLite database (generated on startup)

docs/
  TASKS.md          # 7 practice tasks for agent-driven development
```

## Quick Start

### Running the Application
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make run
```
- Frontend: http://localhost:8000
- API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### Testing
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make test
```

### Code Quality
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make format  # Auto-format with black + ruff --fix
/opt/miniconda3/bin/conda run -n cs146s poetry run make lint    # Check with ruff (no changes)
```

### Database
The database is automatically created and seeded on startup (see `backend/app/db.py:apply_seed_if_needed()`).

To manually re-seed:
```bash
/opt/miniconda3/bin/conda run -n cs146s poetry run make seed
```

## Code Style and Safety Guardrails

### Tooling Expectations
- **Formatter**: black (PEP 8 compliant)
- **Linter**: ruff (fast Python linter)
- **Pre-commit**: Use `pre-commit install` to enable hooks (optional but recommended)
- **Tests**: pytest with simple assertions

### Safe Commands

所有命令统一使用 `/opt/miniconda3/bin/conda run -n cs146s poetry run <command>` 格式：

- `poetry run make run` - Start the dev server (sets PYTHONPATH automatically)
- `poetry run make test` - Run all tests (sets PYTHONPATH automatically)
- `poetry run make seed` - Re-apply database seed
- `poetry run make format` - Auto-format code with black + ruff
- `poetry run make lint` - Check code quality with ruff
- `poetry run pre-commit install` - Install git hooks
- `poetry run pre-commit run --all-files` - Run all pre-commit hooks

### Commands to Avoid
- Direct database mutations outside of `seed.sql` or migration scripts
- Manual editing of auto-generated files
- Running commands that import project code without `poetry run` (e.g., pytest, uvicorn directly)
- Running `uvicorn` directly without PYTHONPATH (use `poetry run make run` instead)
- Running pytest directly without PYTHONPATH (use `poetry run make test` instead)

## Development Workflows

通用模式（TDD）：

```
                              ┌───────────────────┐
                              │ 文件 > 500 行?    │
                              │ Yes: Refactor     │
                              │ No:  跳过         │
                              └───────────────────┘
                                       │
  Red ──────────→ Green ──────────→ Refactor? ─────────→ Lint ──────→ Commit
   │                │                   │                  │
   ▼                ▼                   ▼                  ▼
  写失败        ┌──────┐            ┌──────┐           ┌──────┐
  的测试        │ 运行 │←───┐       │ 运行 │←───┐      │ 运行 │←───┐
                │ 测试 │    │       │ 测试 │    │      │ lint │    │
                └──┬───┘    │       └──┬───┘    │      └──┬───┘    │
                   │        │          │        │         │        │
              ┌────┴────┐   │     ┌────┴────┐   │    ┌────┴────┐   │
              ▼         ▼   │     ▼         ▼   │    ▼         ▼   │
            通过      失败   │   通过      失败    │   通过      失败  │
              │         │   │     │         │   │     │         │  │
              │         ▼   │     │         ▼   │     │         ▼  │
              │       修复──┘     │       修复──┘     │       修复─┘
              │                   │                   │
              ▼                   ▼                   ▼
           下一步              下一步               Commit
```

核心循环：
1. **Red**: 写一个失败的测试
2. **Green**: 写最少的代码让测试通过（测试失败 → 修复 → 重跑，直到通过）
3. **Refactor**（可选）: 单个文件 > 500 行时考虑重构（测试失败 → 修复 → 重跑，直到通过）
4. **Lint**: 运行 lint（失败 → 修复 → 重跑，直到通过）
5. **Commit**: 全部通过后提交

### Adding a New API Endpoint
1. **Write a failing test first** in `backend/tests/test_<module>.py`
2. **Implement the route** in appropriate router (`backend/app/routers/`)
3. **Add/update schemas** in `backend/app/schemas.py` if needed
4. **Run tests** with `poetry run make test` to verify
5. **Run linter** with `make lint` to check code quality
6. **Commit** changes with descriptive message

### Modifying Database Schema
1. **Write a failing test first** for the feature that needs the schema change
2. **Update seed.sql** in `data/seed.sql` with new schema
3. **Update models.py** with corresponding SQLAlchemy models
4. **Update schemas.py** if API input/output changes
5. **Migrate the database**: 用 `sqlite3 data/dev.db` 执行 ALTER TABLE 语句
6. **Implement the feature** (routes, services, etc.)
7. **Run tests** with `poetry run make test` to verify
8. **Run format + lint**, fix issues if any
9. **Commit** changes with descriptive message

### Adding Frontend Features
1. **Update `frontend/app.js`** with new logic
2. **Update `frontend/index.html`** if UI changes needed


### Refactoring a Module
1. **Run tests first** to establish baseline (`poetry run make test`)
2. **Make the refactor** (rename, restructure, etc.)
3. **Update imports** across the codebase
4. **Run tests again** to ensure nothing broke
5. **Run format + lint** with `make format` then `make lint`, fix any issues
6. **Commit** changes with descriptive message

## Key Files and Entry Points

### Backend Entry Points
- `backend/app/main.py` - FastAPI application setup
- `backend/app/routers/notes.py` - Notes CRUD endpoints
- `backend/app/routers/action_items.py` - Action items endpoints
- `backend/app/services/extract.py` - Text extraction logic

### Frontend Entry Points
- `frontend/index.html` - Main UI structure
- `frontend/app.js` - API calls and DOM manipulation

### Test Entry Points
- `backend/tests/test_notes.py` - Notes endpoint tests
- `backend/tests/test_action_items.py` - Action items tests
- `backend/tests/test_extract.py` - Extract service tests

## Tips for Working with This Repo

- **Always use poetry run**: All commands must be run through `poetry run`. Dependencies are managed by Poetry and won't be available otherwise
- **Conda environment**: Use `/opt/miniconda3/bin/conda run -n cs146s poetry run <command>`
- **Use make commands**: They set up PYTHONPATH and other environment variables correctly
- **Context is key**: Always read existing code before modifying
- **Test-driven**: Write tests first when adding new features
- **Keep it simple**: This is a minimal app - don't over-engineer
- **Check the docs**: API documentation at `/docs` is auto-generated and always up-to-date
- **Embrace iteration**: Development is rarely linear. Expect to run test → fix → test cycles multiple times
- **Verify at each step**: After making changes, always run the full validation pipeline: `poetry run make test` → `poetry run make format` → `poetry run make lint`

## Custom Slash Commands

Custom slash commands are defined in `.claude/commands/*.md`. These are reusable workflows that can be invoked with `/command-name`.

To create a new command:
1. Create a new `.md` file in `.claude/commands/`
2. Define the workflow in markdown format
3. Use `$ARGUMENTS` to accept optional parameters
4. Invoke with `/command-name [arguments]`

See `.claude/commands/` for examples.
