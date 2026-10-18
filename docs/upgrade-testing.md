# Testing the upgrade role on a VM

Containers cannot boot a new VyOS image, so the `upgrade` Molecule scenario covers the
skip and failure paths only. The install-and-reboot path needs a VyOS VM. This is the
checklist for that job (planned together with the vyos.vyos integration tests on VMs).

## Setup

1. A VM installed from an **older** VyOS image (for example an earlier Stream release),
   with SSH reachable from the runner.
2. The **newer** ISO **with its `.minisig`** served from the runner. In QEMU's user-mode
   network the runner is `10.0.2.2`, for example `python3 -m http.server 8000`.

## Checks

| Run | Expect |
|---|---|
| `ansible-playbook vyos.blueprints.upgrade -i <inventory> -e upgrade_image_url=http://10.0.2.2:8000/<iso> -e upgrade_expected_version=<new>` | passes; afterwards `show version` reports the new version, `show system image` lists both images with the new one as default boot, and `backup_root` holds a `.cfg`, `.set` and `.json` from before the upgrade |
| the same command again | the router is skipped: no backup, no install, no reboot |
| an image URL that does not exist | fails at the download step, **before** any reboot; no staged file is left in `/root`; the router keeps its version |
| the ISO served **without** its `.minisig` | fails before any reboot with "the image has no signature"; with `-e upgrade_allow_unsigned=true` it installs |

## What it proves

Also watch the controller during the install: since the role downloads the image itself
(quietly) and installs the local file, the connection process should stay idle instead of
at 100% CPU, which is what `add system image <url>` caused with its progress bar.


The prompt answers against the real installer, the signature handling, the reboot and
reconnect, the default-boot and version checks, and the skip on a second run.

## Tested on

| Date | From -> to | Platform | Result |
|---|---|---|---|
| 2026-10-17 | VyOS 1.4.2 -> VyOS Stream 2026.03 | KVM VM, upgrade from community-downloads.vyos.dev | full path passes (`failed=0`): backup, quiet download to `/root`, signature valid, four installer questions answered, `2026.03` default boot, reboot confirmed by a new boot ID, version `2026.03`; a second run skips the router (`ok=3 changed=0`) |

Found and fixed on the way (all invisible in containers):

- the installer's download progress bar overloads the CLI connection (100% CPU on the
  controller, command timeout): the role downloads quietly and installs the local file;
- `/tmp` and `/var/tmp` are small tmpfs; the 1.4.2 installer itself downloads to root's
  home, so the role stages in `/root` (with sudo);
- for a local file the installer skips the signature check: the role runs the installer's
  own minisign check before installing;
- `?` in a command makes the VyOS shell list completions and wait (`echo $?`): no `?` in
  any CLI command (guard: `scripts/check-cli-commands.py`);
- with `check_all: false`, network_cli answers only the first question of a command:
  `check_all: true`, with the questions in the installer's order;
- a fast reboot is back before "SSH down" is noticed: the reboot is confirmed by a changed
  boot ID instead.

