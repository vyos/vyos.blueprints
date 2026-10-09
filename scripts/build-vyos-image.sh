#!/usr/bin/env bash
# Build the VyOS container image for containerlab/Molecule with the official
# vyos-build "iso-to-oci" tool, as described in
# https://docs.vyos.io/en/1.5/installation/virtual/docker.html
#
#   scripts/build-vyos-image.sh <iso-path-or-url> [tag]   # build and import (default tag vyos:blueprints-ci)
#   scripts/build-vyos-image.sh --oci <iso-path-or-url> <out.tar.xz>   # build the image tarball only (CI)
#   scripts/build-vyos-image.sh --import <in.tar.xz> [tag]             # import a tarball built with --oci
#
# Needs xorriso, squashfs-tools, jq, tar, xz (the tool checks) and docker for importing.
#
# With MINISIGN_PUBKEY set, a downloaded ISO is verified against <url>.minisig
# before it is used (VyOS signs its images with minisign); a missing or bad
# signature stops the build.
set -euo pipefail

# iso-to-oci from vyos-build, pinned to a reviewed commit
ISO_TO_OCI_URL="https://raw.githubusercontent.com/vyos/vyos-build/f5a1e8334f772225d9e3ccdab45f6884cec28e59/scripts/iso-to-oci"
DEFAULT_TAG="vyos:blueprints-ci"

build_oci() {  # <iso-path-or-url> <out.tar.xz>
  local src="$1" out
  out="$(realpath -m "$2")"
  local work
  work="$(mktemp -d)"
  trap 'rm -rf "$work"' RETURN
  if [[ "$src" =~ ^https?:// ]]; then
    echo "I: downloading $src"
    curl -fL --retry 3 -o "$work/vyos.iso" "$src"
    if [[ -n "${MINISIGN_PUBKEY:-}" ]]; then
      echo "I: verifying the signature ($src.minisig)"
      curl -fL --retry 3 -o "$work/vyos.iso.minisig" "$src.minisig"
      minisign -Vm "$work/vyos.iso" -x "$work/vyos.iso.minisig" -P "$MINISIGN_PUBKEY"
    fi
    src="$work/vyos.iso"
  elif [[ -n "${MINISIGN_PUBKEY:-}" && -f "$src.minisig" ]]; then
    minisign -Vm "$src" -x "$src.minisig" -P "$MINISIGN_PUBKEY"
  fi
  curl -fsSL --retry 3 -o "$work/iso-to-oci" "$ISO_TO_OCI_URL"
  chmod +x "$work/iso-to-oci"
  (cd "$work" && ./iso-to-oci "$(realpath "$src")")
  mv "$work"/vyos-*-oci-*.tar.xz "$out"
  echo "I: image tarball: $out"
}

import_oci() {  # <in.tar.xz> [tag]
  local tag="${2:-$DEFAULT_TAG}"
  docker import "$1" "$tag" \
    --change 'CMD ["/sbin/init"]' \
    --change 'HEALTHCHECK --start-period=10s CMD systemctl is-system-running'
  echo "I: imported $tag"
}

case "${1:-}" in
  --oci)    [[ $# -eq 3 ]] || { echo "usage: $0 --oci <iso-path-or-url> <out.tar.xz>" >&2; exit 2; }
            build_oci "$2" "$3" ;;
  --import) [[ $# -ge 2 ]] || { echo "usage: $0 --import <in.tar.xz> [tag]" >&2; exit 2; }
            import_oci "$2" "${3:-}" ;;
  ""|-h|--help) sed -n '2,10p' "$0"; exit 2 ;;
  *)        tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
            build_oci "$1" "$tmp/vyos-oci.tar.xz"
            import_oci "$tmp/vyos-oci.tar.xz" "${2:-}" ;;
esac
