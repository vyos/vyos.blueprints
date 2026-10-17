#!/usr/bin/env python3
"""Fail when a command sent to a VyOS CLI contains "?".

In the VyOS shell "?" lists completions ("Display all N possibilities? (y or n)")
and waits for an answer, so such a command never runs and the task hangs until
its timeout (for example "echo rc=$?", or a URL with a query string).
Checks vyos.vyos.vyos_command and ansible.netcommon.cli_command in roles and
Molecule playbooks.
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULES = ("vyos.vyos.vyos_command", "ansible.netcommon.cli_command")


def commands(task_args):
    cmds = task_args.get("commands")
    if cmds is None:
        cmds = [task_args.get("command")]
    for cmd in cmds if isinstance(cmds, list) else [cmds]:
        text = cmd.get("command") if isinstance(cmd, dict) else cmd
        if isinstance(text, str):
            yield text


def walk(node, path, bad):
    if isinstance(node, dict):
        for key, value in node.items():
            if key in MODULES and isinstance(value, dict):
                for text in commands(value):
                    if "?" in text:
                        bad.append(f"{path}: {text.strip()[:120]}")
            walk(value, path, bad)
    elif isinstance(node, list):
        for item in node:
            walk(item, path, bad)


def main():
    bad = []
    files = sorted((ROOT / "roles").rglob("*.yml")) + sorted((ROOT / "extensions" / "molecule").rglob("*.yml"))
    for path in files:
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        walk(data, path.relative_to(ROOT), bad)
    if bad:
        print('CLI commands containing "?" (the VyOS shell waits for an answer):')
        print("\n".join(f"  {line}" for line in bad))
        return 1
    print(f"cli commands: ok ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
