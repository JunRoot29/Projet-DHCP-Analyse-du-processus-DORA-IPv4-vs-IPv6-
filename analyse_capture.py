#!/usr/bin/env python3
from scapy.all import *
import sys

print("ANALYSE CAPTURE DHCPv4 vs DHCPv6")
print("="*50)

if len(sys.argv) < 2:
    print("Usage: python analyse_capture.py <fichier.pcap>")
    sys.exit(1)

file = sys.argv[1]
packets = rdpcap(file)

print(f"Fichier: {file}")
print(f"Nombre total de paquets: {len(packets)}")
print()

# Statistiques IPv4
dhcpv4 = [p for p in packets if p.haslayer(BOOTP)]
print("=== DHCPv4 (DORA) ===")
print(f"Paquets DHCPv4 trouvés: {len(dhcpv4)}")

for i, p in enumerate(dhcpv4[:4], 1):
    if p.haslayer(DHCP):
        options = p[DHCP].options
        for opt in options:
            if isinstance(opt, tuple) and opt[0] == 'message-type':
                msg_type = {1: 'DISCOVER', 2: 'OFFER', 3: 'REQUEST', 5: 'ACK'}.get(opt[1], str(opt[1]))
                src = p[IP].src if p.haslayer(IP) else "N/A"
                dst = p[IP].dst if p.haslayer(IP) else "N/A"
                print(f"  {i}. {msg_type:10} {src:15} -> {dst:15}")

# Statistiques IPv6
dhcpv6 = [p for p in packets if p.haslayer(IPv6) and (p.haslayer(UDP) and p[UDP].dport in [546, 547])]
print(f"\n=== DHCPv6 (SARR) ===")
print(f"Paquets IPv6 sur ports 546/547: {len(dhcpv6)}")

for i, p in enumerate(dhcpv6[:4], 1):
    if p.haslayer(IPv6):
        src = p[IPv6].src
        dst = p[IPv6].dst
        sport = p[UDP].sport if p.haslayer(UDP) else ""
        dport = p[UDP].dport if p.haslayer(UDP) else ""
        print(f"  {i}. Ports {sport}->{dport} | {src:30} -> {dst:30}")

print("\n" + "="*50)
print("COMPARAISON RÉSUMÉE:")
print("DHCPv4 utilise le BROADCAST (255.255.255.255)")
print("DHCPv6 utilise le MULTICAST (ff02::1:2)")
print("="*50)