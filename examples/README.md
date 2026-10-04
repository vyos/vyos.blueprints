# vyos.blueprints examples

Each directory is a complete, runnable Ansible project:

| Example | Roles | Matching docs blueprint |
|---|---|---|
| `single-edge/` | `base`, `edge_nat` | – (small-office internet edge) |
| `ha-pair/` | `base`, `ha_vrrp` | [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |

Every example ships a `topology.clab.yml`, so you can try it against
containerized VyOS before pointing it at real routers:

```bash
sudo containerlab deploy -t topology.clab.yml
ansible-playbook -i inventory.yml site.yml
ansible-playbook -i inventory.yml verify.yml
sudo containerlab destroy -t topology.clab.yml --cleanup
```

To use an example on your own routers, change `ansible_host` and the
credentials in `inventory.yml` (or swap the file for your Netbox / AWX
inventory) and adjust the addresses in `group_vars` / `host_vars`.

Preview the exact commands without touching a device:

```bash
ansible-playbook -i inventory.yml site.yml \
  -e vyos_blueprints_render_only=true -e show_rendered=true
```
