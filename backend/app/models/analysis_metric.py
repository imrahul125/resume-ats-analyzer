"""One weighted factor in an explainable analysis score."""

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, JSON, Numeric, SmallInteger, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AnalysisMetric(Base):
    __tablename__ = "analysis_metrics"
    __table_args__ = (
        UniqueConstraint("analysis_id", "key", name="uq_analysis_metrics_analysis_key"),
        CheckConstraint("score >= 0 AND score <= 100", name="score_range"),
        CheckConstraint("weight >= 0 AND weight <= 1", name="weight_range"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    analysis_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(80), nullable=False)
    score: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    # Store compact structured match facts here, never the uploaded resume text.
    details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    analysis: Mapped["Analysis"] = relationship(back_populates="metrics")

