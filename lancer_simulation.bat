@echo off
echo ========================================
echo    SIMULATION DHCPv4 & DHCPv6 COMPLETE
echo ========================================
cd C:\Users\Junio\Desktop\tp_kathara\simulation

echo 1. Nettoyage...
echo y | kathara wipe

echo 2. Démarrage du lab...
kathara lstart

echo 3. Attente génération des paquets (30s)...
timeout /t 30 /nobreak

echo 4. Récupération de la capture...
mkdir ..\rapport\captures_pcap 2>nul
kathara copy client /shared/dhcp_complet.pcap ..\rapport\captures_pcap\

echo 5. Arrêt du lab...
kathara wipe

echo.
echo ========================================
echo       CAPTURE COMPLÈTE RÉUSSIE !
echo ========================================
echo.
echo Fichier: C:\Users\Junio\Desktop\tp_kathara\rapport\captures_pcap\dhcp_complet.pcap
echo.
echo Ouvrez avec Wireshark et utilisez:
echo   - Filtre IPv4: bootp || dhcp
echo   - Filtre IPv6: dhcpv6 || ipv6
echo.
echo Appuyez sur une touche pour ouvrir Wireshark...
pause
start wireshark "C:\Users\Junio\Desktop\tp_kathara\rapport\captures_pcap\dhcp_complet.pcap"