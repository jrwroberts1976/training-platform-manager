from __future__ import annotations

from .config import Course, Settings
from .utils import run


def sync_course(course: Course, settings: Settings) -> None:
    destination = settings.courses_root / course.slug

    print(f"\nSynchronising {course.title}")

    if (destination / ".git").exists():
        run(["git", "fetch", "--prune", "origin"], cwd=destination)
        run(["git", "checkout", "-B", course.branch, f"origin/{course.branch}"], cwd=destination)
        run(["git", "clean", "-fd"], cwd=destination)
        return

    if destination.exists():
        raise RuntimeError(
            f"{destination} exists but is not a normal Git repository. "
            "Move or remove the directory before continuing."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    run(
        [
            "git",
            "clone",
            "--branch",
            course.branch,
            "--single-branch",
            course.repository,
            str(destination),
        ]
    )


def sync_courses(courses: list[Course], settings: Settings) -> None:
    for course in courses:
        if course.enabled:
            sync_course(course, settings)

    print("\nAll registered courses are up to date")
