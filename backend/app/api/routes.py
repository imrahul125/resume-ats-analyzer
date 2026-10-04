"""Versioned application API routes."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from io import BytesIO
from pathlib import PurePath
from zipfile import BadZipFile, ZipFile

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models import Analysis, AnalysisMetric, JobDescription, Recommendation, Resume
from app.schemas.analysis import AnalysisResult
from app.services.resume_parser import parse_resume
from app.services.scoring import analyze_text

router = APIRouter(prefix="/api/v1", tags=["analysis"])
_PDF_MIME = "application/pdf"
_DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
_GENERIC_MIME = "application/octet-stream"
_MAX_JOB_DESCRIPTION_CHARS = 50_000
_MIN_RESUME_TEXT_CHARS = 40


def _validate_upload(filename: str, content_type: str | None, content: bytes) -> str:
    """Check extension, declared MIME type, and file signature/content."""
    suffix = PurePath(filename).suffix.lower()
    expected = {".pdf": _PDF_MIME, ".docx": _DOCX_MIME}.get(suffix)
    if expected is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Upload a PDF or DOCX resume.",
        )
    if content_type and content_type not in {expected, _GENERIC_MIME}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The file's declared type does not match its extension.",
        )
    if suffix == ".pdf" and not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="This file does not contain a valid PDF signature.",
        )
    if suffix == ".docx":
        try:
            with ZipFile(BytesIO(content)) as archive:
                entries = archive.infolist()
                names = {entry.filename for entry in entries}
            if "[Content_Types].xml" not in names or "word/document.xml" not in names:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail="This file is not a valid DOCX document.",
                )
            expanded_size = sum(entry.file_size for entry in entries)
            if expanded_size > 50 * 1024 * 1024 or any(
                entry.file_size > 1_000_000 and entry.file_size > max(1, entry.compress_size) * 200
                for entry in entries
            ):
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="This DOCX expands to an unsafe size. Re-save it in Word and upload it again.",
                )
        except BadZipFile:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="This file is not a valid DOCX document.",
            ) from None
    return expected


@router.post("/analyze", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED)
def analyze_resume(
    resume_file: UploadFile = File(..., description="A PDF or DOCX resume, up to the configured size limit."),
    job_description: str = Form(..., min_length=1, max_length=_MAX_JOB_DESCRIPTION_CHARS),
    job_title: str | None = Form(default=None, max_length=255),
    company: str | None = Form(default=None, max_length=255),
    db: Session = Depends(get_db),
) -> AnalysisResult:
    """Extract and compare a resume to a job description, then store only metadata/results."""
    clean_job_description = job_description.strip()
    if not clean_job_description:
        raise HTTPException(status_code=422, detail="Paste a job description before analyzing.")

    max_bytes = max(1, get_settings().upload_max_mb) * 1024 * 1024
    filename = resume_file.filename or ""
    content = resume_file.file.read(max_bytes + 1)
    if not content:
        raise HTTPException(status_code=422, detail="The uploaded file is empty.")
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"The resume is larger than the {max_bytes // (1024 * 1024)} MB upload limit.",
        )

    media_type = _validate_upload(filename, resume_file.content_type, content)
    upload_digest = hashlib.sha256(content).hexdigest()
    try:
        resume_text = parse_resume(filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    finally:
        # Do not retain the request's spooled upload after processing.
        content = b""
        resume_file.file.close()

    if len(resume_text) < _MIN_RESUME_TEXT_CHARS:
        raise HTTPException(
            status_code=422,
            detail="We couldn't extract enough selectable text. This may be an image-only PDF; export a text-based PDF or upload a DOCX.",
        )

    resume_text_length = len(resume_text)
    result = analyze_text(resume_text, clean_job_description)
    resume_record = Resume(
        media_type=media_type,
        content_sha256=upload_digest,
    )
    job_record = JobDescription(
        title=job_title.strip() if job_title and job_title.strip() else None,
        company=company.strip() if company and company.strip() else None,
        description_text=clean_job_description,
    )
    # Release the extracted private text as soon as deterministic analysis ends.
    resume_text = ""

    try:
        db.add_all([resume_record, job_record])
        db.flush()
        analysis_record = Analysis(
            resume_id=resume_record.id,
            job_description_id=job_record.id,
            status="completed",
            overall_score=result["overall_score"],
            completed_at=datetime.now(timezone.utc),
        )
        db.add(analysis_record)
        db.flush()

        for metric in result["metrics"]:
            db.add(
                AnalysisMetric(
                    analysis_id=analysis_record.id,
                    key=metric["key"],
                    score=metric["score"],
                    weight=metric["weight"],
                    details={"label": metric["label"], "explanation": metric["explanation"]},
                )
            )
        for order, recommendation in enumerate(result["recommendations"]):
            db.add(
                Recommendation(
                    analysis_id=analysis_record.id,
                    priority=recommendation["priority"],
                    category=recommendation["category"],
                    message=recommendation["message"],
                    sort_order=order,
                )
            )
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="The analysis could not be saved because the database is temporarily unavailable. Please try again.",
        ) from None

    return AnalysisResult(
        id=analysis_record.id,
        overall_score=result["overall_score"],
        resume_text_length=resume_text_length,
        metrics=result["metrics"],
        skills=result["skills"],
        recommendations=result["recommendations"],
    )
