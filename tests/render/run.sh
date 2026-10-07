#!/usr/bin/env bash
# Offline render tests (no device, released vyos.vyos): each case renders a role with state=rendered and
# compares the commands with tests/render/cases/<role>/<case>/expected/<host>.txt.
#
#   tests/render/run.sh                 # all cases
#   tests/render/run.sh ha_vrrp         # cases whose "<role>/<case>" starts with this
#   UPDATE_GOLDEN=true tests/render/run.sh edge_nat   # regenerate golden files
#
# A case directory may contain vars.yml (shared inputs, passed as extra vars),
# inventory.yml (multi-node cases; per-host inputs live there) and roles (a
# comma-separated role list, for blueprints that combine several roles; such
# cases live under cases/blueprints/).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
# Test-only connection (tests/render/collections): the real network_cli, except
# that it never connects and reports VYOS_OFFLINE_OS_VERSION (default 1.5) as
# the device version, so released vyos.vyos renders offline.
export ANSIBLE_COLLECTIONS_PATH="$here/collections${ANSIBLE_COLLECTIONS_PATH:+:$ANSIBLE_COLLECTIONS_PATH}"
offline_version="${VYOS_OFFLINE_OS_VERSION:-1.5}"
update="${UPDATE_GOLDEN:-false}"
filter="${1:-}"
rc=0
for case_dir in "$here"/cases/*/*/; do
  case_dir="${case_dir%/}"
  role="$(basename "$(dirname "$case_dir")")"
  name="$(basename "$case_dir")"
  [[ -n "$filter" && "$role/$name" != "$filter"* ]] && continue
  inventory="$case_dir/inventory.yml"
  [[ -f "$inventory" ]] || inventory="$here/inventory.yml"
  args=(-i "$inventory" "$here/render.yml"
        -e "ansible_connection=blueprints_test.offline.network_cli"
        -e "vyos_offline_os_version=$offline_version"
        -e "role=$role" -e "case_dir=$case_dir" -e "update_golden=$update")
  [[ -f "$case_dir/vars.yml" ]] && args+=(-e "@$case_dir/vars.yml")
  # Blueprints that combine roles list them, comma-separated, in a "roles" file.
  [[ -f "$case_dir/roles" ]] && args+=(-e "render_roles=$(tr -d '[:space:]' < "$case_dir/roles")")
  mkdir -p "$case_dir/expected"
  echo "=== $role/$name"
  # fresh persistent-connection sockets per case (cases reuse TEST-NET addresses)
  ANSIBLE_PERSISTENT_CONTROL_PATH_DIR="$(mktemp -d)"
  export ANSIBLE_PERSISTENT_CONTROL_PATH_DIR
  if ! ansible-playbook "${args[@]}"; then
    echo "FAILED: $role/$name" >&2
    rc=1
  fi
  rm -rf "$ANSIBLE_PERSISTENT_CONTROL_PATH_DIR"
done
exit "$rc"
