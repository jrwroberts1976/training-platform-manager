from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


def run(
    command: list[str],
    cwd: Path | None = None,
    capture: bool = False,
    check: bool = True,
) -> str:
    print("+", " ".join(command))
    result = subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=capture,
    )
    return result.stdout.strip() if capture else ""


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def numeric_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)", path.name)
    return (int(match.group(1)) if match else 9999, path.name)


def markdown_title(path: Path) -> str:
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()

    title = re.sub(r"^\d+-", "", path.stem).replace("-", " ").title()

    replacements = {
        "Github": "GitHub",
        "Cicd": "CI/CD",
        "Dns": "DNS",
        "Dhcp": "DHCP",
        "Api": "API",
        "Ssh": "SSH",
        "Sso": "SSO",
        "Rbac": "RBAC",
        "Yaml": "YAML",
        "Aws": "AWS",
        "Ipv4": "IPv4",
        "Ipv6": "IPv6",
        "Snmp": "SNMP",
        "Sre": "SRE",
        "Iac": "IaC",
    }

    for old, new in replacements.items():
        title = title.replace(old, new)

    return title
