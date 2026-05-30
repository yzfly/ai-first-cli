#!/usr/bin/env python3
"""Validate a Claude skill's SKILL.md frontmatter. Self-contained, no deps.

Usage: python3 validate_skill.py <skill-directory>
Exit 0 if valid, 1 otherwise.
"""
import re
import sys
from pathlib import Path


def validate(skill_dir: str) -> tuple[bool, str]:
    path = Path(skill_dir)
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return False, f"SKILL.md not found in {skill_dir}"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"
    frontmatter = match.group(1)

    if "name:" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description:" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name_match = re.search(r"name:\s*(.+)", frontmatter)
    if name_match:
        name = name_match.group(1).strip().strip('"').strip("'")
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' must be hyphen-case (a-z, 0-9, -)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with '-' or contain '--'"

    desc_match = re.search(r"description:\s*(.+)", frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"

    if len(frontmatter) > 1024:
        return False, f"Frontmatter too long ({len(frontmatter)} > 1024 chars)"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 validate_skill.py <skill-directory>")
        sys.exit(1)
    ok, msg = validate(sys.argv[1])
    print(("✅ " if ok else "❌ ") + msg)
    sys.exit(0 if ok else 1)
