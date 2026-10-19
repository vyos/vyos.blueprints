# Contributing

## Pull requests

- Sign the VyOS CLA (the CLA check comments on your first PR).
- Start the PR title and every commit message with a task key from vyos.dev,
  e.g. `T1234: add the foo role` (checked by Mergify).
- Add a changelog fragment in `changelogs/fragments/` (keys: `major_changes`,
  `minor_changes`, `bugfixes`, `breaking_changes`, `deprecated_features`,
  `removed_features`, `security_fixes`, `known_issues`, `doc_changes`, `trivial`).
- In `assert` conditions (`that:`), never write `\b` with a single backslash: there it
  becomes a backspace. `scripts/check-assert-escapes.py` (run in CI) explains the alternative.
- After changing a role's `meta/argument_specs.yml`, regenerate its README with
  `python3 scripts/gen-role-readmes.py` (CI checks they match).
- Optional: `pre-commit install` runs the same formatting checks locally.

### Molecule in CI

The Molecule matrix in `.github/workflows/tests.yml` has two lists: **required**
scenarios (they must pass for a PR to merge) and **experimental** ones (they run on
every build but do not fail it). A scenario moves from experimental to required once
it passes; [docs/molecule-status.md](docs/molecule-status.md) tracks the open ones.

To iterate on scenarios without the full pipeline, push with `[skip ci]` in the
commit message and start only Molecule:

    gh workflow run tests.yml --ref <branch> -f molecule_only=true -f scenarios='["<scenario>"]'

Every run uploads `molecule-logs-<scenario>`: the containerlab deploy log and a
post-mortem of every lab node (configuration, routes, qdiscs, BGP, IPsec SAs, logs).

# Contributing a blueprint role

A role should implement one page of the VyOS
[Configuration Blueprints](https://docs.vyos.io/en/1.5/configexamples/index.html),
or a building block several pages share.

## Checklist

1. **Inputs** – `meta/argument_specs.yml` with a `main` entry (and `verify`).
   Prefix every variable with the role name (`<role>_...`). Keep the blueprint's
   vocabulary so the docs page and the role read alike.
2. **Defaults** – mirror the argument-spec defaults in `defaults/main.yml`
   (ansible-core validates against the spec but does not apply its defaults).
3. **Tasks** – use vyos.vyos resource modules with
   `state: "{{ '<rendered>' if vyos_blueprints_render_only else 'merged' }}"`
   (see `vars/main.yml` in existing roles), register each result, and finish
   with the "Collect rendered commands" task. Build module `config` from small
   templates in `templates/` rather than long inline Jinja.
   Use `vyos.vyos.vyos_config` only where no resource module exists, and say
   so in the argument spec.
4. **Verify** – `tasks/verify.yml` with operational checks (`show ...`) that
   prove the blueprint works, not just that commands were accepted.
5. **Render test** – `tests/render/cases/<role>/<case>/` with `vars.yml`
   (and `inventory.yml` for multi-node). Generate the golden file with
   `UPDATE_GOLDEN=true tests/render/run.sh <role>/<case>` and check it
   against the docs page by hand before committing.
6. **Molecule scenario** – `extensions/molecule/<role>/` with a containerlab
   topology, inventory, converge and verify. Copy an existing scenario.
7. **Example** – add or extend a directory under `examples/` if the role is a
   user-facing blueprint.
8. **README table** – one line in the top-level README.

## Test tiers

| Tier         | Command                                    | Needs                                                                                              |
| ------------ | ------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| 0 – lint     | `ansible-lint`                             | nothing                                                                                            |
| 1 – render   | `tests/render/run.sh`                      | nothing - a test-only connection reports the VyOS version (`VYOS_OFFLINE_OS_VERSION`, default 1.5) |
| 2 – molecule | `cd extensions && molecule test -s <role>` | docker, containerlab, a VyOS image                                                                 |

Run tiers 0 and 1 before opening a PR; CI runs all three.

### Local setup

```bash
mkdir -p ~/src/ansible_collections/vyos
git clone https://github.com/vyos/vyos.blueprints ~/src/ansible_collections/vyos/blueprints
cd ~/src/ansible_collections/vyos/blueprints
pip install ansible-core ansible-lint ansible-pylibssh molecule
ansible-galaxy collection install -r tests/requirements.yml -p ~/src
export ANSIBLE_COLLECTIONS_PATH=~/src
scripts/build-vyos-image.sh /path/to/vyos-1.5-*.iso    # once, for tier 2 (official iso-to-oci tool)
# or reuse an image built per docs.vyos.io (Run VyOS as a container): docker tag <image> vyos:blueprints-ci
```

Set `CLAB_BECOME=false` if you run containerlab without sudo.

### Container limitations

Containerized VyOS shares the host kernel. Blueprints that depend on kernel
modules or capabilities the CI host lacks (PPPoE/L2TP, some QoS, possibly
DMVPN) may need a VM-based scenario instead; note this in the scenario's
`molecule.yml`.
