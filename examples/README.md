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
| `gcp-ha-vpn-bgp/` | `ipsec_route_based` | [Route-Based Site-to-Site VPN to Google Cloud HA VPN](https://docs.vyos.io/en/1.5/configexamples/gcp-ha-vpn-bgp.html) (no containerlab topology: the far end is Google Cloud) |
| `ha-walkthrough/` | `bonding`, `base`, `ha_vrrp`, `nat`, `wireguard`, `route_policy`, `ospf`, `bgp` | [High Availability Walkthrough](https://docs.vyos.io/en/1.5/configexamples/ha.html) - the complete page |
| `inter-vrf/` | `base`, `route_policy`, `vrf_lite` | [Inter-VRF Routing over VRF Lite](https://docs.vyos.io/en/1.5/configexamples/inter-vrf-routing-vrf-lite.html) (run `isp.yml` for the lab ISP) |
| `wan-load-balancing/` | `base`, `wan_load_balance` | [WAN Load Balancer examples](https://docs.vyos.io/en/1.5/configexamples/wan-load-balancing.html) - example 1 by default, `-e @variants/exampleN.yml` for examples 2-5 |
| `pppoe-ipv6-home/` | `pppoe`, `router_advert`, `firewall` | [PPPoE IPv6 Basic Setup for Home Network](https://docs.vyos.io/en/1.5/configexamples/pppoe-ipv6-basic.html) (run `isp.yml` for the lab ISP) |
| `qos/` | `base`, `qos` | [QoS example](https://docs.vyos.io/en/1.5/configexamples/qos.html) |
| `isis-segment-routing/` | `base`, `isis` | [Segment-routing IS-IS example](https://docs.vyos.io/en/1.5/configexamples/segment-routing-isis.html) (P3 is a VyOS stand-in for the XRv in the lab) |
| `l3vpn-hub-and-spoke/` | `base`, `ospf`, `mpls_ldp`, `l3vpn`, `vrf_lite`, `bgp` | [L3VPN for Hub-and-Spoke connectivity with VyOS](https://docs.vyos.io/en/1.5/configexamples/l3vpn-hub-and-spoke.html) (all 12 routers; reduced lab in the Molecule scenario) |
| `l2tp-lns/` | `base`, `nat`, `l2tp_lns` | [PPPoE over L2TP](https://docs.vyos.io/en/1.5/configexamples/lac-lns.html) (the lab topology stands in for the Cisco LAC and adds FreeRADIUS) |
| `dmvpn-dual-hub/` | `base`, `gre_tunnel`, `dmvpn`, `ospf` | [DMVPN Dual HUB Dual Cloud](https://docs.vyos.io/en/1.5/configexamples/dmvpn-dualhub-dualcloud.html) (VyOS hubs and spokes) |
| `management/` | `base`, `management` | management plane - SNMP, traps, syslog, NTP, RADIUS login |

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
