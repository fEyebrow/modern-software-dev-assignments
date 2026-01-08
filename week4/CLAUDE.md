# Week 4 Developer's Command Center - Repository Guide

This is a minimal full-stack FastAPI + SQLite application designed as a "developer's command center" for practicing agent-driven workflows.

## Environment Setup

### Prerequisites
- **Python environment**: This project requires the `cs146s` conda environment
- **Conda path**: `/opt/miniconda3`
- **Environment path**: `/opt/miniconda3/envs/cs146s`

### Activating the Environment

**For interactive shell (zsh/bash terminal):**
```bash
conda activate cs146s
```

**For non-interactive shell (Claude Code / AI agents):**
Use `conda run` to execute commands without activating the environment:
```bash
/opt/miniconda3/bin/conda run -n cs146s <command>
```

Examples:
```bash
/opt/miniconda3/bin/conda run -n cs146s pre-commit run --all-files
/opt/miniconda3/bin/conda run -n cs146s pytest
/opt/miniconda3/bin/conda run -n cs146s make test
```

### Initial Setup Steps
1. Activate the conda environment (see above)

2. (Optional but recommended) Install pre-commit hooks:
   ```bash
   # Interactive shell
   pre-commit install
   
   # Non-interactive shell (Claude Code)
   /opt/miniconda3/bin/conda run -n cs146s pre-commit install
   ```

3. Verify setup by running the app:
   ```bash
   make run
   ```

4. Open http://localhost:8000 for the frontend and http://localhost:8000/docs for API docs

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

**IMPORTANT**: All commands must be run from the `week4/` directory with the `cs146s` conda environment activated.

### Running the Application
```bash
make run          # Start server at http://localhost:8000
```
- Frontend: http://localhost:8000
- API docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

### Testing
```bash
make test         # Run pytest suite
```

### Code Quality
```bash
make format       # Auto-format with black + ruff --fix
make lint         # Check with ruff (no changes)
```

### Database
The database is automatically created and seeded on startup (see `backend/app/db.py:apply_seed_if_needed()`).

To manually re-seed:
```bash
make seed
```

## Code Style and Safety Guardrails

### Tooling Expectations
- **Formatter**: black (PEP 8 compliant)
- **Linter**: ruff (fast Python linter)
- **Pre-commit**: Use `pre-commit install` to enable hooks (optional but recommended)
- **Tests**: pytest with simple assertions

### Safe Commands
- `make run` - Start the dev server (sets PYTHONPATH automatically)
- `make test` - Run all tests (sets PYTHONPATH automatically)
- `make format` - Auto-format code
- `make lint` - Check code quality
- `make seed` - Re-apply database seed

### Commands to Avoid
- Direct database mutations outside of `seed.sql` or migration scripts
- Manual editing of auto-generated files
- Running `uvicorn` directly without PYTHONPATH (use `make run` instead)
- Running pytest without PYTHONPATH (use `make test` instead)

### Gates Before Committing
1. Run `make format` to ensure code is formatted
2. Run `make lint` to check for issues
3. Run `make test` to ensure tests pass
4. (Optional) Run `pre-commit run --all-files` if hooks are installed

## Development Workflows

### Adding a New API Endpoint
1. **Write a failing test first** in `backend/tests/test_<module>.py`
2. **Implement the route** in appropriate router (`backend/app/routers/`)
3. **Add/update schemas** in `backend/app/schemas.py` if needed
4. **Run tests** with `make test` to verify
5. **Run linter** with `make lint` to check code quality
6. **Update docs** if you're tracking API changes (see docs/TASKS.md #7)

### Modifying Database Schema
1. **Update seed.sql** in `data/seed.sql` with new schema
2. **Update models.py** with corresponding SQLAlchemy models
3. **Delete dev.db** to force recreation: `rm data/dev.db`
4. **Restart the app** with `make run`
5. **Update tests** to reflect schema changes

### Adding Frontend Features
1. **Update `frontend/app.js`** with new logic
2. **Update `frontend/index.html`** if UI changes needed
3. **Test manually** at http://localhost:8000
4. **Add backend tests** for any new API interactions

### Refactoring a Module
1. **Run tests first** to establish baseline (`make test`)
2. **Make the refactor** (rename, restructure, etc.)
3. **Update imports** across the codebase
4. **Run tests again** to ensure nothing broke
5. **Run lint** with `make lint` and fix any issues
6. **Format code** with `make format`

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

## Practice Tasks

See `docs/TASKS.md` for 7 practice tasks designed for agent-driven workflows:
1. Enable pre-commit and fix the repo
2. Add search endpoint for notes
3. Complete action item flow
4. Improve extraction logic
5. Notes CRUD enhancements
6. Request validation and error handling
7. Docs drift check

## Tips for Working with This Repo

- **Conda environment**: Use `conda activate cs146s` (interactive) or `/opt/miniconda3/bin/conda run -n cs146s <command>` (non-interactive/AI agents)
- **Use make commands**: They set up PYTHONPATH and other environment variables correctly
- **Context is key**: Always read existing code before modifying
- **Test-driven**: Write tests first when adding new features
- **Keep it simple**: This is a minimal app - don't over-engineer
- **Check the docs**: API documentation at `/docs` is auto-generated and always up-to-date

## Custom Slash Commands

Custom slash commands are defined in `.claude/commands/*.md`. These are reusable workflows that can be invoked with `/command-name`.

To create a new command:
1. Create a new `.md` file in `.claude/commands/`
2. Define the workflow in markdown format
3. Use `$ARGUMENTS` to accept optional parameters
4. Invoke with `/command-name [arguments]`

See `.claude/commands/` for examples.
