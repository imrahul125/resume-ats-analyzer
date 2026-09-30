"""Metadata for a tailored export; the resume/PDF bytes remain temporary."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TailoredResume(TimestampMixin, Base):
    __tablename__ = "tailored_resumes"
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'generated', 'failed')", name="status_values"),
        CheckConstraint("output_format IN ('pdf')", name="format_values"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    analysis_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(12), default="pending", server_default="pending", nullable=False
    )
    output_format: Mapped[str] = mapped_column(
        String(10), default="pdf", server_default="pdf", nullable=False
    )
    content_sha256: Mapped[str | None] = mapped_column(String(64))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    analysis: Mapped["Analysis"] = relationship(back_populates="tailored_resume")

