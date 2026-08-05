from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_courses, load_settings
from .navigation import update_mkdocs
from .stats import generate_stats
from .sync import sync_courses
from .validation import validate_all


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="training-manager",
        description="Manage training repositories and MkDocs navigation.",
    )
    parser.add_argument(
        "command",
        choices=["sync", "validate", "nav", "stats", "build"],
    )
    parser.add_argument("--courses", default="config/courses.json")
    parser.add_argument("--settings", default="config/settings.json")
    args = parser.parse_args()

    courses = load_courses(Path(args.courses).expanduser().resolve())
    settings = load_settings(Path(args.settings).expanduser().resolve())

    if args.command == "sync":
        sync_courses(courses, settings)
    elif args.command == "validate":
        validate_all(courses, settings)
    elif args.command == "nav":
        update_mkdocs(courses, settings)
    elif args.command == "stats":
        generate_stats(courses, settings)
    elif args.command == "build":
        sync_courses(courses, settings)
        validate_all(courses, settings)
        update_mkdocs(courses, settings)
        generate_stats(courses, settings)


if __name__ == "__main__":
    main()
