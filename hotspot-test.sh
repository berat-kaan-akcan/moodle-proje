#!/bin/bash
# Kullanım: sudo bash ~/moodle-proje/hotspot-test.sh
# Hotspot'u açar, 180 sn boyunca gelen istekleri kaydeder, sonucu hotspot-log.txt'e yazar.
cd /home/berat/moodle-proje || exit 1
LOG=/home/berat/moodle-proje/hotspot-log.txt
exec > >(tee "$LOG") 2>&1

echo "== $(date) =="
nmcli device wifi hotspot ifname wlan0 ssid MOODLE-TEST password test12345
sleep 3
echo "== wlan0 IP =="; ip -4 -br addr show wlan0

sed -i 's|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://10.42.0.1:8080|' .env
grep WWWROOT .env
docker compose up -d
sleep 5

echo "== firewall =="
firewall-cmd --get-zone-of-interface=wlan0
firewall-cmd --zone=public --list-all

echo "== laptop kendi testi =="
curl -m 10 -s -o /dev/null -w "8080 -> %{http_code}\n" http://10.42.0.1:8080

# wlan0'a gelen paketleri en başta say (firewall'dan önce)
nft delete table inet dbg 2>/dev/null
nft add table inet dbg
nft add chain inet dbg pre '{ type filter hook prerouting priority -400; }'
nft add rule inet dbg pre iifname wlan0 icmp type echo-request counter
nft add rule inet dbg pre iifname wlan0 tcp dport 8080 counter
nft add rule inet dbg pre iifname wlan0 tcp dport 8091 counter

# Docker'dan bağımsız basit test sunucusu (8091 firewall'da açık)
python3 -m http.server 8091 --bind 10.42.0.1 --directory /tmp > /tmp/py8091.log 2>&1 &
PY=$!

echo
echo "################################################################"
echo "  Arkadaşın MOODLE-TEST'e bağlansın, MOBİL VERİYİ KAPATSIN,"
echo "  PC ise once komut satirinda:  ping 10.42.0.1"
echo "  ve (Windows PowerShell):  Test-NetConnection 10.42.0.1 -Port 8080"
echo "  sonra tarayıcıda sırayla açsın:"
echo "     http://10.42.0.1:8091"
echo "     http://10.42.0.1:8080"
echo "  180 saniye bekleniyor..."
echo "################################################################"
sleep 180

kill $PY
echo "== wlan0'a ulasan paket sayilari (ping / 8080 / 8091) =="
nft list table inet dbg
nft delete table inet dbg
echo "== 8091 test sunucusuna gelen istekler =="; cat /tmp/py8091.log
echo "== moodle loglari (son 5 dk, dis istekler) =="
docker compose logs --since 5m moodle 2>&1 | grep -v '127.0.0.1' | tail -30
echo "== bagli cihazlar =="; ip neigh show dev wlan0
echo "== nft (8080/drop/reject) =="
nft list ruleset | grep -n -i -E '8080|8091|nm-shared|drop|reject' | head -80
echo "== bitti. Log: $LOG =="
