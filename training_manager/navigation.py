from __future__ import annotations

from .config import Course, Settings
from .utils import markdown_title, numeric_key


def yaml_quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def course_navigation(course: Course, settings: Settings) -> list[str]:
    course_root = settings.courses_root / course.slug
    modules_root = course_root / "modules"

    if not course_root.exists():
        raise FileNotFoundError(f"Course is missing: {course_root}")

    lines = [
        f"      - {yaml_quote(course.title)}:",
        f"          - Course Overview: courses/{course.slug}/README.md",
    ]

    if not modules_root.exists():
        return lines

    modules = sorted(
        (path for path in modules_root.iterdir() if path.is_dir()),
        key=numeric_key,
    )

    for module in modules:
        readme = module / "README.md"
        module_title = markdown_title(readme)

        lines.append(f"          - {yaml_quote(module_title)}:")

        if readme.exists():
            lines.append(
                f"              - Overview: "
                f"courses/{course.slug}/modules/{module.name}/README.md"
            )

        lessons = sorted(
            (
                path
                for path in module.glob("*.md")
                if path.name != "README.md"
            ),
            key=numeric_key,
        )

        for lesson in lessons:
            lesson_title = markdown_title(lesson)
            lines.append(
                f"              - {yaml_quote(lesson_title)}: "
                f"courses/{course.slug}/modules/{module.name}/{lesson.name}"
            )

    return lines


def update_mkdocs(courses: list[Course], settings: Settings) -> None:
    content = settings.mkdocs_file.read_text(encoding="utf-8")

    if settings.start_marker not in content or settings.end_marker not in content:
        raise RuntimeError(
            "Automated course markers are missing from the central mkdocs.yml"
        )

    before, remainder = content.split(settings.start_marker, 1)
    _, after = remainder.split(settings.end_marker, 1)

    generated = [settings.start_marker]

    for course in courses:
        if course.enabled:
            generated.extend(course_navigation(course, settings))

    generated.append(settings.end_marker)

    settings.mkdocs_file.write_text(
        before + "\n".join(generated) + after,
        encoding="utf-8",
    )

    print(f"Updated {settings.mkdocs_file}")
