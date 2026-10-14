# Using vyos.blueprints

## What the roles need from you

A role touches your environment in three places only:

1. **Connection variables** for each router:

   ```yaml
   ansible_network_os: vyos.vyos.vyos
   ansible_connection: ansible.netcommon.network_cli
   ansible_user: vyos
   ansible_password: "{{ vault_vyos_password }}" # or ansible_ssh_private_key_file
   ```

2. **Role inputs** – the variables listed by `ansible-doc -t role vyos.blueprints.<role>`.
   They are validated when the role starts, so typos and missing values fail
   early with a clear message.

3. **Pair or group membership** – only for multi-node blueprints (see below).

Nothing else is assumed: not how the router was deployed, not where your
inventory comes from, not your directory layout.

## Where the variables come from

The same playbook works with any inventory source; only the place where you
keep the variables changes.

| Setup               | Inventory                                                                                                        | Role inputs                                                               |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Single router / lab | static `inventory.yml`                                                                                           | `group_vars/` and `host_vars/`                                            |
| Trying things out   | containerlab (`topology.clab.yml` in each example; clab also writes an Ansible inventory into the lab directory) | example `group_vars/`                                                     |
| Netbox              | `netbox.netbox.nb_inventory`                                                                                     | Netbox config contexts, or `group_vars/` keyed on Netbox-generated groups |
| AWX / AAP           | any of the above as an inventory source                                                                          | same; build an execution environment containing `vyos.blueprints`         |

## Multi-node blueprints

Blueprints such as HA need to know which routers belong together.

- Put the members of one pair in their **own inventory group** and pass its
  name, e.g. `ha_vrrp_pair_group: ha_pair`.
- Keep **shared** settings (VRRP groups, sync-group) in that group's
  `group_vars`, and **per-node** settings (priority, the node's own
  addresses) in `host_vars`.
- Peer addresses are derived from the other member's `host_vars`. If the peer
  is not in your inventory, or you prefer to be explicit, set
  `ha_vrrp_peer_addresses` instead – explicit values always win.

Run multi-node plays against all members together (`hosts: ha_pair`) so the
cross-node checks in `verify` can compare them.

## Preview without touching devices

```bash
ansible-playbook -i inventory.yml site.yml -e vyos_blueprints_render_only=true
```

Each role then uses the modules' `rendered` state and appends the commands it
would send to the `vyos_blueprints_rendered` fact, which you can print or save
for review. The rendering assumes VyOS 1.5 syntax; set
`VYOS_OFFLINE_OS_VERSION=1.4` in the environment to render for 1.4.

> Some vyos.vyos modules currently need a device connection even when
> rendering. Until that is fixed upstream, render-only mode needs vyos.vyos
> from git `main`.

## Checking a deployment

```yaml
- hosts: ha_pair
  gather_facts: false
  tasks:
    - ansible.builtin.include_role:
        name: vyos.blueprints.ha_vrrp
        tasks_from: verify
```

## Layering

```
day-0 provisioning      (not part of this collection: hypervisor, cloud, cloud-init)
        │  reachable VyOS with SSH
        ▼
inventory + variables   (yours: static, containerlab, Netbox, AWX)
        │
        ▼
vyos.blueprints roles   base → edge_nat / ha_vrrp / ...
        │
        ▼
vyos.vyos resource modules → VyOS
        │
        ▼
verify                  (operational checks per role)
```
