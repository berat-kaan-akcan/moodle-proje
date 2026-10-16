#!/usr/bin/env bash
# Sunucuyu lab ağına (switch, kablolu) göre hazırlar: IP'yi bulur, Moodle adresini günceller,
# yedek alır, güvenlik duvarını açar, uykuyu engeller ve sunucu kontrollerini çalıştırır.
# Kullanım (sudo OLMADAN; gerektiğinde kendisi sudo ister):
#   bash test/lab_hazirla.sh            # bağlı kablolu arayüzü kendisi bulur
#   bash test/lab_hazirla.sh eno1       # arayüzü elle ver
#   bash test/lab_hazirla.sh --geri     # test sonrası: adresi localhost'a döndür, portu kapat
cd "$(dirname "$0")/.." || exit 1
[ "$(id -u)" -eq 0 ] && { echo "sudo olmadan çalıştırın (.env dosyasının sahibi değişmesin)."; exit 1; }
set -a; . ./.env; set +a
PORT=${MOODLE_PORT:-8080}
LAB_AG=${LAB_AG:-192.168.50.1/24}   # labda DHCP yoksa sunucunun alacağı adres (Docker'ın 172.17/172.18 ağlarını seçmeyin)

kablo_var() { [ "$(cat "/sys/class/net/$1/carrier" 2>/dev/null)" = 1 ]; }
kablolu_arayuzler() { nmcli -t -f DEVICE,TYPE,STATE device | awk -F: '$2 == "ethernet" && $3 != "unmanaged" {print $1}'; }
ipv4() { ip -4 -br addr show "$1" 2>/dev/null | awk '{print $3}' | cut -d/ -f1 | grep -v '^169\.254\.'; }

adres_yaz() {
  sed -i "s|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=$1|" .env
  export MOODLE_WWWROOT=$1   # yukarıda .env'den dışa aktarılan eski değer compose'da .env'in önüne geçmesin
  docker compose up -d
  for _ in $(seq 30); do
    curl -s -m 3 -o /dev/null "http://localhost:$PORT/login/index.php" && break; sleep 2
  done
  docker compose exec -T -u www-data moodle php /var/www/html/admin/cli/purge_caches.php
  # Önbellek boşken aynı anda gelen ilk istekler "Önbelleğe almak için kilit alınamıyor" (404) hatası alıyor;
  # öğrenciler gelmeden kurs önbelleklerini kur ve giriş sayfasını bir kez aç.
  docker compose exec -T -u www-data moodle php -r \
    'define("CLI_SCRIPT", true); require "/var/www/html/config.php"; foreach (get_courses() as $k) { get_fast_modinfo($k); }'
  curl -s -m 60 -o /dev/null -L "http://localhost:$PORT/login/index.php"
}

