"""Check the containerlab topologies (Molecule scenarios and examples).

Every node's `exec` entry must be a string. An unquoted value ending in a colon,
such as an IPv6 address ending in "::", is read by YAML as a mapping, and
containerlab then refuses the whole topology.
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
bad = []
files = sorted(ROOT.glob("extensions/molecule/*/topology.clab.yml")) + sorted(ROOT.glob("examples/*/topology.clab.yml"))
for path in files:
    nodes = (yaml.safe_load(path.read_text()).get("topology") or {}).get("nodes") or {}
    for name, node in nodes.items():
        commands = (node or {}).get("exec")
        if commands is None:
            continue
        if not isinstance(commands, list):
            bad.append(f"{path.relative_to(ROOT)}: node {name}: exec must be a list, not a {type(commands).__name__}")
            continue
        for entry in commands:
            if not isinstance(entry, str):
                bad.append(f"{path.relative_to(ROOT)}: node {name}: {entry!r} (quote it)")
if bad:
    print("exec entries that are not strings:")
    print("\n".join(f"  {b}" for b in bad))
    sys.exit(1)
print(f"topologies: ok ({len(files)} files)")
