# InsightAI Backend

This is the Python + FastAPI backend for the **InsightAI** Content Intelligence Platform.

## Features Included
- **Asynchronous endpoints** for analysis modules.
- **Structured Pydantic validation** schemas.
- **CORS enabled** for frontend connection.
- **Health check endpoint** (`/health`).
- **Tests** setup via `pytest`.

## Directory Structure
- `app/api/`: Placeholder endpoints for spam, poem, and movie analytics.
- `app/core/`: Application settings and global configurations.
- `app/models/`: Future database schema models.
- `app/schemas/`: Pydantic models for request validation and response serialisation.
- `app/services/`: NLP and machine learning computational modules.
- `app/utils/`: Generic utility helper routines.
- `tests/`: Module unit tests.

## Running Locally

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Access the auto-generated API interactive docs at `http://localhost:8000/docs`.
