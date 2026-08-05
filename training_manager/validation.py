from __future__ import annotations
import re
from .config import Course, Settings

def validate_all(courses: list[Course], settings: Settings) -> None:
    errors = []
    for course in courses:
        if not course.enabled:
            continue
        root = settings.courses_root / course.slug
        if not root.exists():
            errors.append(f"{course.title}: course directory is missing")
            continue
        if not (root / "README.md").exists():
            errors.append(f"{course.title}: README.md is missing")
        modules = root / "modules"
        if not modules.exists():
            errors.append(f"{course.title}: modules directory is missing")
            continue
        seen = {}
        for module in sorted(p for p in modules.iterdir() if p.is_dir()):
            if not (module / "README.md").exists():
                errors.append(f"{course.title}: {module.name}/README.md is missing")
            for lesson in module.glob("*.md"):
                if lesson.name == "README.md":
                    continue
                match = re.match(r"^(\d+)-", lesson.name)
                if not match:
                    errors.append(f"{course.title}: no lesson number: {lesson}")
                    continue
                number = match.group(1)
                if number in seen:
                    errors.append(f"{course.title}: duplicate lesson {number}")
                seen[number] = lesson
    if errors:
        print("\nValidation failed:")
        for error in errors:
            print("-", error)
        raise SystemExit(1)
    print("Validation completed successfully")
