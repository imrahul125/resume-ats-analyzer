"""FastAPI application entry point for ResumeLens."""

from fastapi import FastAPI

app = FastAPI(
    title="ResumeLens API",
    description="Job-specific resume analysis API.",
    version="0.1.0",
)


@app.get("/", tags=["status"])
def root() -> dict[str, str]:
    """Provide a small welcome response and point to the API docs."""
    return {
        "name": "ResumeLens API",
        "message": "The backend is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["status"])
def health() -> dict[str, str]:
    """Report that the API process is responding."""
    return {"status": "ok"}
