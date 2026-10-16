# Robot Decision-Making Playground

## Run tests

Use Python 3.10 or newer. From the repository root:

```bash
cd projects/01-decision-playground
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

The pytest configuration adds this project directory to the import path so `engine` and `data` imports work. Tests are standalone functions: each parameter row is collected independently with a descriptive ID. Movement cases specify their own starting position rather than relying on earlier tests.

Run a subset with `python -m pytest _tests/test_planner.py -v` or `python -m pytest -k detour -v`.
