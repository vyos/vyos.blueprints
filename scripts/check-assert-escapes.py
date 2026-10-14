#!/usr/bin/env python3
"""Fail if an assert condition (`that:`) in a role uses a single-backslash \\b.

In `that:` conditions ansible-core evaluates Jinja string literals with Python's
escape rules, so '\\b' becomes a backspace character and the regex never matches
(templates in `{{ }}` are not affected). Write a word boundary without a backslash:
(?:(?<![A-Za-z0-9_])(?=[A-Za-z0-9_])|(?<=[A-Za-z0-9_])(?![A-Za-z0-9_]))
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
bad = []
for path in sorted(ROOT.glob("roles/*/tasks/*.yml")):
    in_that, indent = False, 0
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.match(r"^(\s*)that:", line)
        if match:
            in_that, indent = True, len(match.group(1))
        elif in_that and line.strip() and len(line) - len(line.lstrip()) <= indent:
            in_that = False
        if in_that and "\\b" in line and "\\\\b" not in line:
            bad.append(f"{path.relative_to(ROOT)}:{number}")
if bad:
    print("single-backslash \\b in assert conditions (it becomes a backspace):")
    print("\n".join(f"  {b}" for b in bad))
    sys.exit(1)
print("assert conditions: ok")
