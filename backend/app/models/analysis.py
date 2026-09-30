"""A score and status for comparing a resume with a job description."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, SmallInteger, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Analysis(TimestampMixin, Base):
    __tablename__ = "analyses"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed', 'failed')", name="status_values"
        ),
        CheckConstraint(
            "overall_score IS NULL OR (overall_score >= 0 AND overall_score <= 100)",
            name="score_range",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    resume_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    job_description_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", server_default="pending", nullable=False
    )
    overall_score: Mapped[int | None] = mapped_column(SmallInteger)
    scoring_version: Mapped[str] = mapped_column(
        String(50), default="v1", server_default="v1", nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    resume: Mapped["Resume"] = relationship(back_populates="analyses")
    job_description: Mapped["JobDescription"] = relationship(back_populates="analyses")
    metrics: Mapped[list["AnalysisMetric"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan"
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan"
    )
    tailored_resume: Mapped["TailoredResume | None"] = relationship(
        back_populates="analysis", cascade="all, delete-orphan", uselist=False
    )

