# Assignment cost estimator

A Django tool for a two-year assignment from Switzerland to the UK. Day 1 provides a local Django server and an automated health check.

## Run locally

Use Python 3.12. Run these commands from the repository root in PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open [the health check](http://127.0.0.1:8000/healthz/). On macOS or Linux, use `python3.12` to create the environment and `.venv/bin/python` for the commands that follow.

## Run checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

To run the same style checks as CI, install `requirements-dev.txt`, then run `python -m ruff check .` and `python -m ruff format --check .` using the virtual environment's Python.

## AI tools used

ChatGPT (Codex) helped review the brief and research references, find and compare official engineering documentation, and draft the Day 1 starter and tests.
