"""Explainable, deterministic job-to-resume scoring; no LLM-generated score."""

from __future__ import annotations

import re

from app.services.jd_analyzer import SkillRequirement, classify_skill_in_resume, extract_job_requirements
from app.services.resume_parser import extract_sections


WEIGHTS: dict[str, tuple[str, float]] = {
    "skill_match": ("Keyword and skill match", 0.25),
    "required_match": ("Required requirements", 0.20),
    "experience_evidence": ("Experience evidence", 0.15),
    "structure": ("Resume structure", 0.10),
    "education": ("Education match", 0.10),
    "job_language": ("Job-language overlap", 0.10),
    "formatting": ("ATS-style readability", 0.10),
}

_STOP_WORDS = set(
    "a an and are as at be by for from has have in into is it its of on or our that the their this to we with will you your"
    " ability responsibilities experience role team work working including across using strong excellent proven skills"
    .split()
)


def _ratio(points: float, total: int, neutral: int = 50) -> int:
    if total == 0:
        return neutral
    return round(max(0.0, min(1.0, points / total)) * 100)


def _skill_score(requirements: list[SkillRequirement], resume_text: str) -> tuple[int, list[dict[str, str]]]:
    results: list[dict[str, str]] = []
    points = 0.0
    required_points = 0.0
    required_total = 0
    for item in requirements:
        status = classify_skill_in_resume(resume_text, item.name)
        points += {"matched": 1.0, "partial": 0.5, "missing": 0.0}[status]
        if item.requirement == "required":
            required_total += 1
            required_points += {"matched": 1.0, "partial": 0.5, "missing": 0.0}[status]
        results.append({"name": item.name, "status": status, "requirement": item.requirement})
    return _ratio(points, len(requirements), neutral=0), results


def _education_score(job_text: str, resume_text: str, sections: dict[str, str]) -> tuple[int, str]:
    levels = [
        (4, re.compile(r"\b(ph\.?d\.?|doctorate|doctoral)\b", re.I)),
        (3, re.compile(r"\b(master'?s|master of|mba|m\.s\.?|m\.a\.?)\b", re.I)),
        (2, re.compile(r"\b(bachelor'?s|bachelor of|b\.s\.?|b\.a\.?|undergraduate degree)\b", re.I)),
        (1, re.compile(r"\b(associate'?s degree|diploma)\b", re.I)),
    ]
    job_levels = [level for level, pattern in levels if pattern.search(job_text)]
    if not job_levels and not re.search(r"\b(degree|education|academic qualification)\b", job_text, re.I):
        return 100, "No specific education requirement was detected in the job description."

    resume_levels = [level for level, pattern in levels if pattern.search(resume_text)]
    if job_levels and resume_levels:
        required_level = max(job_levels)
        if max(resume_levels) >= required_level:
            return 100, "The resume text includes an education level matching or exceeding the stated level."
        return 0, "No resume text was found for the stated education level."
    if sections.get("education"):
        return 50, "An education section is present, but the required level could not be verified from its text."
    return 0, "The job description mentions education, but no education section was detected in the resume."


