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
    homepage_file: Path
    stats_file: Path
    skills_file: Path
    learning_paths_file: Path
    recent_updates_file: Path
    start_marker: str
    end_marker: str


def load_courses(path: Path) -> list[Course]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Course(**item) for item in data.get("courses", [])]


def load_settings(path: Path) -> Settings:
    data = json.loads(path.read_text(encoding="utf-8"))
    platform_root = Path(data["platform_root"]).expanduser().resolve()

    def resolve(relative: str) -> Path:
        return platform_root / relative

    return Settings(
        platform_root=platform_root,
        courses_root=resolve(data["courses_root"]),
        mkdocs_file=resolve(data["mkdocs_file"]),
        homepage_file=resolve(data.get("homepage_file", "docs/training/index.md")),
        stats_file=resolve(data.get("stats_file", "docs/training/course-statistics.md")),
        skills_file=resolve(data.get("skills_file", "docs/training/skill-matrix.md")),
        learning_paths_file=resolve(data.get("learning_paths_file", "docs/training/learning-paths.md")),
        recent_updates_file=resolve(data.get("recent_updates_file", "docs/training/recent-updates.md")),
        start_marker=data.get("start_marker", "      # BEGIN AUTOMATED COURSES"),
        end_marker=data.get("end_marker", "      # END AUTOMATED COURSES"),
    )
