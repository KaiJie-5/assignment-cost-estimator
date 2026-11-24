# Assignment cost estimator

A Django tool that estimates the employer's cost of a two-year assignment from Zurich to London.

## Loom video

[Watch the Loom walkthrough](https://www.loom.com/share/99aec92280c444b5b9b2ad606b4603f9)

## Get the code

```sh
git clone https://github.com/KaiJie-5/assignment-cost-estimator.git
cd assignment-cost-estimator
```

## Start the app

Run the commands for your system from the `assignment-cost-estimator` folder. The version command should show Python 3.12.

### Windows PowerShell

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

## Run the tests

In the same folder, run the commands for your system.

### Windows PowerShell

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

## AI tools used

ChatGPT (Codex) helped find official tax and immigration sources.