def _job_language_score(job_text: str, resume_text: str) -> tuple[int, str]:
    job_terms = [
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{3,}", job_text)
        if token.lower() not in _STOP_WORDS
    ]
    if not job_terms:
        return 0, "No distinctive job-description terms were available for comparison."
    frequencies: dict[str, int] = {}
    for term in job_terms:
        frequencies[term] = frequencies.get(term, 0) + 1
    key_terms = sorted(frequencies, key=lambda term: (-frequencies[term], term))[:25]
    resume_terms = {word.lower() for word in re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{3,}", resume_text)}
    overlap = sum(term in resume_terms for term in key_terms)
    return round(overlap / len(key_terms) * 100), f"{overlap} of the {len(key_terms)} most repeated job-description terms also appear in the resume. This is word overlap, not embedding-based semantic matching."


def _formatting_score(text: str, sections: list[str]) -> tuple[int, str]:
    score = 45
    if len(text) >= 500:
        score += 25
    elif len(text) >= 250:
        score += 18
    elif len(text) >= 100:
        score += 10
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        score += 10
    if re.search(r"(?:\+?\d[\d ()-]{7,}\d)", text):
        score += 8
    if re.search(r"(?:^|\n)\s*(?:[-*•▪]|\d+[.)])\s+", text):
        score += 7
    if len(sections) >= 3:
        score += 5
    lines = [line for line in text.splitlines() if line]
    if lines and max(map(len, lines)) > 240:
        score -= 10
    odd_chars = sum(not char.isprintable() and char not in "\n\r\t" for char in text)
    if text and odd_chars / len(text) > 0.03:
        score -= 10
    return max(0, min(100, score)), "A basic text-extraction and readability heuristic; it cannot predict every ATS parser."


def _recommendations(
    skills: list[dict[str, str]], sections: list[str], requirements: list[SkillRequirement]
) -> list[dict[str, str]]:
    requirement_by_name = {item.name: item.requirement for item in requirements}
    output: list[dict[str, str]] = []
    for skill in skills:
        if skill["status"] == "missing":
            kind = requirement_by_name[skill["name"]]
            priority = "high" if kind == "required" else "medium"
            output.append(
                {
                    "priority": priority,
                    "category": "missing_requirement",
                    "message": (
                        f"The job description lists {skill['name']} as {kind}, but the resume text does not provide supporting evidence. "
                        "Only add it if it accurately reflects your experience."
                    ),
                }
            )
        elif skill["status"] == "partial":
            output.append(
                {
                    "priority": "medium",
                    "category": "partial_requirement",
                    "message": (
                        f"The resume contains partial wording related to {skill['name']}. If you have direct experience, describe the specific work clearly."
                    ),
                }
            )
    if "experience" not in sections:
        output.append(
            {
                "priority": "medium",
                "category": "resume_structure",
                "message": "A standard Experience section heading was not detected. Use a clear heading if your resume includes work history.",
            }
        )
    if not requirements:
        output.append(
            {
                "priority": "low",
                "category": "job_description",
                "message": "No skills from the analyzer's current skill list were detected. Review the job description and compare its requirements manually.",
            }
        )
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(output, key=lambda item: (order[item["priority"]], item["category"]))[:12]


def analyze_text(resume_text: str, job_text: str) -> dict:
    """Compute score factors and recommendations from extracted text only."""
    requirements = extract_job_requirements(job_text)
    skill_score, skills = _skill_score(requirements, resume_text)
    required = [item for item in requirements if item.requirement == "required"]
    required_points = sum(
        {"matched": 1.0, "partial": 0.5, "missing": 0.0}[item["status"]]
        for item in skills
        if item["requirement"] == "required"
    )
    required_score = _ratio(required_points, len(required), neutral=100)

    sections_by_name = extract_sections(resume_text)
    section_names = list(sections_by_name)
    structured_career_text = "\n".join(
        sections_by_name.get(name, "") for name in ("experience", "projects", "internships")
    )
    career_points = sum(
        {"matched": 1.0, "partial": 0.5, "missing": 0.0}[
            classify_skill_in_resume(structured_career_text, item["name"])
        ]
        for item in skills
    )
    experience_score = _ratio(career_points, len(skills), neutral=50)
    structure_score = min(100, round(len(section_names) / 4 * 100))
    education_score, education_explanation = _education_score(job_text, resume_text, sections_by_name)
    job_language_score, language_explanation = _job_language_score(job_text, resume_text)
    formatting_score, formatting_explanation = _formatting_score(resume_text, section_names)

    scores = {
        "skill_match": skill_score,
        "required_match": required_score,
        "experience_evidence": experience_score,
        "structure": structure_score,
        "education": education_score,
        "job_language": job_language_score,
        "formatting": formatting_score,
    }
    explanations = {
        "skill_match": "Matched skills count fully, partial matches count halfway, and missing skills count zero.",
        "required_match": "Only explicitly required skills are included; missing required skills lower this factor more directly.",
        "experience_evidence": "Checks recognized job skills inside Experience, Projects, and Internships sections.",
        "structure": f"Detected {len(section_names)} standard resume sections; four detected sections reach 100.",
        "education": education_explanation,
        "job_language": language_explanation,
        "formatting": formatting_explanation,
    }
    metrics = [
        {
            "key": key,
            "label": WEIGHTS[key][0],
            "score": scores[key],
            "weight": WEIGHTS[key][1],
            "explanation": explanations[key],
        }
        for key in WEIGHTS
    ]
    overall = round(sum(metric["score"] * metric["weight"] for metric in metrics))
    return {
        "overall_score": overall,
        "metrics": metrics,
        "skills": skills,
        "recommendations": _recommendations(skills, section_names, requirements),
        "sections": section_names,
    }
