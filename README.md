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
