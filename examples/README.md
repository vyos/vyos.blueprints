# vyos.blueprints examples

Each directory is a complete, runnable Ansible project:

| Example | Roles | Matching docs blueprint |
|---|---|---|
| `single-edge/` | `base`, `edge_nat` | – (small-office internet edge) |
| `ha-pair/` | `base`, `ha_vrrp` | [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) |
| `ospf-unnumbered/` | `base`, `ospf_unnumbered` | [OSPF unnumbered with ECMP](https://docs.vyos.io/en/1.5/configexamples/ospf-unnumbered.html) |
| `bgp-unnumbered/` | `bgp_unnumbered` | [BGP IPv6 unnumbered with extended nexthop](https://docs.vyos.io/en/1.5/configexamples/bgp-ipv6-unnumbered.html) |
| `zone-policy/` | `base`, `zone_firewall` | [Zone-Policy example](https://docs.vyos.io/en/1.5/configexamples/zone-policy.html) |
| `vrf-firewall/` | `base`, `vrf_firewall` | [VRF and firewall example](https://docs.vyos.io/en/1.5/configexamples/fwall-and-vrf.html) |
| `bridge-firewall/` | `base`, `bridge_firewall` | [Bridge and firewall example](https://docs.vyos.io/en/1.5/configexamples/fwall-and-bridge.html) |
| `ipsec-route-based/` | `base`, `ipsec_route_based` | [Route-based ... VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-route-based.html); for [Route-based ... VyOS and Palo Alto](https://docs.vyos.io/en/1.5/configexamples/ipsec-pa-route-based.html) rename the peer `CISCO` to `PA` - the VyOS side is otherwise identical |
| `ipsec-policy-based/` | `base`, `ipsec_policy_based` | [Policy-based Site-to-Site VPN IPsec between VyOS and Cisco](https://docs.vyos.io/en/1.5/configexamples/ipsec-cisco-policy-based.html) |
| `policy-ipsec-firewall/` | `base`, `ipsec_policy_based`, `firewall`, `nat` | [Policy-Based Site-to-Site VPN and Firewall Configuration](https://docs.vyos.io/en/1.5/configexamples/policy-based-ipsec-and-firewall.html) |
| `flexvpn-cisco/` | `gre_tunnel`, `ipsec_policy_based` | [Site-to-Site IPSec VPN to Cisco using FlexVPN](https://docs.vyos.io/en/1.5/configexamples/site-2-site-cisco.html) (no containerlab topology: needs a Cisco FlexVPN hub) |
| `azure-vpn-bgp/` | `ipsec_route_based` | [Route-Based Site-to-Site VPN to Azure (BGP over IKEv2/IPsec)](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-bgp.html) (no containerlab topology: the far end is Azure) |
| `azure-vpn-dual-bgp/` | `ipsec_route_based` | [Route-Based Redundant Site-to-Site VPN to Azure (BGP over IKEv2/IPsec)](https://docs.vyos.io/en/1.5/configexamples/azure-vpn-dual-bgp.html) (no containerlab topology: the far end is Azure) |

Most examples ship a `topology.clab.yml`, so you can try them against
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
