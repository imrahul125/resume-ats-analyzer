"""ORM models; import mapped classes here so Alembic can discover them."""

from app.models.analysis import Analysis
from app.models.analysis_metric import AnalysisMetric
from app.models.base import Base
from app.models.job_description import JobDescription
from app.models.recommendation import Recommendation
from app.models.resume import Resume
from app.models.tailored_resume import TailoredResume
from app.models.user import User

__all__ = [
    "Analysis",
    "AnalysisMetric",
    "Base",
    "JobDescription",
    "Recommendation",
    "Resume",
    "TailoredResume",
    "User",
]
