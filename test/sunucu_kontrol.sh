#!/usr/bin/env bash
# Sunucu (PC-1) otomatik kontrolleri. Kullanım: bash test/sunucu_kontrol.sh
cd "$(dirname "$0")/.." || exit 1
set -a; . ./.env; set +a
GEC=0; KAL=0
ok()  { echo "  [GEÇTİ] $1"; GEC=$((GEC+1)); }
bad() { echo "  [KALDI] $1"; KAL=$((KAL+1)); }
chk() { if eval "$2" >/dev/null 2>&1; then ok "$1"; else bad "$1"; fi; }

HOST=${MOODLE_WWWROOT#http://}; IP=${HOST%%:*}
echo "== 1. Servisler =="
for s in db moodle cron jobe; do
  chk "$s çalışıyor" "docker compose ps --status running --services | grep -qx $s"
done
chk "db healthy" "docker compose ps db | grep -q healthy"

echo "== 2. Adres ve erişim =="
echo "  wwwroot: $MOODLE_WWWROOT"
chk "wwwroot IP'si bu bilgisayarda tanımlı ($IP)" "ip -4 -br addr | grep -q \"$IP/\""
CODE=$(curl -s -m 10 -o /dev/null -w '%{http_code}' "$MOODLE_WWWROOT/login/index.php")
chk "giriş sayfası yanıt veriyor (HTTP $CODE)" "[ \"$CODE\" = 200 ] || [ \"$CODE\" = 303 ]"
chk "güvenlik duvarında ${MOODLE_PORT}/tcp açık" "sudo -n firewall-cmd --list-ports | grep -q ${MOODLE_PORT}/tcp || sudo -n firewall-cmd --list-all | grep -q ${MOODLE_PORT}"

echo "== 3. Dış kaynak bağımlılığı (giriş sayfası) =="
DIS=$(curl -s -m 10 -L "$MOODLE_WWWROOT/login/index.php" | grep -oE '(src|href)="https?://[^"]+"' | grep -v "$HOST" | sort -u)
if [ "$CODE" != 200 ] && [ "$CODE" != 303 ]; then bad "dış kaynak taraması yapılamadı (sayfa açılmadı)"
elif [ -z "$DIS" ]; then ok "dış alan adına bağlantı yok"; else bad "dış bağlantılar bulundu:"; echo "$DIS" | sed 's/^/      /'; fi

echo "== 4. Jobe (kod çalıştırma) =="
KEY=$(docker compose exec -T db mariadb -N -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "select value from mdl_config_plugins where plugin='qtype_coderunner' and name='jobe_apikey'")
SONUC=$(docker compose exec -T moodle curl -s -m 20 -X POST http://jobe/jobe/index.php/restapi/runs \
  -H 'Content-Type: application/json' -H "X-API-KEY: $KEY" \
  -d '{"run_spec":{"language_id":"python3","sourcecode":"print(6*7)"}}')
chk "python3 kodu Jobe'da çalıştı (çıktı 42)" "echo '$SONUC' | grep -q '\"stdout\":\"42'"
SONSUZ=$(docker compose exec -T moodle curl -s -m 40 -X POST http://jobe/jobe/index.php/restapi/runs \
  -H 'Content-Type: application/json' -H "X-API-KEY: $KEY" \
  -d '{"run_spec":{"language_id":"python3","sourcecode":"while True: pass","parameters":{"cputime":2}}}')
chk "sonsuz döngü zaman aşımıyla kesildi (outcome 13)" "echo '$SONUC$SONSUZ' | grep -q '\"outcome\":13'"

echo "== 5. Güvenlik =="
chk "ADMIN_PASS varsayılan değil" "[ \"$ADMIN_PASS\" != 'Admin.1234!' ]"
chk "DB_ROOT_PASSWORD varsayılan değil" "[ \"$DB_ROOT_PASSWORD\" != 'root_degistir' ]"
chk "config.php debugdisplay kapalı" "! grep -Eq '^\\\$CFG->debugdisplay *= *1' config.php"

echo "== 6. Sunucu internetsiz mi? (bilgi) =="
if ping -c1 -W2 8.8.8.8 >/dev/null 2>&1; then echo "  [BİLGİ] sunucuda internet VAR (lab testi için kapatın)"; else echo "  [BİLGİ] sunucuda internet yok"; fi

echo; echo "Özet: $GEC geçti, $KAL kaldı"; [ "$KAL" -eq 0 ]
