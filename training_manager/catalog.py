from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from .config import Course, Settings
from .manifests import load_manifest
from .utils import run


def counts(course: Course, settings: Settings) -> tuple[int, int, int, int]:
    root = settings.courses_root / course.slug
    modules_root = root / "modules"
    modules = [p for p in modules_root.iterdir() if p.is_dir()] if modules_root.exists() else []
    lessons = sum(
        1 for module in modules for p in module.glob("*.md") if p.name != "README.md"
    )
    labs = sum(1 for _ in (root / "labs").rglob("*.md")) if (root / "labs").exists() else 0
    projects = sum(1 for _ in (root / "projects").rglob("*.md")) if (root / "projects").exists() else 0
    return len(modules), lessons, labs, projects


def last_commit(course: Course, settings: Settings) -> tuple[str, str]:
    root = settings.courses_root / course.slug
    if not (root / ".git").exists():
        return "Unknown", "Unknown"

    date = run(["git", "log", "-1", "--format=%cs"], cwd=root, capture=True)
    commit = run(["git", "log", "-1", "--format=%h"], cwd=root, capture=True)
    return date or "Unknown", commit or "Unknown"


def generate_homepage(courses: list[Course], settings: Settings) -> None:
    enabled = [c for c in courses if c.enabled]
    totals = [counts(c, settings) for c in enabled]
    total_modules = sum(x[0] for x in totals)
    total_lessons = sum(x[1] for x in totals)
    total_labs = sum(x[2] for x in totals)
    total_projects = sum(x[3] for x in totals)

    lines = [
        "# Engineering Training Platform",
        "",
        "A self-maintaining engineering learning platform built with Git, Python, MkDocs, Docker and CI/CD.",
        "",
        "## Platform Summary",
        "",
        f"- **Courses:** {len(enabled)}",
        f"- **Modules:** {total_modules}",
        f"- **Lessons:** {total_lessons}",
        f"- **Labs:** {total_labs}",
        f"- **Projects:** {total_projects}",
        "",
        "## Courses",
        "",
    ]

    ordered = sorted(
        enabled,
        key=lambda c: (not load_manifest(c, settings).featured, c.title.lower()),
    )

    for course in ordered:
        manifest = load_manifest(course, settings)
        module_count, lesson_count, lab_count, project_count = counts(course, settings)
        lines.extend([
            f"### [{manifest.title}](../courses/{course.slug}/README.md)",
            "",
            manifest.description,
            "",
            f"**Level:** {manifest.level}  ",
            f"**Modules:** {module_count} · **Lessons:** {lesson_count} · "
            f"**Labs:** {lab_count} · **Projects:** {project_count}",
            "",
        ])

    settings.homepage_file.parent.mkdir(parents=True, exist_ok=True)
    settings.homepage_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.homepage_file}")


def generate_stats(courses: list[Course], settings: Settings) -> None:
    rows = []
    totals = [0, 0, 0, 0]

    for course in courses:
        if not course.enabled:
            continue
        values = counts(course, settings)
        totals = [a + b for a, b in zip(totals, values)]
        rows.append(
            f"| {course.title} | {values[0]} | {values[1]} | {values[2]} | {values[3]} |"
        )

    lines = [
        "# Training Course Statistics",
        "",
        "| Course | Modules | Lessons | Labs | Projects |",
        "|---|---:|---:|---:|---:|",
        *rows,
        f"| **Total** | **{totals[0]}** | **{totals[1]}** | **{totals[2]}** | **{totals[3]}** |",
        "",
        "Generated automatically by Training Platform Manager v0.4.",
        "",
    ]

    settings.stats_file.parent.mkdir(parents=True, exist_ok=True)
    settings.stats_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.stats_file}")


def generate_skills(courses: list[Course], settings: Settings) -> None:
    tag_courses: dict[str, list[str]] = defaultdict(list)

    for course in courses:
        if not course.enabled:
            continue
        manifest = load_manifest(course, settings)
        for tag in manifest.tags:
            tag_courses[tag].append(manifest.title)

    lines = [
        "# Skill Matrix",
        "",
        "| Skill | Evidence |",
        "|---|---|",
    ]

    for tag in sorted(tag_courses, key=str.lower):
        lines.append(f"| {tag} | {', '.join(sorted(tag_courses[tag]))} |")

    if not tag_courses:
        lines.append("| Course metadata | Add `tags` to each course manifest |")

    lines += ["", "Generated automatically from course manifests.", ""]

    settings.skills_file.parent.mkdir(parents=True, exist_ok=True)
    settings.skills_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.skills_file}")


def generate_learning_paths(courses: list[Course], settings: Settings) -> None:
    enabled = [c for c in courses if c.enabled]
    by_slug = {c.slug: c for c in enabled}
    manifests = {c.slug: load_manifest(c, settings) for c in enabled}

    lines = ["# Learning Paths", ""]

    for course in enabled:
        manifest = manifests[course.slug]
        if not manifest.requires:
            continue

        prerequisites = [
            f"[{manifests[slug].title}](../courses/{slug}/README.md)"
            for slug in manifest.requires
            if slug in by_slug
        ]

        if prerequisites:
            lines.extend([
                f"## {manifest.title}",
                "",
                "Recommended prerequisites:",
                "",
                *[f"- {item}" for item in prerequisites],
                "",
            ])

    if len(lines) == 2:
        lines.extend([
            "No prerequisite relationships have been defined yet.",
            "",
            "Add a `requires` list to each course manifest.",
            "",
        ])

    settings.learning_paths_file.parent.mkdir(parents=True, exist_ok=True)
    settings.learning_paths_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.learning_paths_file}")


def generate_recent_updates(courses: list[Course], settings: Settings) -> None:
    updates = []
    for course in courses:
        if not course.enabled:
            continue
        date, commit = last_commit(course, settings)
        updates.append((date, course.title, course.slug, commit))

    updates.sort(reverse=True)

    lines = [
        "# Recently Updated Courses",
        "",
        "| Date | Course | Commit |",
        "|---|---|---|",
    ]

    for date, title, slug, commit in updates:
        lines.append(
            f"| {date} | [{title}](../courses/{slug}/README.md) | `{commit}` |"
        )

    lines += ["", "Generated from the latest local Git commit for each course.", ""]

    settings.recent_updates_file.parent.mkdir(parents=True, exist_ok=True)
    settings.recent_updates_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.recent_updates_file}")


def generate_catalog(courses: list[Course], settings: Settings) -> None:
    generate_homepage(courses, settings)
    generate_stats(courses, settings)
    generate_skills(courses, settings)
    generate_learning_paths(courses, settings)
    generate_recent_updates(courses, settings)
