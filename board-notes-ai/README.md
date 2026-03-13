# Board Notes AI

## Run locally

Start from the project directory, not the workspace root:

```bash
cd board-notes-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.server:app --host 0.0.0.0 --port 8000
```

Using `python -m uvicorn` avoids PATH issues when the `uvicorn` executable is not available globally.