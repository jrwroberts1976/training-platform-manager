from __future__ import annotations

from .config import Course, Settings


def generate_stats(courses: list[Course], settings: Settings) -> None:
    rows = []
    total_modules = 0
    total_lessons = 0

    for course in courses:
        if not course.enabled:
            continue

        course_root = settings.courses_root / course.slug
        modules_root = course_root / "modules"

        module_count = 0
        lesson_count = 0

        if modules_root.exists():
            modules = [p for p in modules_root.iterdir() if p.is_dir()]
            module_count = len(modules)
            lesson_count = sum(
                1
                for module in modules
                for lesson in module.glob("*.md")
                if lesson.name != "README.md"
            )

        total_modules += module_count
        total_lessons += lesson_count
        rows.append(
            f"| {course.title} | {module_count} | {lesson_count} |"
        )

    lines = [
        "# Training Course Statistics",
        "",
        "| Course | Modules | Lessons |",
        "|---|---:|---:|",
        *rows,
        f"| **Total** | **{total_modules}** | **{total_lessons}** |",
        "",
        "This page is generated automatically by the training platform manager.",
        "",
    ]

    settings.stats_file.parent.mkdir(parents=True, exist_ok=True)
    settings.stats_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {settings.stats_file}")
