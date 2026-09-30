"""Resume metadata; uploaded files and extracted text are not stored here."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Resume(TimestampMixin, Base):
    __tablename__ = "resumes"
    __table_args__ = (Index("ix_resumes_user_id", "user_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    media_type: Mapped[str] = mapped_column(String(127), nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User | None"] = relationship(back_populates="resumes")
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="resume")

