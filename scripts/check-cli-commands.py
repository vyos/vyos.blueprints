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


class AnsibleTagLoader(yaml.SafeLoader):
    """SafeLoader that accepts Ansible tags (!vault, !unsafe, ...) without acting on them."""


def _tagged_value(loader, tag_suffix, node):
    # The value of a tagged scalar is kept as text (a !vault value stays ciphertext).
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


AnsibleTagLoader.add_multi_constructor("!", _tagged_value)


def main():
    bad = []
    unreadable = []
    files = sorted((ROOT / "roles").rglob("*.yml")) + sorted((ROOT / "extensions" / "molecule").rglob("*.yml"))
    for path in files:
        try:
            data = yaml.load(path.read_text(), Loader=AnsibleTagLoader)  # noqa: S506 - safe loader subclass
        except yaml.YAMLError as err:
            unreadable.append(f"{path.relative_to(ROOT)}: {str(err).splitlines()[0]}")
            continue
        walk(data, path.relative_to(ROOT), bad)
    if unreadable:
        print("Files the CLI command check cannot read (fix them, or the check is incomplete):")
        print("\n".join(f"  {line}" for line in unreadable))
    if bad:
        print('CLI commands containing "?" (the VyOS shell waits for an answer):')
        print("\n".join(f"  {line}" for line in bad))
    if bad or unreadable:
        return 1
    print(f"cli commands: ok ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
