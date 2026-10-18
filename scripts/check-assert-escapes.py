"""Check `assert` conditions in role tasks and Molecule playbooks.

1. Every condition must be a string. An unquoted condition containing ": " (for
   example a regex like 'Paths: ...') is read by YAML as a mapping, and Ansible
   fails with "Conditional expressions must be strings".
2. No single-backslash \\b in a condition. ansible-core evaluates Jinja string
   literals in conditions with Python's escape rules, so '\\b' becomes a backspace
   and the regex never matches ({{ }} templates are not affected). Write a word
   boundary without a backslash: (?<![A-Za-z0-9_]) before, (?![A-Za-z0-9_]) after.
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(ROOT.glob("roles/*/tasks/*.yml")) + sorted(ROOT.glob("extensions/molecule/*/*.yml"))
bad = []


def tasks_of(node):
    """Yield every task dict in a playbook or task list, including blocks."""
    if isinstance(node, list):
        for item in node:
            yield from tasks_of(item)
    elif isinstance(node, dict):
        if "hosts" in node:  # a play
            for key in ("pre_tasks", "tasks", "post_tasks", "handlers"):
                yield from tasks_of(node.get(key) or [])
            return
        yield node
        for key in ("block", "rescue", "always"):
            yield from tasks_of(node.get(key) or [])


for path in FILES:
    rel = path.relative_to(ROOT)
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError:
        continue  # not our concern here; ansible-lint reports it
    for task in tasks_of(data):
        module = task.get("ansible.builtin.assert") or task.get("assert")
        if not isinstance(module, dict) or "that" not in module:
            continue
        conditions = module["that"] if isinstance(module["that"], list) else [module["that"]]
        for cond in conditions:
            if not isinstance(cond, str):
                bad.append(f"{rel}: task '{task.get('name', '?')}': condition is a {type(cond).__name__}, not a string (quote it, or avoid ': ')")
    # single-backslash \b, line-based (the YAML loader keeps the backslashes)
    in_that, indent = False, 0
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.match(r"^(\s*)that:", line)
        if match:
            in_that, indent = True, len(match.group(1))
        elif in_that and line.strip() and len(line) - len(line.lstrip()) <= indent:
            in_that = False
        if in_that and "\\b" in line and "\\\\b" not in line:
            bad.append(f"{rel}:{number}: single-backslash \\b in an assert condition (it becomes a backspace)")
if bad:
    print("assert condition problems:")
    print("\n".join(f"  {b}" for b in bad))
    sys.exit(1)
print(f"assert conditions: ok ({len(FILES)} files)")
