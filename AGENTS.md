# AGENTS.md

## Project purpose

`vyos.blueprints` is an Ansible collection of **roles** that deploy the VyOS 1.5
Configuration Blueprints (docs.vyos.io/en/1.5/configexamples), plus building-block
roles (firewall, NAT, routing, VPNs, management) and operational roles (`backup`,
`upgrade`). It contains no modules; roles drive the `vyos.vyos` resource modules.

## Layout

- `roles/<role>/` - `meta/argument_specs.yml` (validated inputs, the role's
  documentation), `defaults/`, `vars/`, `templates/` (module input as YAML),
  `tasks/main.yml` and `tasks/verify.yml` (operational checks).
- `tests/render/` - offline render tests: each case renders roles with
  `state: rendered` and compares with golden `set` commands. A test-only
  connection (`tests/render/collections`) reports the VyOS version, so no device
  is needed.
- `extensions/molecule/<scenario>/` - containerlab-based tests on VyOS containers.
- `examples/` - runnable projects per blueprint; `docs/upstream-findings.md` -
  vyos.vyos bugs and gaps the roles work around.

## Conventions

- Prefer vyos.vyos resource modules; use `vyos.vyos.vyos_config` only where no
  module (or option) exists, and say so in a comment and in the argument spec.
- Every role honours `vyos_blueprints_render_only` and appends to
  `vyos_blueprints_rendered`; secrets are masked there and hidden with `no_log`.
- Building-block roles do nothing when their key input is empty.
- Golden files change only on purpose: regenerate with
  `UPDATE_GOLDEN=true tests/render/run.sh <role>/<case>` and check them against
  the docs page.
- PR titles and commit messages start with a task key (`T<digits>: ...`); every
  PR adds a changelog fragment in `changelogs/fragments/`.

## Checks before a PR

`ansible-lint`, `tests/render/run.sh` (or the cases you touched), and
`molecule syntax -s <scenario>` from `extensions/`.
