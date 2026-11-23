# Assignment cost estimator

A Django tool that estimates the employer's cost of a two-year assignment from Zurich to London.

## Run locally

Use Python 3.12. Run these commands from the repository root in PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open [the estimator](http://127.0.0.1:8000/), select **Load Pack Test Case**, then select **Calculate cost**. The two-year estimate is £556,517.92 under the assumptions listed below the result.

On macOS or Linux, use `python3.12` to create the environment and `.venv/bin/python` for the commands that follow.

## Run checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

To run the same style checks as CI, install `requirements-dev.txt`, then run `python -m ruff check .` and `python -m ruff format --check .` using the virtual environment's Python.
