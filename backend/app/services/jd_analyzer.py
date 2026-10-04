"""Deterministic extraction and normalization of common job skills."""

from __future__ import annotations

import re
from dataclasses import dataclass


# Keep this list deliberately small and explicit. New aliases should be added
# only when they are unambiguous enough to avoid inventing skill matches.
SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "Java": ("java",),
    "JavaScript": ("javascript", "ecmascript", "js"),
    "TypeScript": ("typescript",),
    "React": ("react", "react.js", "reactjs"),
    "React Native": ("react native", "react-native"),
    "Node.js": ("node.js", "nodejs", "node"),
    "Express.js": ("express.js", "expressjs", "express"),
    "FastAPI": ("fastapi", "fast api"),
    "Django": ("django",),
    "Flask": ("flask",),
    "Spring Boot": ("spring boot",),
    "C++": ("c++",),
    "C#": ("c#", "c sharp"),
    "SQL": ("sql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "MongoDB": ("mongodb", "mongo db"),
    "Redis": ("redis",),
    "REST API": ("rest api", "restful api", "rest apis", "restful apis"),
    "GraphQL": ("graphql",),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure", "microsoft azure"),
    "Google Cloud": ("google cloud", "gcp"),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Git": ("git",),
    "Linux": ("linux",),
    "CI/CD": ("ci/cd", "continuous integration", "continuous delivery"),
    "Machine Learning": ("machine learning", "ml"),
    "Natural Language Processing": ("natural language processing", "nlp"),
    "HTML": ("html",),
    "CSS": ("css",),
    "Pytest": ("pytest",),
}

_PREFERRED_CUE = re.compile(
    r"\b(preferred|nice to have|bonus|optional|not required|a plus|desirable|desired)\b", re.I
)
_REQUIRED_CUE = re.compile(
    r"\b(required|must have|must be|minimum qualifications|basic qualifications|requirements|we require)\b",
    re.I,
)
_PREFERRED_HEADING = re.compile(r"^\s*(preferred qualifications|preferred|nice to have|bonus|desired)\s*: ?$", re.I)
_REQUIRED_HEADING = re.compile(r"^\s*(requirements|minimum qualifications|basic qualifications|must have|required qualifications)\s*: ?$", re.I)


@dataclass(frozen=True)
class SkillRequirement:
    name: str
    requirement: str


def normalize_skill(name: str) -> str | None:
    """Map a known spelling or alias to its canonical skill name."""
    candidate = name.strip().lower()
    for canonical, aliases in SKILL_ALIASES.items():
        if candidate == canonical.lower() or candidate in aliases:
            return canonical
    return None


def _contains_alias(text: str, canonical: str) -> bool:
    aliases = sorted(SKILL_ALIASES[canonical], key=len, reverse=True)
    for alias in aliases:
        pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
        match = re.search(pattern, text, flags=re.I)
        if not match:
            continue
        # Do not count a short skill separately when it is only part of a more
        # specific skill phrase, such as React inside React Native.
        for other_name, other_aliases in SKILL_ALIASES.items():
            if other_name == canonical:
                continue
            for other_alias in other_aliases:
                if len(other_alias) <= len(alias):
                    continue
                other_pattern = rf"(?<![a-z0-9]){re.escape(other_alias)}(?![a-z0-9])"
                if any(
                    other_match.start() <= match.start() and other_match.end() >= match.end()
                    for other_match in re.finditer(other_pattern, text, flags=re.I)
                ):
                    return False
        return True
    return False


def extract_job_requirements(text: str) -> list[SkillRequirement]:
    """Find known skills and classify explicit required/preferred context.

    When a job description does not label a skill's importance, it is marked
    preferred. This conservative default avoids claiming the employer requires
    a skill when the text does not say so.
    """
    found: dict[str, str] = {}
    current_section = "preferred"
    source_lines = text.splitlines() or [text]
    lines = [
        sentence.strip(" \t-•▪")
        for source_line in source_lines
        for sentence in re.split(r"(?<=[.!?;])\s+|[•▪]", source_line)
        if sentence.strip(" \t-•▪")
    ]
    for line in lines:
        if _PREFERRED_HEADING.match(line):
            current_section = "preferred"
            continue
        if _REQUIRED_HEADING.match(line):
            current_section = "required"
            continue

        if _PREFERRED_CUE.search(line):
            importance = "preferred"
        elif _REQUIRED_CUE.search(line):
            importance = "required"
        else:
            importance = current_section

        for canonical in SKILL_ALIASES:
            if _contains_alias(line, canonical):
                # Required evidence takes precedence if the skill is repeated.
                if found.get(canonical) != "required":
                    found[canonical] = importance

    return [SkillRequirement(name, found[name]) for name in SKILL_ALIASES if name in found]


def classify_skill_in_resume(text: str, canonical: str) -> str:
    """Return matched, partial, or missing using exact aliases and word evidence."""
    if _contains_alias(text, canonical):
        return "matched"

    # Multi-word requirements can have partial evidence (for example, "React"
    # when the job asks specifically for "React Native"). Single words stay
    # missing unless a known alias is present.
    words = [word.lower() for word in re.findall(r"[a-zA-Z]{3,}", canonical)]
    if len(words) > 1 and any(re.search(rf"\b{re.escape(word)}\b", text, re.I) for word in words):
        return "partial"
    return "missing"
