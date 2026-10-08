# Changelog

## 0.1.0 (unreleased)

- Initial roles: `base`, `edge_nat`, `ha_vrrp`.
- New role `ospf_unnumbered` (docs blueprint "OSPF unnumbered with ECMP").
- New role `bgp_unnumbered` (docs blueprint "BGP IPv6 unnumbered with extended nexthop").
- New role `zone_firewall` (docs blueprint "Zone-Policy example").
- New role `vrf_firewall` (docs blueprint "VRF and firewall example").
- New role `bridge_firewall` (docs blueprint "Bridge and firewall example").
- New role `ipsec_route_based` (docs blueprints "Route-based Site-to-Site VPN IPsec between VyOS and Cisco" and "... between VyOS and Palo Alto").
- New role `ipsec_policy_based` (docs blueprint "Policy-based Site-to-Site VPN IPsec between VyOS and Cisco").
- New roles `firewall` and `nat`; `ipsec_policy_based` gains proposal ids, ESP mode, `vpn ipsec interface`, optional peer IKE ids and optional lifetime/PFS/DPD (docs blueprint "Policy-Based Site-to-Site VPN and Firewall Configuration").
- New role `gre_tunnel`; `ipsec_policy_based` gains `vpn ipsec options` (FlexVPN, virtual-ip), per-tunnel protocol and peer virtual-address (docs blueprint "Site-to-Site IPSec VPN to Cisco using FlexVPN").
- `ipsec_route_based` gains BGP over the VTIs, interface routes, VTI description and MSS clamping, IKEv2 re-auth, peer description, ESP group on the VTI, `vpn ipsec interface` and optional lifetime/PFS/DPD/close-action (docs blueprint "Route-Based Site-to-Site VPN to Azure").
- Render-only preview mode (`vyos_blueprints_render_only`).
- Offline render tests and containerlab-based Molecule scenarios.
- `ipsec_route_based`: peers sharing a `psk_name` share one PSK entry with all their ids (docs blueprint "Route-Based Redundant Site-to-Site VPN to Azure").
- `ipsec_route_based`: IKE PRF, BGP prefix-lists and route-maps with per-neighbour import/export (docs blueprint "Route-Based Site-to-Site VPN to Google Cloud HA VPN").
- New role `bonding`; `base` gains static routes; `ha_vrrp` conntrack-sync gains event-listen-queue-size and disabling conntrack helpers (docs blueprint "High Availability Walkthrough", part 1).
- New roles `wireguard`, `route_policy` and `ospf` (docs blueprint "High Availability Walkthrough", part 2).
- New role `bgp`; `route_policy` sets route-map descriptions (docs blueprint "High Availability Walkthrough", part 3).
- New role `vrf_lite`; `route_policy` gains IPv6 prefix-lists and route-map IPv6 matches (docs blueprint "Inter-VRF Routing over VRF Lite").
- New role `wan_load_balance`, the first role that removes settings it owns (load-balancing rules) when they leave the inputs (docs blueprint "WAN Load Balancer examples").
- New roles `pppoe` and `router_advert`; `firewall` gains named rulesets (docs blueprint "PPPoE IPv6 Basic Setup for Home Network").
- New role `qos` (docs blueprint "QoS example").
- New role `isis` (docs blueprint "Segment-routing IS-IS example").
- New roles `mpls_ldp` and `l3vpn`; `vrf_lite` gains `label vpn export`, VRF networks and CE `as-override`; `bgp` gains log-neighbor-changes (docs blueprint "L3VPN for Hub-and-Spoke connectivity with VyOS").
- New role `l2tp_lns` (docs blueprint "PPPoE over L2TP"); its Molecule scenario is experimental.
- New role `dmvpn`; `gre_tunnel` gains GRE key and enable-multicast; `ospf` gains interface area, `passive disable`, `passive-interface default` and an optional router-id (docs blueprint "DMVPN Dual HUB Dual Cloud").
- New role `management`: SNMP (communities, v3, trap targets), remote syslog, NTP and RADIUS login; secrets are masked in rendered output.
- New role `backup` and collection playbook `vyos.blueprints.backup` for bulk configuration backups.
