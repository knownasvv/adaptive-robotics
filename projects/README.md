# Project tests

## Run tests

Use Python 3.11 or newer. From the repository root:

```bash
cd projects
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

The shared virtual environment lives in `.venv` under this directory. If it already exists, activate it without recreating it. You can also use `.venv/bin/python` instead of `python` in the commands below without activating it.

From this directory:

```bash
# All projects
python -m pytest -v

# One project
python -m pytest 01-decision-playground -v

# One test module
python -m pytest 01-decision-playground/_tests/test_planner.test.py -v

# Scenarios matching a name
python -m pytest 01-decision-playground -k detour -v
```

The shared [pytest configuration](pytest.ini) discovers tests recursively and supports `test_*.py`, `*_test.py`, and `*.test.py` filenames. Importlib mode supports the dotted filenames without conventional module-name imports. The playground directory is added to the import path so its `engine` and `data` imports work.

Tests are standalone functions: each parameter row is collected independently with a descriptive ID. Movement cases specify their own starting position rather than relying on earlier tests.

When adding projects, prefer unique package names rather than reusing top-level names such as `engine` and `data`; importlib mode does not isolate application packages between projects.
