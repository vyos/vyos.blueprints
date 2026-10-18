# vyos.blueprints

[![CI](https://github.com/vyos/vyos.blueprints/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/vyos/vyos.blueprints/actions/workflows/tests.yml)
[![Security](https://github.com/vyos/vyos.blueprints/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/vyos/vyos.blueprints/actions/workflows/security.yml)

Ansible roles that deploy the [VyOS Configuration Blueprints](https://docs.vyos.io/en/1.5/configexamples/index.html)
on top of the [vyos.vyos](https://github.com/vyos/vyos.vyos) resource modules.
Each role turns one blueprint (or one building block shared by several) into a
validated, idempotent, testable unit.

## Description

**Beta.** All blueprints from the VyOS 1.5 configuration examples are implemented,
together with building-block roles and operational roles for bulk backups and
rolling upgrades. Every role has documented, validated inputs and a `verify` entry point
with operational checks.

## Requirements

- ansible-core 2.16 or newer; sanity-tested on 2.16, 2.18 and 2.20
- Python 3.10 or newer on the control node
- The collections [vyos.vyos](https://github.com/vyos/vyos.vyos) 6.1.0+ and
  [ansible.netcommon](https://github.com/ansible-collections/ansible.netcommon) 6.0.0+,
  installed automatically with this collection
- An SSH library for `ansible.netcommon.network_cli`:
  [ansible-pylibssh](https://pypi.org/project/ansible-pylibssh/) (recommended) or paramiko
- VyOS 1.5, reachable over SSH. The roles follow the VyOS 1.5 documentation. The
  operational roles `backup` and `upgrade` are also tested on VyOS 1.4.2 (including the
  upgrade from 1.4.2 to the 1.5 line).

## Installation

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install vyos.blueprints
```

Or list it in a `requirements.yml`:

```yaml
collections:
  - name: vyos.blueprints
```

```bash
ansible-galaxy collection install -r requirements.yml
```

Until the first release is published, install from GitHub:

```bash
ansible-galaxy collection install git+https://github.com/vyos/vyos.blueprints.git
```

To upgrade to the newest version, add `--upgrade` to the install command.

## Use cases

- **Deploy a VyOS configuration blueprint**, such as a VRRP pair, a zone-based firewall,
  a route-based IPsec VPN to Azure or Google Cloud, or a DMVPN with dual hubs, from a
  short description of the routers in your inventory.
- **Preview** what a role would send, without touching a router (render-only mode).
- **Back up** the configuration of every router in one run, with retention.
- **Upgrade** routers to a new VyOS image one at a time: backup, download, signature
  check, install, reboot, version check; routers already upgraded are skipped.

### Quick start

After installing the collection:

```bash
ansible-playbook vyos.blueprints.install_examples   # copies runnable examples to ./vyos-blueprints-examples
```

Then apply roles to your routers, for example a VRRP pair:

```yaml
# site.yml
- hosts: ha_pair
  gather_facts: false
  roles:
    - vyos.blueprints.base
    - vyos.blueprints.ha_vrrp
```

See [docs/using.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/using.md) for the inventory contract, multi-node
conventions and the render-only preview mode.

### Roles

| Role | What it does | Blueprint |
|---|---|---|
| `vyos.blueprints.base` | Hostname, interfaces and VLAN sub-interfaces, IPv4/IPv6 addressing, NTP, remote syslog | building block |
| `vyos.blueprints.edge_nat` | WAN (DHCP or static), default route, source NAT masquerade | small-office edge |
| `vyos.blueprints.ha_vrrp` | Two-node VRRP, sync-group, conntrack-sync | [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.ospf_unnumbered` | OSPF over unnumbered point-to-point links with ECMP, MD5 auth, redistribute connected | [OSPF unnumbered with ECMP](https://docs.vyos.io/en/1.5/configexamples/ospf-unnumbered.html) |
| `vyos.blueprints.bgp_unnumbered` | eBGP over IPv6 link-local interfaces, extended next-hop, ECMP, redistribute connected | [BGP IPv6 unnumbered with extended nexthop](https://docs.vyos.io/en/1.5/configexamples/bgp-ipv6-unnumbered.html) |
| `vyos.blueprints.zone_firewall` | Zones, one ruleset per zone-pair-direction (IPv4 and IPv6), base established/invalid rules, default-log | [Zone-Policy example](https://docs.vyos.io/en/1.5/configexamples/zone-policy.html) |
| `vyos.blueprints.vrf_firewall` | VRFs and tables, VLAN/PPPoE VRF membership, inter-VRF route leaking, forward/input filters, state policy | [VRF and firewall example](https://docs.vyos.io/en/1.5/configexamples/fwall-and-vrf.html) |
| `vyos.blueprints.bridge_firewall` | Bridges, interface groups, bridge prerouting/forward rulesets, IPv4 rulesets for routed traffic and router access | [Bridge and firewall example](https://docs.vyos.io/en/1.5/configexamples/fwall-and-bridge.html) |
| `vyos.blueprints.ipsec_route_based` | Route-based site-to-site IPsec over VTI (IKEv1/IKEv2, PSK), optional OSPF or BGP inside the tunnel | [Route-based ... VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-route-based.html), [Route-based ... VyOS and Palo Alto](https://docs.vyos.io/en/1.5/configexamples/ipsec-pa-route-based.html), [Route-Based ... to Azure (BGP)](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-bgp.html), [Route-Based Redundant ... to Azure](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-dual-bgp.html), [Route-Based ... to Google Cloud HA VPN](https://docs.vyos.io/en/1.5/configexamples/gcp-ha-vpn-bgp.html) |
| `vyos.blueprints.ipsec_policy_based` | Policy-based site-to-site IPsec with traffic selectors (IKEv1/IKEv2, PSK) | [Policy-based Site-to-Site VPN IPsec between VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-policy-based.html) |
| `vyos.blueprints.firewall` | Firewall network/address/port groups, IPv4/IPv6 input, forward and output filters | building block; used by [Policy-Based Site-to-Site VPN and Firewall Configuration](https://docs.vyos.io/en/1.5/configexamples/policy-based-ipsec-and-firewall.html) |
| `vyos.blueprints.nat` | Source NAT (masquerade, SNAT, exclusions) and destination NAT | building block; used by [Policy-Based Site-to-Site VPN and Firewall Configuration](https://docs.vyos.io/en/1.5/configexamples/policy-based-ipsec-and-firewall.html) |
| `vyos.blueprints.gre_tunnel` | GRE and other tunnel interfaces (endpoints, MTU, MSS clamping, addresses) | building block; used by [Site-to-Site IPSec VPN to Cisco using FlexVPN](https://docs.vyos.io/en/1.5/configexamples/site-2-site-cisco.html) |
| `vyos.blueprints.bonding` | Bonding (LAG/LACP) interfaces | building block; used by [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.wireguard` | WireGuard interfaces and peers (1.4+/1.5 syntax) | building block; used by [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.route_policy` | Access-lists, prefix-lists and route-maps (incl. AS-path prepend) | building block; used by [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.ospf` | OSPFv2 - areas, interface timers/costs/auth, redistribution with access-list export filters, import route-map | building block; used by [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.bgp` | BGP - neighbours, networks, redistribution with metric, per-neighbour import/export route-maps | building block; used by [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `vyos.blueprints.vrf_lite` | VRFs with static routes, MP-BGP route leaking (RD/RT, VPN import/export, import route-maps), eBGP inside a VRF | [Inter-VRF Routing over VRF Lite](https://docs.vyos.io/en/1.5/configexamples/inter-vrf-routing-vrf-lite.html) |
| `vyos.blueprints.wan_load_balance` | WAN load balancing and failover with health checks; owns its rules (stale rule settings are pruned) | [WAN Load Balancer examples](https://docs.vyos.io/en/1.5/configexamples/wan-load-balancing.html) (all 5) |
| `vyos.blueprints.pppoe` | PPPoE client with IPv6 autoconf and DHCPv6 prefix delegation | [PPPoE IPv6 Basic Setup for Home Network](https://docs.vyos.io/en/1.5/configexamples/pppoe-ipv6-basic.html) |
| `vyos.blueprints.router_advert` | IPv6 router advertisements (SLAAC, RDNSS, link MTU) | building block; used by [PPPoE IPv6 Basic Setup for Home Network](https://docs.vyos.io/en/1.5/configexamples/pppoe-ipv6-basic.html) |
| `vyos.blueprints.qos` | QoS shaper policies with classes, DSCP re-marking and interface attachment; any match criteria | [QoS example](https://docs.vyos.io/en/1.5/configexamples/qos.html) |
| `vyos.blueprints.isis` | IS-IS with MPLS segment routing (prefix SIDs, MSD, SRGB/SRLB) and MPLS interfaces | [Segment-routing IS-IS example](https://docs.vyos.io/en/1.5/configexamples/segment-routing-isis.html) |
| `vyos.blueprints.l3vpn` | MPLS L3VPN control plane - iBGP VPNv4 with route reflectors, peer-group, RR clients, next-hop self | [L3VPN for Hub-and-Spoke connectivity with VyOS](https://docs.vyos.io/en/1.5/configexamples/l3vpn-hub-and-spoke.html) |
| `vyos.blueprints.mpls_ldp` | MPLS forwarding and LDP | building block; used by [L3VPN for Hub-and-Spoke connectivity with VyOS](https://docs.vyos.io/en/1.5/configexamples/l3vpn-hub-and-spoke.html) |
| `vyos.blueprints.l2tp_lns` | L2TP network server for PPP sessions from a LAC, RADIUS or local authentication | [PPPoE over L2TP](https://docs.vyos.io/en/1.5/configexamples/lac-lns.html) |
| `vyos.blueprints.dmvpn` | DMVPN - NHRP for hubs and spokes (phase 3), IPsec profile in transport mode, unprotected-GRE drop rule | [DMVPN Dual HUB Dual Cloud](https://docs.vyos.io/en/1.5/configexamples/dmvpn-dualhub-dualcloud.html) |
| `vyos.blueprints.management` | SNMP v2c/v3 and trap targets, remote syslog, NTP, RADIUS login; secrets masked | building block (roadmap: management plane) |
| `vyos.blueprints.backup` | Bulk configuration backups - restorable hierarchical form and set commands, version manifest, retention, optional git commit | operations; `ansible-playbook vyos.blueprints.backup` |
| `vyos.blueprints.upgrade` | Bulk image upgrades - backup, add image, reboot, version check; skips routers already upgraded, one router at a time | operations; `ansible-playbook vyos.blueprints.upgrade` |

Every role has documented, validated inputs (`ansible-doc -t role vyos.blueprints.<role>`)
and a `verify` entry point with operational checks
(`include_role: {name: vyos.blueprints.<role>, tasks_from: verify}`).

### Scope

The roles configure a reachable VyOS router. Provisioning the router itself
(hypervisor, cloud image, cloud-init) and choosing an inventory source are left
to you; [docs/using.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/using.md) shows how the roles fit with static
inventories, containerlab, Netbox and AWX.

Roles use `state: merged`: they add or change what they describe and leave
other configuration alone. Removing settings that were dropped from your
variables is not handled yet, except by `wan_load_balance`, which owns its rules.

## Testing

| Test | Runs | State |
|---|---|---|
| ansible-lint, ansible-test sanity, Galaxy import | every pull request | passing |
| Red Hat certification checks - galaxy-importer, ansible-lint (production profile), ansible-test sanity on ansible-core 2.16, 2.18 and 2.20 | every pull request, and weekly | passing |
| Render tests - every role and blueprint rendered offline against vyos.vyos and compared with the docs page's commands | every pull request | passing |
| Molecule - the roles applied to VyOS 1.5 (VyOS Stream, in containerlab): converge, idempotence, and the blueprint's behaviour checked with traffic | every pull request | **23 of 29 scenarios pass and are required**; 6 run as experimental - see [docs/molecule-status.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/molecule-status.md) |

Until a role's scenario passes, test it in a lab before using it in production, for
example with the render-only preview (see
[docs/using.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/using.md))
and the examples' containerlab topologies. Issues and fixes are welcome.

To run the checks locally, see
[CONTRIBUTING.md](https://github.com/vyos/vyos.blueprints/blob/main/CONTRIBUTING.md); the live upgrade test is described in
[docs/upgrade-testing.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/upgrade-testing.md).

## Upstream findings

[docs/upstream-findings.md](https://github.com/vyos/vyos.blueprints/blob/main/docs/upstream-findings.md) lists the vyos.vyos bugs, missing modules and
options, and docs-page issues found while building these roles, with the workaround used for each.

## Contributing

New blueprints are welcome. See [CONTRIBUTING.md](https://github.com/vyos/vyos.blueprints/blob/main/CONTRIBUTING.md) for the
PR conventions (CLA, `T<id>:` titles, changelog fragments), the role checklist and the test tiers.

## Security

Please report security issues privately - see [SECURITY.md](https://github.com/vyos/vyos.blueprints/blob/main/SECURITY.md).

## Support

The collection is maintained by the VyOS team. Community help is available through
[GitHub issues](https://github.com/vyos/vyos.blueprints/issues), the
[VyOS issue tracker](https://vyos.dev), the [VyOS forum](https://forum.vyos.io/) and the
[Ansible Forum](https://forum.ansible.com/).

If you obtained the collection from Red Hat Automation Hub as certified content, it is
entitled to support through Ansible Automation Platform, using the **Create issue**
button on the collection's page in Automation Hub.

## Release notes and roadmap

Release notes are in [CHANGELOG.rst](https://github.com/vyos/vyos.blueprints/blob/main/CHANGELOG.rst). The collection follows
semantic versioning; the first release is 0.1.0.

Planned: an image-management module in vyos.vyos to replace the CLI dialogue in the
`upgrade` role, a REST API backend for the roles (via rest.vyos), and removal of each
workaround listed in the upstream findings once its fix is released.

## Related information

- [VyOS Configuration Blueprints](https://docs.vyos.io/en/1.5/configexamples/index.html)
- [VyOS documentation](https://docs.vyos.io/en/latest/)
- [vyos.vyos collection](https://github.com/vyos/vyos.vyos)
- [Ansible network automation](https://docs.ansible.com/ansible/latest/network/index.html)
- [Ansible collections overview](https://github.com/ansible-collections/overview)

## License information

GNU General Public License v3.0 or later. See
[LICENSE](https://github.com/vyos/vyos.blueprints/blob/main/LICENSE) for the full text.
