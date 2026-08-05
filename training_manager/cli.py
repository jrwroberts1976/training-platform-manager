from __future__ import annotations

import argparse
from pathlib import Path

from .catalog import generate_catalog
from .config import load_courses, load_settings
from .navigation import update_mkdocs
from .scaffold import CreateCourseOptions, create_course, docker_options
from .sync import sync_courses
from .validation import validate_all


def parse_modules(value: str) -> list[str]:
    modules = [item.strip() for item in value.split(",") if item.strip()]
    if not modules:
        raise argparse.ArgumentTypeError("At least one module is required")
    return modules


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="training-manager",
        description="Manage repositories and generate the engineering learning platform.",
    )
    parser.add_argument("--courses", default="config/courses.json")
    parser.add_argument("--settings", default="config/settings.json")

    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ["sync", "validate", "nav", "catalog", "build"]:
        subparsers.add_parser(command)

    create = subparsers.add_parser("create-course")
    create.add_argument("slug")
    create.add_argument("--title")
    create.add_argument("--level", default="Intermediate")
    create.add_argument("--hours", type=int, default=20)
    create.add_argument("--description")
    create.add_argument("--modules", type=parse_modules)
    create.add_argument("--template", choices=["docker"])
    create.add_argument("--github", action="store_true")
    create.add_argument("--private", action="store_true")
    create.add_argument("--register", action="store_true")
    create.add_argument("--build", action="store_true")

    args = parser.parse_args()
    courses_path = Path(args.courses).expanduser().resolve()
    settings_path = Path(args.settings).expanduser().resolve()
    settings = load_settings(settings_path)

    if args.command == "create-course":
        if args.template == "docker":
            options = docker_options()
            options.create_github = args.github
            options.public = not args.private
            options.register = args.register
            options.run_build = args.build
        else:
            slug = args.slug
            title = args.title or slug.replace("-", " ").title()
            modules = args.modules or ["Introduction", "Core Concepts", "Practical Labs", "Final Project"]
            options = CreateCourseOptions(
                slug=slug,
                title=title,
                level=args.level,
                estimated_hours=args.hours,
                modules=modules,
                description=args.description or f"Professional training covering {title}.",
                public=not args.private,
                create_github=args.github,
                register=args.register,
                run_build=args.build,
            )

        create_course(options, settings, courses_path)
        return

    courses = load_courses(courses_path)

    if args.command == "sync":
        sync_courses(courses, settings)
    elif args.command == "validate":
        validate_all(courses, settings)
    elif args.command == "nav":
        update_mkdocs(courses, settings)
    elif args.command == "catalog":
        generate_catalog(courses, settings)
    elif args.command == "build":
        sync_courses(courses, settings)
        validate_all(courses, settings)
        update_mkdocs(courses, settings)
        generate_catalog(courses, settings)


if __name__ == "__main__":
    main()
