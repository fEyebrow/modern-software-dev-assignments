# Test Runner with Coverage

Run pytest test suite with coverage analysis and provide structured results.

## Usage

```
/test-runner [optional: test path or marker]
```

## Examples

- `/test-runner` - Run all tests with coverage
- `/test-runner backend/tests/test_notes.py` - Run specific test file
- `/test-runner backend/tests/test_notes.py::test_create_and_list_notes` - Run single test

## Steps

### 1. Environment Check

Check if we're in the correct directory:
- Verify `backend/tests/` directory exists
- If not, inform user they need to be in the `week4/` directory

Remind user about conda environment:
- Display message: "⚠️  Ensure conda environment 'cs146s' is activated with: `conda activate cs146s`"

### 2. Determine Test Target

Parse the `$ARGUMENTS` variable:
- If `$ARGUMENTS` is empty or not provided → set TARGET to `backend/tests`
- If `$ARGUMENTS` has a value → set TARGET to `$ARGUMENTS`

### 3. Run Tests

Execute the following command to run tests:

```bash
source /opt/miniconda3/etc/profile.d/conda.sh && conda activate cs146s && PYTHONPATH=. poetry run pytest -v ${TARGET} --maxfail=1 -x
```

Explanation:
- `source /opt/miniconda3/etc/profile.d/conda.sh` = Initialize conda in this shell session
- `conda activate cs146s` = Activate the project environment
- `PYTHONPATH=.` = Set Python module search path
- `poetry run pytest` = Run pytest in Poetry's virtual environment
- `-v ${TARGET}` = Run tests verbosely on target
- `--maxfail=1 -x` = Stop after first failure for fast feedback

Note: Commands are chained with `&&` to ensure each step succeeds before continuing.

### 4. Run Coverage Analysis (only if all tests passed)

If all tests passed in step 3, run coverage analysis:

```bash
source /opt/miniconda3/etc/profile.d/conda.sh && conda activate cs146s && PYTHONPATH=. poetry run pytest -v ${TARGET} --cov=backend/app --cov-report=term-missing
```

Explanation:
- Same as step 3, but adds coverage flags
- `--cov=backend/app` = Measure coverage of backend/app code
- `--cov-report=term-missing` = Show which lines are not covered
- No `--maxfail=1 -x` since we know tests pass

### 5. Parse and Display Results

Extract the following information from pytest output:

**Test Results (from step 3):**
- Total number of tests run
- Number of tests passed
- Number of tests failed
- Execution time

**Failure Information (if applicable, from step 3):**
- Complete pytest error output (including error type, traceback, and message)
- Test name and file location for building rerun command

**Coverage Data (from step 4, only if tests passed):**
- Overall coverage percentage
- Per-file coverage percentages (ONLY for files < 100%)
- Missing line numbers (from the "Missing" column)

### 6. Generate Structured Report

Create a clear, three-part output:

**Part 1: Test Results (Always show)**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If all tests pass:]
✅ All X tests passed in N.NNs

[If tests fail:]
❌ X/Y tests failed in N.NNs
```

**Part 2: Failure Details (Only if tests failed)**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Failure Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Show the complete pytest error output, including:]
- Error type (AssertionError, TypeError, etc.)
- Full traceback
- Error message
- Code context

💡 Next Steps:
   • Check source: [file:line from traceback]
   • Fix the error
   • Rerun: /test-runner [exact test path]
```

**Part 3: Coverage Analysis (Only show if all tests passed)**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Coverage Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Coverage: XX%

[If there are files with < 100% coverage:]
Files with incomplete coverage:

• backend/app/db.py                    49%  [Missing: 19-27, 32-40, 48, 52-56]
• backend/app/routers/notes.py         87%  [Missing: 44-47]
• backend/app/main.py                  95%  [Missing: 29]
• backend/app/routers/action_items.py  96%  [Missing: 31]

💡 Next Steps:
   • Add tests for uncovered lines
   • Run /test-runner to verify improvement

[If coverage < 80%:]
⚠️  Warning: Coverage below 80% target

[If all files have 100% coverage:]
✨ Perfect! All files have 100% coverage.
```

## Safety Notes

- This is a read-only operation (no code modifications)
- Uses `--maxfail=1 -x` for fail-fast behavior to save time
- Safe to run multiple times
- Requires pytest and pytest-cov to be installed in the active environment

## Expected Behavior

This command will:
1. Run your test suite
2. Generate coverage metrics
3. Stop at the first failure (if any)
4. Provide a clear summary of results
5. Show which code lines need test coverage
