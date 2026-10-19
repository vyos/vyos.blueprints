========================================
VyOS Blueprints Collection Release Notes
========================================

.. contents:: Topics

v1.0.0
======

Release Summary
---------------

First stable release of vyos.blueprints: Ansible roles that implement the
VyOS 1.5 Configuration Blueprints from docs.vyos.io, so a blueprint such as a
VRRP pair, a zone-based firewall, OSPF or BGP unnumbered, an L3VPN, a
route-based IPsec VPN to Azure or Google Cloud, or a dual-hub DMVPN is applied
from a short description of the routers in the inventory.

The collection contains the blueprint roles, the building-block roles they
are made of (interfaces, firewall, NAT, routing, VPNs, management), and two
operational roles: ``backup`` for bulk configuration backups with retention,
and ``upgrade`` for rolling image upgrades with backup, signature check,
reboot and version check, one router at a time. Every role has validated
inputs, a render-only preview mode, and a ``verify`` entry point with
operational checks.

Testing: every role is render-tested on each pull request; 23 blueprint
scenarios are tested live against VyOS 1.5 in containerlab (traffic,
idempotence, verify checks); ``upgrade`` is tested on a VM from VyOS 1.4.2 to
VyOS Stream 2026.03. The bug fixes and changes listed below were made during
that pre-release testing.

Requires ansible-core 2.16 or newer and vyos.vyos 6.1.0 or newer. With
1.0.0, the role inputs are a stable interface under semantic versioning.

Minor Changes
-------------

- upgrade - new ``upgrade_allow_unsigned`` (default ``false``). ``add system image`` asks before installing an image without a signature; the role now answers that question instead of waiting for its timeout, and always declines an image with an invalid signature.
- upgrade - new ``upgrade_stage_dir`` (default ``/root``, where the VyOS 1.4.2 installer downloads; staging uses sudo) and ``upgrade_stage_min_free_mb`` (default ``1024``).
- upgrade - uses ``vyos.vyos.vyos_command`` (with prompt answers) instead of ``ansible.netcommon.cli_command``.

Bugfixes
--------

- backup - the default ``backup_root`` is now ``backups`` in the directory Ansible runs from. It was ``{{ playbook_dir }}/backups``, which for the collection playbook (``ansible-playbook vyos.blueprints.backup``) is inside the installed collection.
- bgp - neighbours without address-family options are activated for ipv4-unicast (or ipv6-unicast); VyOS 1.5 leaves them inactive otherwise.
- bgp, bgp_unnumbered, l3vpn, vrf_lite, ipsec_route_based - BGP session checks accept an established session that shows ``(Policy)`` instead of a prefix count.
- bgp_unnumbered - drop ``parameters default no-ipv4-unicast``, which VyOS 1.5 rejects; VyOS always applies it.
- bgp_unnumbered - the BGP neighbour now renders without a bare ``interface v6only`` line, which made every run report a change.
- firewall - the verify check matches the VyOS 1.5 ``show firewall`` header (lower-case family name).
- ipsec_route_based - BGP neighbours without address-family options are activated for ipv4-unicast (or ipv6-unicast), as in the bgp role.
- ipsec_route_based, ipsec_policy_based - peer names are checked up front; VyOS 1.5 only accepts letters, digits, hyphens and underscores.
- management - SNMP trap targets with a community or port no longer report a change on every run (idempotence).
- qos - the verify check uses ``show qos shaper`` (``show qos`` alone is incomplete in VyOS 1.5).
- upgrade - a failed ``add system image`` (for example "The image cannot be fetched from ...") now fails the run with the installer's message; the role requires the installer's "Copying system image files" step. Before, it continued and failed later with an unrelated templating error.
- upgrade - all four installer questions are answered now (``check_all: true``). With ``check_all: false`` network_cli answers only the first question of a command, so the installer waited at "set the new image as the default one for boot". The role also fails early, with instructions, when ``/mnt/installation`` is left over from an interrupted install.
- upgrade - an image given as a URL is now downloaded by the role (quietly, with ``curl``) into ``upgrade_stage_dir`` on the router, its signature verified as the VyOS installer does, and then installed from the local file. The installer's own download draws a progress bar that overloaded the CLI connection, so ``add system image <url>`` ran into the command timeout on a real router although the download itself took about 90 seconds. The staged files are removed afterwards, also when the upgrade fails.
- upgrade - result markers (``download-ok`` and the others) must stand on a line of their own, so an echoed command line can no longer satisfy a check; a render-only run (``vyos_blueprints_render_only``) skips the role entirely instead of reaching the install and reboot steps.
- upgrade - the check for installer errors now detects ``Error:`` lines from ``add system image``.
- upgrade - the installer's questions are matched in both the 1.4.2/1.5 wording ("copy ...") and the earlier one ("save ..."), and answered with ``yes``/``no``, which both accept.
- upgrade - the reboot is confirmed by a changed boot ID instead of waiting for SSH to go down. A fast-booting router could be back before the first check; the port then never looked closed and the task waited for its timeout although the upgrade had succeeded.
- upgrade - the role's own commands no longer contain ``?``: the VyOS shell treats it as a request for completions and waits for an answer, so the download never started. Image URLs containing ``?`` are rejected with a clear message.
- upgrade - when the installer stops on a signature question, the run fails with a message that names the cause.
- verify tasks - checks with a word boundary in ``assert`` conditions could never match (``\b`` became a backspace); rewritten without backslash escapes.
- vrf_lite - every VRF with BGP gets a ``system-as``, which VyOS 1.5 requires.
- wan_load_balance - pruning now deletes the highest node no longer wanted, so no empty node is left behind and a repeated run reports no change.
- wireguard - the verify check reads handshakes from ``show interfaces wireguard <name> summary``.

Documentation Changes
---------------------

- Add SECURITY.md with the private vulnerability reporting process.
- README - add the collection's beta status, what is tested, CI badges and a security section.
