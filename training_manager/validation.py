from __future__ import annotations

import re
from pathlib import Path

from .config import Course, Settings


def validate_course(course: Course, settings: Settings) -> list[str]:
    errors: list[str] = []
    course_root = settings.courses_root / course.slug

    if not course_root.exists():
        return [f"{course.title}: course directory is missing"]

    if not (course_root / "README.md").exists():
        errors.append(f"{course.title}: README.md is missing")

    modules_root = course_root / "modules"
    if not modules_root.exists():
        errors.append(f"{course.title}: modules directory is missing")
        return errors

    seen_numbers: dict[str, Path] = {}

    for module in sorted(path for path in modules_root.iterdir() if path.is_dir()):
        if not (module / "README.md").exists():
            errors.append(f"{course.title}: {module.name}/README.md is missing")

        for lesson in module.glob("*.md"):
            if lesson.name == "README.md":
                continue

            match = re.match(r"^(\d+)-", lesson.name)
            if not match:
                errors.append(
                    f"{course.title}: lesson has no numeric prefix: {lesson}"
                )
                continue

            number = match.group(1)
            if number in seen_numbers:
                errors.append(
                    f"{course.title}: duplicate lesson number {number}: "
                    f"{seen_numbers[number]} and {lesson}"
                )
            else:
                seen_numbers[number] = lesson

    return errors


def validate_all(courses: list[Course], settings: Settings) -> None:
    errors: list[str] = []

    for course in courses:
        if course.enabled:
            errors.extend(validate_course(course, settings))

    if errors:
        print("\nValidation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Validation completed successfully")
