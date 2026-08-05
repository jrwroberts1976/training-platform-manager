from __future__ import annotations

import re
import subprocess
from pathlib import Path


def run(command: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


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
        "Azure": "Azure",
        "Ipv4": "IPv4",
        "Ipv6": "IPv6",
        "Snmp": "SNMP",
    }

    for old, new in replacements.items():
        title = title.replace(old, new)

    return title
