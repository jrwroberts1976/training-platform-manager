from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .config import Course, Settings, load_courses, save_courses
from .utils import command_exists, run, slugify


DEFAULT_DOCKER_MODULES = [
    "Introduction",
    "Images",
    "Containers",
    "Volumes",
    "Networks",
    "Docker Compose",
    "Building Images",
    "Security",
    "Troubleshooting",
    "Final Project",
]


@dataclass
class CreateCourseOptions:
    slug: str
    title: str
    level: str
    estimated_hours: int
    modules: list[str]
    description: str
    public: bool
    create_github: bool
    register: bool
    run_build: bool


def render_module_readme(number: int, name: str) -> str:
    return f"""# Module {number:02d} - {name}

## Overview

This module introduces **{name}**.

## Learning Objectives

- Understand the core concepts
- Complete practical exercises
- Validate the implementation
- Document the results

## Lessons

Lessons will be added as the course develops.
"""


def render_course_readme(options: CreateCourseOptions) -> str:
    lines = [
        f"# {options.title}",
        "",
        "## Overview",
        "",
        options.description,
        "",
        "## Course Details",
        "",
        f"- **Level:** {options.level}",
        f"- **Estimated duration:** {options.estimated_hours} hours",
        f"- **Modules:** {len(options.modules)}",
        "",
        "## Modules",
        "",
    ]

    for index, name in enumerate(options.modules, start=1):
        module_slug = slugify(name)
        lines.append(
            f"- [Module {index:02d} - {name}]"
            f"(modules/{index:02d}-{module_slug}/README.md)"
        )

    return "\n".join(lines) + "\n"


def render_mkdocs(options: CreateCourseOptions) -> str:
    lines = [
        f"site_name: {options.title}",
        "theme:",
        "  name: material",
        "",
        "nav:",
        "  - Home: README.md",
    ]

    for index, name in enumerate(options.modules, start=1):
        module_slug = slugify(name)
        lines.extend([
            f"  - Module {index:02d} - {name}:",
            f"      - Overview: modules/{index:02d}-{module_slug}/README.md",
        ])

    return "\n".join(lines) + "\n"


def create_course(
    options: CreateCourseOptions,
    settings: Settings,
    courses_path: Path,
) -> Path:
    repo_name = f"{options.slug}-training"
    destination = settings.project_root / repo_name

    if destination.exists():
        raise RuntimeError(f"Destination already exists: {destination}")

    destination.mkdir(parents=True)
    for directory in [
        "modules",
        "labs",
        "projects",
        "resources",
        "diagrams",
        "scripts",
        ".github/workflows",
    ]:
        (destination / directory).mkdir(parents=True, exist_ok=True)

    (destination / "README.md").write_text(
        render_course_readme(options),
        encoding="utf-8",
    )
    (destination / "mkdocs.yml").write_text(
        render_mkdocs(options),
        encoding="utf-8",
    )
    (destination / ".gitignore").write_text(
        ".venv/\n__pycache__/\nsite/\n.env\n",
        encoding="utf-8",
    )
    (destination / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0\n\n- Initial course structure\n",
        encoding="utf-8",
    )
    (destination / "ROADMAP.md").write_text(
        f"# {options.title} Roadmap\n\n- Complete module content\n- Add labs\n- Add projects\n",
        encoding="utf-8",
    )
    (destination / "LICENSE").write_text(
        "Choose an open-source licence before publishing.\n",
        encoding="utf-8",
    )

    manifest = {
        "slug": options.slug,
        "title": options.title,
        "description": options.description,
        "level": options.level,
        "estimated_hours": options.estimated_hours,
        "tags": [],
        "requires": [],
        "icon": "school",
        "featured": False,
    }
    (destination / "course-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    for index, name in enumerate(options.modules, start=1):
        module_dir = destination / "modules" / f"{index:02d}-{slugify(name)}"
        module_dir.mkdir()
        (module_dir / "README.md").write_text(
            render_module_readme(index, name),
            encoding="utf-8",
        )

    for folder in ["labs", "projects", "resources", "diagrams", "scripts"]:
        (destination / folder / "README.md").write_text(
            f"# {folder.title()}\n\nAdd {folder} here.\n",
            encoding="utf-8",
        )

    workflow = """name: Validate Course

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Check Markdown
        run: find . -name "*.md" -type f -print
"""
    (destination / ".github/workflows/validate.yml").write_text(
        workflow,
        encoding="utf-8",
    )

    run(["git", "init"], cwd=destination)
    run(["git", "branch", "-M", "main"], cwd=destination)
    run(["git", "add", "."], cwd=destination)
    run(["git", "commit", "-m", f"Create {options.title} course"], cwd=destination)

    repository = (
        f"git@github.com:{settings.github_owner}/{repo_name}.git"
        if settings.github_owner
        else ""
    )

    if options.create_github:
        if not command_exists("gh"):
            raise RuntimeError("GitHub CLI 'gh' is not installed")

        visibility = "--public" if options.public else "--private"
        run(
            [
                "gh",
                "repo",
                "create",
                f"{settings.github_owner}/{repo_name}",
                visibility,
                "--source",
                str(destination),
                "--remote",
                "origin",
                "--push",
                "--description",
                options.description,
            ],
            cwd=destination,
        )

    if options.register:
        if not repository:
            raise RuntimeError("github_owner is missing from settings.json")

        courses = load_courses(courses_path)
        if any(c.slug == options.slug for c in courses):
            raise RuntimeError(f"Course is already registered: {options.slug}")

        courses.append(
            Course(
                slug=options.slug,
                title=options.title,
                repository=repository,
                branch="main",
                enabled=True,
            )
        )
        save_courses(courses_path, courses)
        print(f"Registered {options.title} in {courses_path}")

    if options.run_build:
        print("Course created. Run the manager build after pushing the repository.")

    print(f"Created course at {destination}")
    return destination


def docker_options() -> CreateCourseOptions:
    return CreateCourseOptions(
        slug="docker",
        title="Docker Engineering",
        level="Beginner to Intermediate",
        estimated_hours=40,
        modules=DEFAULT_DOCKER_MODULES,
        description=(
            "Professional engineering training covering Docker fundamentals, "
            "images, containers, networking, storage, Compose, security and operations."
        ),
        public=True,
        create_github=False,
        register=False,
        run_build=False,
    )