if [ "$1" = "--geri" ]; then
  ESKI=${MOODLE_WWWROOT#http://}; ESKI=${ESKI%%:*}
  ARAYUZ=$(ip -4 -br addr | awk -v ip="$ESKI/" 'index($3, ip) == 1 {print $1; exit}')
  [ -n "$ARAYUZ" ] && [ "$ARAYUZ" != lo ] && systemctl is-active -q firewalld \
    && sudo firewall-cmd --zone="$(sudo firewall-cmd --get-zone-of-interface="$ARAYUZ")" --remove-port="$PORT/tcp"
  pkill -f "^systemd-inhibit .*Moodle lab" 2>/dev/null
  nmcli connection delete lab >/dev/null 2>&1 && echo "Lab ağ bağlantısı silindi."
  nmcli radio wifi on
  adres_yaz "http://localhost:$PORT"
  echo "Adres http://localhost:$PORT olarak geri alındı."
  exit 0
fi

echo "== 1. Ağ =="
if nmcli -t -f TYPE,STATE device | grep -q '^wifi:connected'; then
  nmcli radio wifi off && echo "  Wi-Fi kapatıldı (sunucu internete oradan çıkmasın; --geri ile açılır)."
fi
ADAY=${1:-$(kablolu_arayuzler)}
ARAYUZ=
for i in $(seq 30); do
  for a in $ADAY; do kablo_var "$a" && { ARAYUZ=$a; break 2; }; done
  [ "$i" = 1 ] && echo "  Kablo bağlantısı bekleniyor (60 sn): kabloyu switch'e takın, port ışığı yanmalı..."
  sleep 2
done
if [ -z "$ARAYUZ" ]; then
  echo "  [KALDI] Kabloda bağlantı yok (NO-CARRIER). Başka port/kablo deneyin; duvar prizi switch'e bağlı olmayabilir."
  for a in $ADAY; do echo "    $a: carrier=$(cat /sys/class/net/$a/carrier 2>/dev/null)"; done
  exit 1
fi
echo "  Kablo bağlı: $ARAYUZ"
IP=$(ipv4 "$ARAYUZ")
if [ -z "$IP" ]; then
  echo "  DHCP bekleniyor (20 sn)..."
  for i in $(seq 10); do IP=$(ipv4 "$ARAYUZ"); [ -n "$IP" ] && break; sleep 2; done
fi
if [ -z "$IP" ]; then
  # Labda DHCP yok: sunucu kendine sabit adres alır ve (dnsmasq varsa) lab PC'lerine IP dağıtır.
  # Wi-Fi kapalı olduğundan NetworkManager'ın paylaşım modu dışarıya internet vermez.
  # Switch okul ağına da bağlıysa DHCP dağıtmamak için: LAB_YONTEM=manual bash test/lab_hazirla.sh
  YONTEM=${LAB_YONTEM:-shared}; command -v dnsmasq >/dev/null || YONTEM=manual
  echo "  Labda DHCP yok; sunucu ${LAB_AG%/*} adresini alıyor (yöntem: $YONTEM)."
  nmcli connection delete lab >/dev/null 2>&1
  nmcli connection add type ethernet ifname "$ARAYUZ" con-name lab autoconnect no \
      ipv4.method "$YONTEM" ipv4.addresses "$LAB_AG" ipv6.method disabled >/dev/null \
    && nmcli connection up lab >/dev/null \
    || { echo "  [KALDI] lab bağlantısı açılamadı:  nmcli connection up lab"; exit 1; }
  IP=${LAB_AG%/*}
  if [ "$YONTEM" = shared ]; then
    echo "  Lab PC'leri DHCP ile ${IP%.*}.x adresi alır; sabit IP'li PC'lerde: bash istemci_hazirla.sh $IP"
  else
    echo "  [UYARI] dnsmasq yok; lab PC'lerinde IP'yi istemci_hazirla.sh verecek: bash istemci_hazirla.sh $IP"
  fi
fi
echo "  Arayüz: $ARAYUZ   IP: $IP"
if ping -c1 -W2 8.8.8.8 >/dev/null 2>&1; then
  echo "  [UYARI] Sunucuda internet VAR. Wi-Fi açıksa kapatın (nmcli radio wifi off)."
  echo "          İnternet kablodan geliyorsa lab PC'lerinde de vardır; istemci kontrolü bunu gösterir."
else
  echo "  Sunucuda internet yok."
fi

echo "== 2. Yedek =="
YEDEK=cikti/yedek-lab-$(date +%F-%H%M).sql.gz
mkdir -p cikti
if docker compose exec -T db mariadb-dump -u "$DB_USER" -p"$DB_PASSWORD" --single-transaction "$DB_NAME" | gzip > "$YEDEK" \
   && [ "$(stat -c %s "$YEDEK")" -gt 100000 ]; then
  echo "  $YEDEK ($(du -h "$YEDEK" | cut -f1))"
else
  echo "  [KALDI] Yedek alınamadı; devam edilmiyor."; exit 1
fi

echo "== 3. Moodle adresi =="
adres_yaz "http://$IP:$PORT"

echo "== 4. Güvenlik duvarı =="
if systemctl is-active -q firewalld; then
  BOLGE=$(sudo firewall-cmd --get-zone-of-interface="$ARAYUZ" 2>/dev/null || sudo firewall-cmd --get-default-zone)
  sudo firewall-cmd --zone="$BOLGE" --add-port="$PORT/tcp" && echo "  $BOLGE bölgesinde $PORT/tcp açıldı (yeniden başlatınca kapanır)."
else
  echo "  firewalld çalışmıyor; atlandı."
fi

echo "== 5. Uyku engeli =="
if pgrep -f "^systemd-inhibit .*Moodle lab" >/dev/null; then
  echo "  Zaten etkin."
else
  setsid systemd-inhibit --what=sleep:idle --why="Moodle lab" sleep 8h >/dev/null 2>&1 &
  echo "  8 saat boyunca uyku/askıya alma engellendi. Fişi takın, kapağı kapatmayın."
fi

echo
bash test/sunucu_kontrol.sh
echo
echo "################################################################"
echo "  Lab PC'lerinde açılacak adres:   http://$IP:$PORT"
echo "  Pardus/Linux lab PC'si (test klasörünü USB ile taşıyın; IP'yi gerekirse kendisi verir):"
echo "    bash istemci_hazirla.sh $IP $PORT"
echo "  Windows lab PC'si:"
echo "    powershell -ExecutionPolicy Bypass -File istemci_kontrol.ps1 http://$IP:$PORT"
echo "  Yük testi:  python3 test/sinav_yuk_testi.py hazirla 40 <cmid>"
echo "              python3 test/sinav_yuk_testi.py calistir"
echo "  Bitince:    python3 test/sinav_yuk_testi.py temizle  &&  bash test/lab_hazirla.sh --geri"
echo "################################################################"
