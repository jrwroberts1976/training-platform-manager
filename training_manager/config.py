from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Course:
    slug: str
    title: str
    repository: str
    branch: str = "main"
    enabled: bool = True


@dataclass(frozen=True)
class Settings:
    platform_root: Path
    courses_root: Path
    mkdocs_file: Path
    stats_file: Path
    start_marker: str
    end_marker: str


def load_courses(path: Path) -> list[Course]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Course(**item) for item in data.get("courses", [])]


def load_settings(path: Path) -> Settings:
    data = json.loads(path.read_text(encoding="utf-8"))
    platform_root = Path(data["platform_root"]).expanduser().resolve()

    return Settings(
        platform_root=platform_root,
        courses_root=platform_root / data["courses_root"],
        mkdocs_file=platform_root / data["mkdocs_file"],
        stats_file=platform_root / data.get(
            "stats_file",
            "docs/training/course-statistics.md",
        ),
        start_marker=data.get(
            "start_marker",
            "      # BEGIN AUTOMATED COURSES",
        ),
        end_marker=data.get(
            "end_marker",
            "      # END AUTOMATED COURSES",
        ),
    )
