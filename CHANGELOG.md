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
