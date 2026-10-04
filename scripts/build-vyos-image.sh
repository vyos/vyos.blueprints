#!/usr/bin/env bash
# Build a VyOS container image from an ISO for containerlab
# (procedure from containerlab.dev/manual/kinds/vyosnetworks_vyos).
#
#   scripts/build-vyos-image.sh <iso-path-or-url> [image-tag]
#
# Needs: bsdtar (libarchive-tools), sqfs2tar (squashfs-tools-ng), docker.
set -euo pipefail
src="${1:?usage: $0 <iso-path-or-url> [image-tag]}"
tag="${2:-vyos:blueprints-ci}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

if [[ "$src" =~ ^https?:// ]]; then
  curl -fL --retry 3 -o "$work/vyos.iso" "$src"
else
  cp "$src" "$work/vyos.iso"
fi

cd "$work"
bsdtar -xf vyos.iso live/filesystem.squashfs
sqfs2tar live/filesystem.squashfs > rootfs.tar
cat > Dockerfile <<'DOCKERFILE'
FROM scratch
ADD rootfs.tar /
RUN for service in getty.target auditd.service; do systemctl mask $service; done && \
    systemctl disable kea-dhcp-ddns-server.service
HEALTHCHECK --start-period=10s CMD systemctl is-system-running
CMD ["/sbin/init"]
DOCKERFILE
docker build -t "$tag" .
echo "built $tag"
