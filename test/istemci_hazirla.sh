#!/usr/bin/env bash
# Lab PC'sini (Pardus/Linux) sunucunun ağına sokar ve istemci kontrolünü çalıştırır.
# Önce mevcut ayarla dener, olmazsa DHCP, o da olmazsa sunucunun ağından sabit IP verir.
# Kullanım (test klasöründe, sudo OLMADAN; gerekirse şifreyi kendisi sorar):
#   bash istemci_hazirla.sh 192.168.50.1          # sunucu IP'si (lab_hazirla.sh sonunda yazar)
#   bash istemci_hazirla.sh 192.168.50.1 8080     # port farklıysa
#   bash istemci_hazirla.sh --geri                # test sonrası okulun ağ ayarına dön
cd "$(dirname "$0")" || exit 1
BAG=lab-istemci

# Öğrenci hesabı ağ ayarını değiştiremiyorsa aynı komutu sudo ile tekrarla.
nm() { nmcli "$@" 2>/dev/null || sudo nmcli "$@"; }
bag_var() { nmcli -t -f NAME connection show | grep -qx "$BAG"; }
kablo_var() { [ "$(cat "/sys/class/net/$1/carrier" 2>/dev/null)" = 1 ]; }
kablolu_arayuzler() { nmcli -t -f DEVICE,TYPE,STATE device | awk -F: '$2 == "ethernet" && $3 != "unmanaged" {print $1}'; }

if [ "$1" = --geri ]; then
  bag_var && nm connection delete "$BAG" >/dev/null && echo "$BAG bağlantısı silindi; okulun ayarı geri geliyor."
  nm radio wifi on
  for a in $(kablolu_arayuzler); do nmcli device connect "$a" >/dev/null 2>&1; done
  exit 0
fi

SUNUCU=${1:?Kullanım: bash istemci_hazirla.sh SUNUCU_IP [PORT]}
PORT=${2:-8080}
erisim() { ping -c1 -W1 "$SUNUCU" >/dev/null 2>&1; }
bekle()  { for _ in $(seq "$1"); do erisim && return 0; sleep 1; done; return 1; }

echo "== Ağ =="
if nmcli -t -f TYPE,STATE device | grep -q '^wifi:connected'; then
  nm radio wifi off && echo "  Wi-Fi kapatıldı (internet oradan gelmesin; --geri ile açılır)."
fi
ARAYUZ=
for a in $(kablolu_arayuzler); do kablo_var "$a" && { ARAYUZ=$a; break; }; done
[ -z "$ARAYUZ" ] && { echo "  [KALDI] Kabloda bağlantı yok; kabloyu ve switch port ışığını kontrol edin."; exit 1; }
echo "  Kablo bağlı: $ARAYUZ"

if bekle 3; then
  echo "  Sunucuya mevcut ayarla erişiliyor."
else
  echo "  Sunucuya erişilemiyor; DHCP deneniyor (20 sn)..."
  bag_var && nm connection delete "$BAG" >/dev/null
  nm connection add type ethernet ifname "$ARAYUZ" con-name "$BAG" ipv4.method auto ipv6.method disabled >/dev/null
  nm connection up "$BAG" >/dev/null 2>&1
  if ! bekle 20; then
    # Sunucunun /24 ağından 100–249 arası bir adres; MAC'e göre başlar. Aynı başlangıcı alan PC'ler olabileceğinden
    # NetworkManager adresi almadan önce ağda soruyor (dad-timeout), kullanılıyorsa bir sonrakine geçiliyor.
    BAS=$(( 16#$(cut -d: -f5,6 "/sys/class/net/$ARAYUZ/address" | tr -d :) ))
    ADRES=
    for i in $(seq 0 149); do
      A=${SUNUCU%.*}.$(( (BAS + i) % 150 + 100 ))
      [ "$A" = "$SUNUCU" ] && continue
      nm connection modify "$BAG" ipv4.method manual ipv4.addresses "$A/24" ipv4.dad-timeout 2000
      nm connection up "$BAG" >/dev/null 2>&1 && { ADRES=$A; break; }
      echo "  $A kullanımda, sonraki deneniyor..."
    done
    [ -z "$ADRES" ] && { echo "  [KALDI] Boş adres bulunamadı:  nmcli connection up $BAG"; exit 1; }
    echo "  DHCP yok; sabit IP verildi: $ADRES/24"
    bekle 10 || { echo "  [KALDI] Sunucuya ($SUNUCU) hâlâ ping gitmiyor. Aynı switch'te mi? Sunucuda lab_hazirla.sh çalıştı mı?"; exit 1; }
  fi
fi
echo "  Bu PC: $(ip -4 -br addr show "$ARAYUZ" | awk '{print $3}')   Sunucu: $SUNUCU"
echo
bash istemci_kontrol.sh "http://$SUNUCU:$PORT"
SONUC=$?
echo
echo "Tarayıcıda açın:  http://$SUNUCU:$PORT   (http:// ile; Firefox'ta proxy kapalı olmalı)"
echo "Test bitince:     bash istemci_hazirla.sh --geri"
exit $SONUC
