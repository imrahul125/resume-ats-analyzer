"""Public response models for a resume-to-job analysis."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class MetricResult(BaseModel):
    key: str
    label: str
    score: int = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    explanation: str


class SkillResult(BaseModel):
    name: str
    status: Literal["matched", "partial", "missing"]
    requirement: Literal["required", "preferred"]


class RecommendationResult(BaseModel):
    priority: Literal["high", "medium", "low"]
    category: str
    message: str


class AnalysisResult(BaseModel):
    id: UUID
    overall_score: int = Field(ge=0, le=100)
    resume_text_length: int = Field(ge=0)
    metrics: list[MetricResult]
    skills: list[SkillResult]
    recommendations: list[RecommendationResult]
