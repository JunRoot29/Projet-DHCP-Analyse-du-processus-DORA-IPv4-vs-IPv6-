# Projet-DHCP-Analyse-du-processus-DORA-IPv4-vs-IPv6-
Analyser le processus DORA (Discover-Offer-Request-ACK) du protocole DHCP en comparant la norme et l'implémentation réelle via captures Wireshark.

## 📁 Structure du projet (Tout-en-un)

```
simulation/
├── lab.conf
├── client.startup
├── server.startup
├── lancer_simulation.bat
├── captures/
│   ├── dhcpv4.pcap
│   └── dhcpv6.pcap
└── README.md
```

---

## ⚙️ Fichiers de configuration

### `lab.conf`
```bash
client[0]=lan4
server[0]=lan4
lan4[subnet]=10.0.0.0/24
server[ip]=10.0.0.1

client[1]=lan6
server[1]=lan6
lan6[subnet]=2001:db8:1::/64
server[ipv6]=2001:db8:1::1/64
```

### `client.startup`
```bash
#!/bin/bash
apt update
apt install -y isc-dhcp-client isc-dhcp-client-ddns tcpdump iproute2
ip link set eth0 up
ip link set eth1 up
sysctl -w net.ipv6.conf.eth1.accept_ra=2
```

### `server.startup`
```bash
#!/bin/bash
apt update
apt install -y isc-dhcp-server radvd tcpdump iproute2

# DHCPv4
echo 'INTERFACESv4="eth0"' > /etc/default/isc-dhcp-server
cat << EOF > /etc/dhcp/dhcpd.conf
subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.100 10.0.0.200;
  option routers 10.0.0.1;
}
EOF

# DHCPv6
echo 'INTERFACESv6="eth1"' >> /etc/default/isc-dhcp-server
cat << EOF > /etc/dhcp/dhcpd6.conf
subnet6 2001:db8:1::/64 {
  range6 2001:db8:1::100 2001:db8:1::200;
}
EOF

# RADVD
cat << EOF > /etc/radvd.conf
interface eth1 {
  AdvSendAdvert on;
  prefix 2001:db8:1::/64 { AdvAutonomous on; };
};
EOF

service radvd restart
service isc-dhcp-server restart
```

### `lancer_simulation.bat`
```batch
@echo off
cd /d "%~dp0"
kathara wipe
kathara lstart -d .
kathara exec client -- mkdir -p /shared/captures
start "IPv4" cmd /c "kathara exec client -- tcpdump -i eth0 -w /shared/captures/dhcpv4.pcap -v"
start "IPv6" cmd /c "kathara exec client -- tcpdump -i eth1 -w /shared/captures/dhcpv6.pcap -v"
timeout /t 5
kathara exec client -- dhclient -v eth0
kathara exec client -- dhclient -6 -v eth1
pause
```

---

## 📊 Tableau comparatif DORA

| Étape | Message IPv4 | Destination IPv4 | Message IPv6 | Destination IPv6 |
|-------|-------------|------------------|--------------|------------------|
| D/S   | DISCOVER    | 255.255.255.255 (broadcast) | SOLICIT | ff02::1:2 (multicast) |
| O/A   | OFFER       | À observer | ADVERTISE | Unicast (client) |
| R     | REQUEST     | 255.255.255.255 (broadcast) | REQUEST | ff02::1:2 (multicast) |
| A/R   | ACK         | À observer | REPLY | Unicast (client) |

---

## 🖼️ Captures Wireshark

**Filtres à utiliser :**
- IPv4 : `bootp` ou `dhcp`
- IPv6 : `dhcpv6`

**À annoter sur chaque capture :**
- Adresse MAC destination
- Adresse IP destination
- Port source/destination
- Type de diffusion (broadcast/multicast/unicast)

---

## ✅ Rendu attendu

1. Fichiers `.pcap` des captures
2. 4+ screenshots Wireshark annotés
3. Tableau comparatif complété
4. Analyse concise (5-10 lignes)

---

## 🚀 Lancement

```
1. Double-cliquer sur lancer_simulation.bat
2. Attendre 30 secondes
3. Récupérer les captures dans /shared/captures/
```

---

**Bon TP !** 🖥️🔍
