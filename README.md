# vyos.blueprints

Ansible roles that deploy the [VyOS Configuration Blueprints](https://docs.vyos.io/en/1.5/configexamples/index.html)
on top of the [vyos.vyos](https://github.com/vyos/vyos.vyos) resource modules.
Each role turns one blueprint (or one building block shared by several) into a
validated, idempotent, testable unit.

## Roles

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
| `vyos.blueprints.ipsec_route_based` | Route-based site-to-site IPsec over VTI (IKEv1/IKEv2, PSK), optional OSPF or BGP inside the tunnel | [Route-based ... VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-route-based.html), [Route-based ... VyOS and Palo Alto](https://docs.vyos.io/en/1.5/configexamples/ipsec-pa-route-based.html), [Route-Based ... to Azure (BGP)](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-bgp.html), [Route-Based Redundant ... to Azure](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-dual-bgp.html) |
| `vyos.blueprints.ipsec_policy_based` | Policy-based site-to-site IPsec with traffic selectors (IKEv1/IKEv2, PSK) | [Policy-based Site-to-Site VPN IPsec between VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-policy-based.html) |
| `vyos.blueprints.firewall` | Firewall network/address/port groups, IPv4/IPv6 input, forward and output filters | building block; used by [Policy-Based Site-to-Site VPN and Firewall Configuration](https://docs.vyos.io/en/1.5/configexamples/policy-based-ipsec-and-firewall.html) |
| `vyos.blueprints.nat` | Source NAT (masquerade, SNAT, exclusions) and destination NAT | building block; used by [Policy-Based Site-to-Site VPN and Firewall Configuration](https://docs.vyos.io/en/1.5/configexamples/policy-based-ipsec-and-firewall.html) |
| `vyos.blueprints.gre_tunnel` | GRE and other tunnel interfaces (endpoints, MTU, MSS clamping, addresses) | building block; used by [Site-to-Site IPSec VPN to Cisco using FlexVPN](https://docs.vyos.io/en/1.5/configexamples/site-2-site-cisco.html) |

Every role has documented, validated inputs (`ansible-doc -t role vyos.blueprints.<role>`)
and a `verify` entry point with operational checks
(`include_role: {name: vyos.blueprints.<role>, tasks_from: verify}`).

## Quick start

```bash
ansible-galaxy collection install vyos.blueprints
ansible-playbook vyos.blueprints.install_examples   # copies runnable examples to ./vyos-blueprints-examples
```

```yaml
# site.yml
- hosts: ha_pair
  gather_facts: false
  roles:
    - vyos.blueprints.base
    - vyos.blueprints.ha_vrrp
```

See [docs/using.md](docs/using.md) for the inventory contract, multi-node
conventions and the render-only preview mode.

## Requirements

- ansible-core 2.16+
- vyos.vyos 6.0.0+ (installed automatically)
- VyOS 1.4 or 1.5, reachable over SSH (`ansible.netcommon.network_cli`)

## Scope

The roles configure a reachable VyOS router. Provisioning the router itself
(hypervisor, cloud image, cloud-init) and choosing an inventory source are left
to you; [docs/using.md](docs/using.md) shows how the roles fit with static
inventories, containerlab, Netbox and AWX.

Roles use `state: merged`: they add or change what they describe and leave
other configuration alone. Removing settings that were dropped from your
variables is not handled yet.

## Contributing

New blueprints are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
role checklist and the test tiers.

## License

GPL-3.0-or-later
