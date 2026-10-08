#!/usr/bin/env bash
# İstemci (PC-2, Linux) kontrolleri. Kullanım: bash test/istemci_kontrol.sh http://10.42.0.1:8080
URL=${1:?Kullanım: bash test/istemci_kontrol.sh http://SUNUCU_IP:8080}
HOST=${URL#http://}; IP=${HOST%%:*}
GEC=0; KAL=0
ok()  { echo "  [GEÇTİ] $1"; GEC=$((GEC+1)); }
bad() { echo "  [KALDI] $1"; KAL=$((KAL+1)); }
chk() { if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

echo "== Kanıt A: istemcide internet YOK olmalı =="
chk "8.8.8.8'e ping gitmiyor"        "! ping -c2 -W2 8.8.8.8"
chk "DNS çözümlenmiyor (google.com)" "! getent hosts google.com"
chk "google.com'a HTTPS açılmıyor"   "! curl -s -m 5 -o /dev/null https://www.google.com"
chk "1.1.1.1'e HTTPS açılmıyor"      "! curl -s -m 5 -o /dev/null https://1.1.1.1"

echo "== Kanıt B: sunucuya erişim VAR olmalı =="
chk "sunucuya ping gidiyor ($IP)"    "ping -c2 -W2 $IP"
CODE=$(curl -s -m 10 -o /dev/null -w '%{http_code}' "$URL/login/index.php")
chk "giriş sayfası yanıt veriyor (HTTP $CODE)" "[ \"$CODE\" = 200 ] || [ \"$CODE\" = 303 ]"
LOC=$(curl -s -m 10 -o /dev/null -w '%{redirect_url}' "$URL/")
chk "yönlendirme sunucu adresine gidiyor ($LOC)" "echo \"$LOC\" | grep -q \"$IP\" || [ -z \"$LOC\" ]"

echo "== T4: dış kaynak =="
DIS=$(curl -s -m 10 -L "$URL/login/index.php" | grep -oE '(src|href)="https?://[^"]+"' | grep -v "$HOST" | sort -u)
if [ "$CODE" != 200 ] && [ "$CODE" != 303 ]; then bad "dış kaynak taraması yapılamadı (sayfa açılmadı)"
elif [ -z "$DIS" ]; then ok "dış bağlantı yok"; else bad "dış bağlantılar:"; echo "$DIS" | sed 's/^/      /'; fi

echo; echo "Özet: $GEC geçti, $KAL kaldı"; [ "$KAL" -eq 0 ]
