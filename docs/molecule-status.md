# Molecule status

Live tests: every scenario applies its roles to VyOS 1.5 (VyOS Stream, in
containerlab), checks idempotence and verifies the blueprint's behaviour with
traffic. The CI matrix runs the passing scenarios as **required** and the others
as **experimental** (they run on every build but do not fail it).

## Required (passing)

base, management, backup, upgrade, edge_nat, ha_vrrp, ha_walkthrough_bgp,
ha_walkthrough_ospf, ospf_unnumbered, bgp_unnumbered, isis_segment_routing,
inter_vrf, zone_firewall, bridge_firewall, gre_tunnel, wan_load_balance, qos,
ipsec_route_based, ipsec_route_based_bgp, ipsec_route_based_bgp_dual,
ipsec_route_based_gcp, ipsec_policy_based, policy_ipsec_firewall.

The IPsec scenarios (and `dmvpn`: hubs before spokes) configure responders before initiators (`converge.yml`): an
initiator that starts IKE before its peer is configured gets NO_PROPOSAL_CHOSEN and
does not retry.

`upgrade` covers the skip and failure paths only (containers cannot boot a new
image); `qos` checks classification and delivery, not DSCP re-marking, which
VyOS 1.5 does not implement (see `upstream-findings.md`, VyOS issues).

## Experimental (being made to pass)

| Scenario | Where it fails | What is known |
|---|---|---|
| `ha_walkthrough` | verify: internal host -> internet through NAT | router1 is VRRP master for `int` and NATs correctly; router2 *also* holds the `public` address (203.0.113.1) - a split brain on VLAN 100 only, over the LACP bond to the lab switch. Next: VRRP state and per-VLAN counters on both routers. |
| `vrf_firewall` | verify: pings across VRFs | converge and idempotence pass; inter-VRF traffic does not flow. Next: post-mortem routes per VRF (`ip route show vrf X`) and the leaking routes. |
| `l3vpn_hub_and_spoke` | verify: CE loopback to CE loopback | BGP (VPNv4 and CE sessions) is up; the MPLS data plane does not forward. Next: label tables (`ip -f mpls route`) and `net.mpls.*` sysctls in the PE containers. |
| `dmvpn` | verify: no Full OSPF adjacency on tun100/tun101 | passed in most runs, but not reliably. With hubs configured before spokes, IPsec is ESTABLISHED/INSTALLED everywhere, yet OSPF over the mGRE tunnels does not reach Full. Next: OSPF and NHRP state, which the post-mortem now records. |
| `pppoe_ipv6` | verify: `pppoe0` not up | PPP modules are loaded; next: the PPPoE server (accel-ppp) and client logs in the post-mortem. |
| `l2tp_lns` | verify: no `ppp0` on the LAC | L2TP modules are loaded (linux-modules-extra); next: xl2tpd/pppd logs on the LAC and accel-ppp on the LNS. |

Each run uploads `molecule-logs-<scenario>` with the containerlab deploy log and a
post-mortem of every node (configuration, routes, qdiscs, BGP, IPsec SAs and logs).
To iterate on a few scenarios without the full pipeline:

    git commit -m "... [skip ci]" && git push
    gh workflow run tests.yml --ref <branch> -f molecule_only=true -f scenarios='["vrf_firewall"]'
