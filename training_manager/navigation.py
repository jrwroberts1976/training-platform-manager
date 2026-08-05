from __future__ import annotations

from .config import Course, Settings
from .utils import markdown_title, numeric_key


def yaml_quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def course_navigation(course: Course, settings: Settings) -> list[str]:
    root = settings.courses_root / course.slug
    modules_root = root / "modules"

    lines = [
        f"      - {yaml_quote(course.title)}:",
        f"          - Course Overview: courses/{course.slug}/README.md",
    ]

    if not modules_root.exists():
        return lines

    for module in sorted((p for p in modules_root.iterdir() if p.is_dir()), key=numeric_key):
        readme = module / "README.md"
        lines.append(f"          - {yaml_quote(markdown_title(readme))}:")
        if readme.exists():
            lines.append(
                f"              - Overview: "
                f"courses/{course.slug}/modules/{module.name}/README.md"
            )

        for lesson in sorted(
            (p for p in module.glob("*.md") if p.name != "README.md"),
            key=numeric_key,
        ):
            lines.append(
                f"              - {yaml_quote(markdown_title(lesson))}: "
                f"courses/{course.slug}/modules/{module.name}/{lesson.name}"
            )

    return lines


def update_mkdocs(courses: list[Course], settings: Settings) -> None:
    content = settings.mkdocs_file.read_text(encoding="utf-8")

    if settings.start_marker not in content or settings.end_marker not in content:
        raise RuntimeError("Automated course markers are missing from mkdocs.yml")

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
