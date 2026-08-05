from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .config import Course, Settings


@dataclass
class Manifest:
    slug: str
    title: str
    description: str
    level: str = "Mixed"
    estimated_hours: int = 0
    tags: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    icon: str = "school"
    featured: bool = False


def load_manifest(course: Course, settings: Settings) -> Manifest:
    course_root = settings.courses_root / course.slug
    path = course_root / "course-manifest.json"

    if not path.exists():
        return Manifest(
            slug=course.slug,
            title=course.title,
            description=f"Training course for {course.title}.",
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    # Existing generated manifests may be lesson lists. Fall back safely.
    if isinstance(data, list):
        return Manifest(
            slug=course.slug,
            title=course.title,
            description=f"Training course for {course.title}.",
        )

    return Manifest(
        slug=data.get("slug", course.slug),
        title=data.get("title", course.title),
        description=data.get("description", f"Training course for {course.title}."),
        level=data.get("level", "Mixed"),
        estimated_hours=int(data.get("estimated_hours", 0)),
        tags=list(data.get("tags", [])),
        requires=list(data.get("requires", [])),
        icon=data.get("icon", "school"),
        featured=bool(data.get("featured", False)),
    )
