# API Guide

The backend is a FastAPI REST API. In local development, its base URL is
`http://127.0.0.1:8000`; interactive OpenAPI documentation is at `/docs`.

## Current endpoints

| Method | Path | Purpose | Success response |
| --- | --- | --- | --- |
| `GET` | `/` | Welcome message and documentation link. | JSON with API name, status message, and docs path. |
| `GET` | `/health` | Check that the API process is responding. | `{"status":"ok"}` |
| `GET` | `/health/database` | Run a read-only `SELECT 1` through SQLAlchemy. | `{"status":"ok"}` |
| `POST` | `/api/v1/analyze` | Parse and compare a PDF/DOCX resume with a job description. | Score factors, skill statuses, and recommendations. |

The database health endpoint returns HTTP 503 with a generic message when the
database is not configured or cannot be reached. It does not return credentials,
SQL, or a stack trace.

## CORS and frontend connection

The React app uses `VITE_API_BASE_URL` through the shared client in
`frontend/src/services/api.ts`. Vite reads the repository-root `.env` but only
exposes variables prefixed with `VITE_` to browser code. Database credentials,
AI keys, and signing secrets are not exposed.

FastAPI reads comma-separated allowed browser origins from `CORS_ORIGINS`. The
local defaults are `http://localhost:5173` and `http://127.0.0.1:5173`. Set the
production value to the exact Vercel site origin; avoid wildcard origins.

## Request flow

The landing page's service badge calls `GET /health/database` when it loads and
every 30 seconds.

## Resume analysis

`POST /api/v1/analyze` accepts `multipart/form-data` with:

- `resume_file`: PDF or DOCX, limited by `UPLOAD_MAX_MB` (10 MB by default).
- `job_description`: pasted job description, required (up to 50,000 characters).
- `job_title` and `company`: optional strings.

The route validates the extension, declared media type when supplied, and the
PDF signature or DOCX package contents. Resume text is extracted in memory and
is not saved. The job description and derived analysis records are stored in
PostgreSQL. The response includes a weighted Job Match Score, factor scores,
skill classifications, and recommendations.

Expected client errors include 413 for an oversized file, 415 for an unsupported
or malformed file, and 422 when the resume contains too little extractable text
or the job description is blank. A database write failure returns 503 without
exposing connection details.
