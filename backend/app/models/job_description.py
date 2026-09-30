"""Job descriptions supplied for a specific resume analysis."""

from uuid import UUID, uuid4

from sqlalchemy import String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class JobDescription(TimestampMixin, Base):
    __tablename__ = "job_descriptions"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str | None] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255))
    description_text: Mapped[str] = mapped_column(Text, nullable=False)

    analyses: Mapped[list["Analysis"]] = relationship(back_populates="job_description")

