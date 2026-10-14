# Upstream findings

Bugs, missing modules and missing options found while implementing the VyOS
1.5 Configuration Blueprints with vyos.vyos 6.1.0, plus issues in the docs
pages themselves. Every item is worked around in this collection; the
"Workaround" column says where, so the workaround can be removed once the item
is fixed upstream.

## 1. vyos.vyos bugs

| # | Module | Bug | Impact | Found on | Workaround |
|---|---|---|---|---|---|
| B1 | **vyos_bgp_global** | In `rm_templates/bgp_global.py` the `bgp_params.no_client_to_client_reflection` entry has `compval: bgp_params.log_neighbor_changes` (copied from the entry above). Setting `log_neighbor_changes` also renders `no-client-to-client-reflection`. | **Severe** - on a route reflector, reflection between clients silently stops; PEs never learn each other's VPN routes. | L3VPN hub-and-spoke | `l3vpn`, `bgp`: `log-neighbor-changes` via vyos_config |
| B2 | **vyos_vrf** | With `state: merged`, `bind_to_all` omitted or `false` renders `delete vrf bind-to-all`. A merge must not delete. | Removes an existing `bind-to-all` on apply. | VRF and firewall, Inter-VRF, L3VPN | `vrf_firewall`, `vrf_lite`: value always passed explicitly (documented) |
| B3 | all version-gated modules (13) | `get_os_version()` opens a device connection even for `state: rendered`/`parsed`; also an `UnboundLocalError` when no device info is returned. | Offline rendering/parsing impossible for ntp_global, logging_global, ha, firewall_global, firewall_rules, ospfv2, ospfv3, ospf_interfaces, bgp_global, bgp_address_family, route_maps, static_routes, vrf. | Scaffold (render tests) | Render tests use a test-only connection (`tests/render/collections`) that reports the version; no patch needed |
| B4 | vyos_vpn_ipsec | `ike_group.proposal.prf` is in the argspec but has no template - silently dropped. | IKE PRF never configured. | Google Cloud HA VPN | `ipsec_route_based`: PRF via vyos_config |
| B5 | vyos_snmp_server | The trap-target template checks `authorization_type`/`client`/`network` (copied from communities) instead of `community`/`port`. | Trap-target community and port silently dropped. | management role (SNMP) | `management`: v2c trap targets via vyos_config |
| B6 | vyos_snmp_server | SNMPv3 trap-target `port` renders `service snmp v3 trap-target port X` without the address. | Invalid command. | management role (SNMP) | - (avoid v3 trap-target port) |
| B7 | vyos_bgp_global | Neighbours with `peer_group: true` (peer-group definitions) render nothing. | Peer-groups silently missing. | BGP IPv6 unnumbered, L3VPN | `bgp_unnumbered`, `l3vpn`: vyos_config |
| B8 | vyos_bgp_address_family | `default_originate` is typed as a string (route-map name); a plain `default-originate` renders `default-originate route-map {}`. | Bare default-originate impossible. | Inter-VRF (ISP side) | Lab ISP via vyos_config |
| B9 | vyos_ospf_interfaces | `passive: false` renders nothing instead of `passive disable`. | Interfaces cannot be exempted from `passive-interface default`. | DMVPN | `ospf`: `passive disable` via vyos_config |
| B10 | vyos_firewall_global | ~~Zones render `member interface <if>`; the 1.5 zone docs use `interface <if>`.~~ **Resolved: not a bug.** VyOS 1.5 reads zone members from `member interface` (vyos-1x `op_mode/zone.py`), as the module renders, and live commits accept it. | - | Zone-Policy | - (the docs page's `interface` form is outdated) |
| B11 | (deprecations) | `ansible.module_utils._text`, `_collections_compat` (removed in ansible-core 2.24), `exit_json(warnings=)` (removed in 2.23). | Modules break on upcoming ansible-core. | All (CI log) | - |
| B12 | vyos_bgp_global | `bgp_params.default.no_ipv4_unicast` renders `protocols bgp parameters default no-ipv4-unicast`, a path VyOS 1.5 no longer has (it always configures FRR with `no bgp default ipv4-unicast`). | Commit fails: `Configuration path … is not valid`. | BGP IPv6 unnumbered (live Molecule run) | `bgp_unnumbered`: option dropped |

## 2. Missing vyos.vyos modules

Areas with no resource module at all; the listed role configures them with
vyos.vyos.vyos_config.

| Missing module | CLI tree | Role(s) |
|---|---|---|
| IS-IS (incl. segment routing) | `protocols isis` | `isis` |
| MPLS / LDP | `protocols mpls` | `isis`, `mpls_ldp` |
| WAN load balancing | `load-balancing wan` | `wan_load_balance` |
| QoS | `qos` | `qos` |
| WireGuard interfaces | `interfaces wireguard` | `wireguard` |
| PPPoE client interfaces | `interfaces pppoe` | `pppoe` |
| L2TP server (LNS / remote-access) | `vpn l2tp remote-access` | `l2tp_lns` |
| NHRP | `protocols nhrp` | `dmvpn` |
| Router advertisements | `service router-advert` | `router_advert` |
| Bridge interfaces | `interfaces bridge` | `bridge_firewall` |
| Conntrack-sync | `service conntrack-sync` | `ha_vrrp` |
| Access-lists | `policy access-list` | `route_policy` |
| RADIUS login | `system login radius` | `management` |
| Protocol route-maps (zebra) | `system ip protocol <proto> route-map` | `ospf` |
| PPPoE server (lab only) | `service pppoe-server` | Molecule scaffolding |

## 3. Missing options in existing modules

| Module | Missing | Role(s) working around it |
|---|---|---|
| vyos_interfaces | VRF on VLAN (vif) interfaces | `vrf_firewall`, `vrf_lite` |
| vyos_interfaces | Tunnel `encapsulation`, `remote`, `source-address`/`source-interface`, `parameters ip key`, `enable-multicast` | `gre_tunnel` |
| vyos_interfaces | `ip adjust-mss` (VTI, tunnel) | `ipsec_route_based`, `gre_tunnel` |
| vyos_vrf | Static route next hop in another VRF (`interface X vrf Y`, route leaking) | `vrf_firewall` |
| vyos_vrf | VRF BGP address families - `rd`, `route-target`, `import/export vpn`, `label vpn export`, `network`, `redistribute`, `route-map vpn import` | `vrf_lite` |
| vyos_vrf | VRF BGP neighbour address-family options (`as-override`, activation) | `vrf_lite` |
| vyos_vrf | VRF BGP without a per-VRF `system-as` (requires `as_number`, renders it) | - (harmless extra) |
| vyos_bgp_global | `neighbor <if> interface v6only` (unnumbered) | `bgp_unnumbered` |
| vyos_bgp_global | `remote-as external`/`internal` (integer only) | `bgp_unnumbered` |
| vyos_bgp_global | `bestpath as-path multipath-relax` | `bgp_unnumbered` |
| vyos_bgp_global / _address_family | Neighbour `ipv4-vpn` options (`route-reflector-client`, `nexthop-self`) | `l3vpn` |
| vyos_ospfv2 | Access-list export filter (`access-list N export <type>`) | `ospf` |
| vyos_ospfv2 | Bare `log-adjacency-changes` (only `detail`) | `ospf` |
| vyos_ospf_interfaces | Interface `area` | `ospf` |
| vyos_route_maps | Route-map `description` | `route_policy` |
| vyos_snmp_server | More than one SNMPv2c trap target | `management` |
| vyos_firewall_rules | Bridge firewall (`afi: bridge`, `ethernet-type`, MAC matches) | `bridge_firewall` |
| vyos_firewall_global | Interface groups | `bridge_firewall` |

## 4. Issues in the docs pages (vyos-documentation, 1.5)

| Page | Issue |
|---|---|
| OSPF unnumbered with ECMP | Per-interface OSPF uses 1.3 syntax (`interfaces ethernet X ip ospf ...`); 1.4+ is `protocols ospf interface X ...`. |
| Zone-Policy example | Pre-1.4 syntax (`firewall name`/`ipv6-name`, `zone-policy`); NTP (123) and DHCP (67,68) listed as tcp. |
| VRF and firewall example | Text says "WAN: allow connection to PROD", but the configuration has no such rule. |
| High Availability Walkthrough | `set interfaces ethernet bond0 ...` (should be `interfaces bonding`); `accept-protocol 'tcp,udp,icmp'` as one value; WireGuard in pre-1.4 syntax (`pubkey`, `endpoint 'ip:port'`); "Enable OSPF" shows one router-id (10.254.60.2) for all routers; router2's BGP only "identical but BGPPREPENDOUT". |
| Policy-Based Site-to-Site VPN and Firewall | RIGHT has no default route towards LEFT. |
| Route-Based VPN to Azure | Does not set `disable-route-autoinstall` (route-based VPNs usually need it). |
| PPPoE IPv6 Basic Setup | `state established 'enable'` is pre-1.4 syntax. |
| QoS example | Text says VyOS2 re-marks "CS4 -> CS6", configuration sets CS5; class 20 shown as `show` output only. |
| Inter-VRF Routing over VRF Lite | Bare `set protocols bgp address-family ipv4-unicast` (no effect). |
| BGP IPv6 unnumbered with extended nexthop | `set protocols bgp parameters default no-ipv4-unicast` no longer exists in 1.5 (VyOS always applies it) and is rejected. |
| Route-Based Site-to-Site VPN to Azure (BGP), and the redundant variant | Peers are named by IP address (`site-to-site peer 51.105.0.2`); VyOS 1.5 requires names of letters, digits, hyphens and underscores. |
| DMVPN Dual HUB Dual Cloud | Spoke-3's tunnel-interface block is missing (only its NHRP block is shown). |

## 5. VyOS issues

| Area | Issue | Seen in | Workaround |
|---|---|---|---|
| Bonding (vyos-1x `interfaces_bonding.py`) | A bond member whose `interfaces ethernet ethX` node exists but is empty is rejected with `it has a "" assigned!`: the empty node yields an empty option path, which is not in the allowed list. On hardware the node holds `hw-id`, so it mainly shows up in containers. | `ha_walkthrough` Molecule scenario | the scenario sets a `description` (an allowed option) on members before bonding |

## 6. Test environment notes

GitHub's hosted runners (Azure kernel) ship `vrf`, `mpls_*` and `l2tp_*` only in
`linux-modules-extra-<kernel>`, which the Molecule job installs before loading modules.

Molecule scenarios that depend on host kernel features (may need a VM-based
runner): `ipsec_*`, `ha_walkthrough` (LACP bonding), `ha_walkthrough_ospf`
(WireGuard), `isis_segment_routing` and `l3vpn_hub_and_spoke` (MPLS),
`pppoe_ipv6` and `l2tp_lns` (PPP, L2TP; `l2tp_lns` is experimental), `dmvpn`
(GRE, NHRP, xfrm).
