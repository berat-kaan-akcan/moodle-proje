# Lab Ağında Sınav: DHCP'siz Switch Üzerinden Moodle Yayınlama

| | |
|---|---|
| **Senaryo** | Labda tek switch var, DHCP yok, Wi‑Fi yok, internet yok. Lab PC'lerinde Pardus kurulu. |
| **Sunucu** | Senin dizüstün (CachyOS): Docker'da Moodle + MariaDB + Jobe, kablolu kart `eno1` |
| **Hedef** | Lab PC'leri tarayıcıdan `http://<senin-IP>:8080` adresine girsin, internete **çıkamasın** |
| **Hazır betikler** | Sunucu: [test/lab_hazirla.sh](../test/lab_hazirla.sh) · Lab PC'si: [test/istemci_hazirla.sh](../test/istemci_hazirla.sh) |

---

## 1. Mantık (neden çalışır, neden internet olmaz)

```
                 ┌─────────────── LAB SWITCH (okul ağına bağlı DEĞİL) ───────────────┐
                 │                                                                   │
   Dizüstü (CachyOS)                    Pardus PC-1         Pardus PC-2   ...   Pardus PC-N
   eno1: 192.168.50.1/24               192.168.50.x        192.168.50.y        192.168.50.z
   Wi‑Fi KAPALI                         tarayıcı → http://192.168.50.1:8080
   Docker → :8080 Moodle
```

- Switch yalnızca aynı alt ağdaki (`192.168.50.0/24`) cihazları birbirine bağlar. Herkes aynı alt ağda bir IP adresi alırsa birbirine ulaşır.
- **DHCP'yi sen sağlarsın:** NetworkManager'ın paylaşım modu (`ipv4.method shared`) senin dizüstünde küçük bir DHCP sunucusu (dnsmasq) çalıştırır. Pardus PC'leri "otomatik (DHCP)" ayarındaysa IP'yi senden alır ve PC'lere tek tek dokunman gerekmez.
- **İnternet yok, çünkü:** Switch'in dışarıya bağlantısı yok. Senin dizüstünün de internete çıkışı yok, çünkü Wi‑Fi kapalı. Paylaşım modu, internet varsa onu dağıtır. **Wi‑Fi (ya da telefondan USB/Bluetooth bağlantı) açık kalırsa lab PC'leri senin üzerinden internete çıkar.** Bu yüzden betik Wi‑Fi'ı kendisi kapatır.

Seçilen ağ `192.168.50.0/24`: Docker'ın kullandığı `172.17/172.18` ağlarıyla çakışmaz.

---

## 2. Önce öğren: Lab PC'leri hangi ayarda? (labda 2 dakika)

Bir Pardus PC'sinde terminal aç (Uygulamalar → Uçbirim):

```bash
ip -4 -br addr            # PC'nin IP'si var mı?
nmcli device show | grep -E 'GENERAL.DEVICE|IP4.ADDRESS|IP4.GATEWAY'
nmcli -f NAME,TYPE,DEVICE connection show
```

| Görülen | Anlamı | Ne yapacaksın |
|---|---|---|
| Kablolu kartta IP yok ya da `169.254.x.x` var | PC DHCP bekliyor, ama labda DHCP yok | **Durum A** (en kolayı): Dizüstün DHCP dağıtır, PC'lere dokunmazsın |
| Her PC'de sabit bir IP var (örn. `10.10.5.23/24`) | PC'ler elle ayarlanmış | **Durum B**: Dizüstün o ağa boş bir IP ile katılır, PC'lere dokunmazsın |
| Karışık ya da bozuk | – | **Durum C**: PC'lere USB ile [istemci_hazirla.sh](../test/istemci_hazirla.sh) çalıştırılır |

**Switch'i de kontrol et:** Switch'ten duvara ya da başka bir dolaba giden bir kablo (uplink) var mı? Varsa switch okul ağına bağlı olabilir. Bu durumda okul ağına DHCP dağıtmak başka cihazları bozar (sahte DHCP sunucusu). Ya o kabloyu çıkar (lab sorumlusuyla konuşarak) ya da Durum A yerine `LAB_YONTEM=manual` kullan (bkz. 4.2).

---

## 3. Evde ön hazırlık (internet varken)

Labda internet olmayacağı için **her şey önceden indirilmiş olmalı**.

```bash
cd ~/moodle-proje
docker compose pull                 # imajlar güncel ve yerelde olsun (labda çekilemez)
docker compose up -d
docker compose ps                   # db, moodle, cron, jobe: Up / healthy
bash test/sunucu_kontrol.sh         # şimdilik adres maddeleri kalabilir, Jobe maddeleri GEÇMELİ
```

- [ ] `.env` içindeki varsayılan şifreleri (`ADMIN_PASS`, `DB_ROOT_PASSWORD`) değiştir. Moodle admin şifresini arayüzden de değiştir.
- [ ] Sınav, sorular ve öğrenci hesapları hazır (CSV yükleme: [scripts/sifre_uret.py](../scripts/sifre_uret.py)). Şifre dağıtım listesini yazdır.
- [ ] `test/` klasörünü **USB belleğe** kopyala (Pardus PC'lerinde gerekirse lazım olacak).
- [ ] Yanına al: **Ethernet kablosu** (switch'e yetecek uzunlukta), **şarj aleti**, yedek kablo. Dizüstünde ethernet portu var (`eno1`).
- [ ] İsteğe bağlı prova: Evde dizüstünü ve başka bir bilgisayarı kabloyla doğrudan bağla ya da internetsiz bir switch kullan. Sonra aşağıdaki adımları baştan sona dene.

---

## 4. Lab günü: Sunucu (senin dizüstün)

### 4.1 Önerilen: tek komut

1. Fişi tak, kabloyu dizüstü ile switch arasına tak. Switch'teki port ışığı yanmalı.
2. Terminal (fish da olur; betik bash ile çalışır, **sudo kullanma**, gerektiğinde şifreni kendisi sorar):

```bash
cd ~/moodle-proje
bash test/lab_hazirla.sh
```

Betik sırasıyla şunları yapar:

| Adım | Ne yapar |
|---|---|
| 1. Ağ | Wi‑Fi'ı kapatır. `eno1` üzerinde kablo bekler. 20 sn DHCP bekler, DHCP yoksa `lab` adlı bağlantıyı açar: `192.168.50.1/24`, paylaşım modu. Bu modda lab PC'lerine `192.168.50.x` dağıtılır. |
| 2. Yedek | Veritabanının yedeğini `cikti/yedek-lab-TARİH.sql.gz` dosyasına alır |
| 3. Adres | `.env` içinde `MOODLE_WWWROOT=http://192.168.50.1:8080` yazar, konteynerleri yeniler, önbelleği temizleyip yeniden ısıtır |
| 4. Firewall | `eno1` arayüzünün bölgesinde (`nm-shared`) 8080/tcp'yi açar. Senin makinende zaten kalıcı olarak açık. |
| 5. Uyku | 8 saat boyunca uyku/askıya almayı engeller |
| Kontrol | [test/sunucu_kontrol.sh](../test/sunucu_kontrol.sh) betiğini çalıştırır: servisler, adres, dış bağlantı, Jobe |

Sonda öğrencilere söylenecek adresi yazar: **`http://192.168.50.1:8080`**

> Farklı bir ağ seçmek için: `LAB_AG=10.99.0.1/24 bash test/lab_hazirla.sh`

### 4.2 Durum B ya da switch okul ağına bağlıysa: DHCP dağıtmadan

**Lab PC'leri zaten sabit IP'liyse (Durum B):** Onların ağından boş bir adres seç. Örnek: PC'ler `10.10.5.0/24` ağında. Aday adresin kullanılmadığını doğrula (kablo takılıyken, dizüstünde):

```bash
sudo arping -D -I eno1 -c 3 10.10.5.250 && echo BOŞ || echo "KULLANIMDA, başka adres seç"
```

(Alternatif: Bir lab PC'sinden `ping 10.10.5.250` çalıştır. Yanıt gelmiyorsa adres boştur.) Sonra:

```bash
LAB_AG=10.10.5.250/24 LAB_YONTEM=manual bash test/lab_hazirla.sh
```

**Switch okul ağına bağlıysa ama PC'ler DHCP bekliyorsa:** `LAB_YONTEM=manual bash test/lab_hazirla.sh` çalıştır, sonra PC'lere IP'yi Durum C'deki gibi ver.

### 4.3 Betik çalışmazsa: elle (aynı adımlar)

```bash
# 1) Ağ
nmcli radio wifi off
nmcli connection delete lab 2>/dev/null
nmcli connection add type ethernet ifname eno1 con-name lab autoconnect no \
      ipv4.method shared ipv4.addresses 192.168.50.1/24 ipv6.method disabled   # DHCP dağıtmamak için: ipv4.method manual
nmcli connection up lab
ip -4 -br addr show eno1                    # 192.168.50.1/24 görünmeli

# 2) Moodle adresi
cd ~/moodle-proje
sed -i 's|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://192.168.50.1:8080|' .env
docker compose up -d
docker compose exec -T -u www-data moodle php /var/www/html/admin/cli/purge_caches.php

# 3) Firewall (hangi bölgede olduğuna bak, oraya aç)
sudo firewall-cmd --get-zone-of-interface=eno1
sudo firewall-cmd --zone=nm-shared --add-port=8080/tcp      # manual modda bölge genelde: public

# 4) Uyku
systemd-inhibit --what=sleep:idle --why="Moodle lab" sleep 8h &

# 5) Kontrol
curl -s -o /dev/null -w '%{http_code}\n' http://192.168.50.1:8080/login/index.php   # 200 ya da 303
ping -c2 -W2 8.8.8.8                        # YANIT GELMEMELİ
```

---

## 5. Lab günü: Pardus PC'leri

### Durum A: PC'ler DHCP'de (önerilen yol)

Hiçbir ayar gerekmez. Dizüstünde betik bittikten sonra PC'nin kablosunu çıkarıp tak ya da sağ alttaki ağ simgesinden bağlantıyı kes/bağlan. PC `192.168.50.x` adresini alır. Tarayıcıda:

```
http://192.168.50.1:8080
```

Hangi PC'lerin IP aldığını dizüstünden görmek için: `ip neigh show dev eno1`

### Durum B: PC'ler zaten sabit IP'li

Ayar gerekmez. Adres, 4.2'de seçtiğin IP olur: `http://10.10.5.250:8080`

### Durum C: PC'ye elle IP vermek

**a) USB'deki betikle (en hızlı):**

```bash
cd /media/$USER/<USB>/test
bash istemci_hazirla.sh 192.168.50.1
```

Betik önce mevcut ayarla dener, sonra DHCP'yi dener. İkisi de olmazsa `192.168.50.100–249` arasından **boş** bir adres alır: NetworkManager adresi kullanmadan önce ağda başka biri kullanıyor mu diye sorar, kullanılıyorsa bir sonrakine geçer. Sonra kontrolleri çalıştırır. Ağ ayarı için yetki isterse lab yöneticisinin şifresi gerekir.
> Pardus'ta `curl` kurulu değilse betik IP'yi verir ama kontrol aşamasında "curl yok" der. Bu bir sorun değil, tarayıcıdan dene.

**b) Arayüzden (yetki varsa, betik yoksa):**
Ağ simgesi → **Bağlantıları Düzenle** (GNOME'da: Ayarlar → Ağ → Kablolu ⚙) → **IPv4 Ayarları** →
- Yöntem: **Elle**
- Adres: `192.168.50.101` (her PC'ye farklı bir sayı ver: PC-1 → .101, PC-2 → .102 …)
- Ağ maskesi: `24` (ya da `255.255.255.0`)
- Ağ geçidi: **boş** (ya da `192.168.50.1`)
- Kaydet, sonra bağlantıyı kapatıp aç.

**c) Terminalden:**

```bash
nmcli device                          # kablolu kartın adı (enp3s0, eno1 …)
sudo nmcli connection add type ethernet ifname enp3s0 con-name lab-istemci \
     ipv4.method manual ipv4.addresses 192.168.50.101/24 ipv6.method disabled
sudo nmcli connection up lab-istemci
ping -c2 192.168.50.1
```

### Tarayıcı notları
- Adresi **`http://`** ile yaz. Firefox `https://` deneyip hata verebilir.
- Okul Firefox'a proxy tanımladıysa: Ayarlar → Ağ Ayarları → **Proxy yok**.

---

## 6. İnternet olmadığını ve her şeyin çalıştığını doğrula

Bir lab PC'sinde (USB'deki betik):

```bash
bash istemci_kontrol.sh http://192.168.50.1:8080
```

- **Kanıt A:** `8.8.8.8`, DNS ve `google.com` erişilemiyor olmalı.
- **Kanıt B:** Sunucuya ping gidiyor, giriş sayfası 200/303 dönüyor.
- **T4:** Sayfa dışarıdan kaynak (font, CDN) istemiyor.

Elle kontrol: `ping 8.8.8.8` **yanıt vermemeli**, `ping 192.168.50.1` **yanıt vermeli**.

Öğrenciler girmeden önce: Hoca hesabıyla sınavı aç, bir CodeRunner sorusunda **Kontrol et**'e bas. Bu hem Jobe'u dener hem önbelleği ısıtır.

---

## 7. Sorun giderme

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Betik "NO-CARRIER / kabloda bağlantı yok" diyor | Kablo, port ya da switch kapalı | Başka port/kablo dene. Switch'in fişine bak. `cat /sys/class/net/eno1/carrier` 1 olmalı |
| PC IP almıyor (Durum A) | Dizüstünde paylaşım modu açılmadı ya da PC sabit IP'ye ayarlı | Dizüstünde `nmcli connection show --active` içinde `lab` görünmeli. `journalctl -u NetworkManager -n 50`. PC'de kabloyu çıkarıp tak ya da Durum C |
| PC IP aldı, ping gidiyor ama sayfa açılmıyor | Firewall ya da Moodle | Dizüstünde `sudo firewall-cmd --get-zone-of-interface=eno1`, ardından o bölgede `--list-ports` (8080 olmalı). `docker compose ps` |
| Sayfa açılıyor ama `localhost`'a ya da eski IP'ye yönleniyor | `.env` adresi güncel değil | `grep WWWROOT .env` → `http://192.168.50.1:8080` olmalı. `docker compose up -d` + purge_caches |
| Ping de gitmiyor | Farklı alt ağ ya da PC'nin kendi firewall'u | PC'de `ip -4 -br addr`. Sunucuyla aynı `192.168.50.x/24` ağında mı? |
| Lab PC'sinde internet var | Dizüstünde Wi‑Fi/USB tethering açık ya da switch okul ağına bağlı | Dizüstünde `nmcli radio wifi off`, telefonu çıkar. Switch'in uplink kablosunu kontrol et |
| İlk girişlerde "Önbelleğe almak için kilit alınamıyor" | Konteyner yeni başladı, önbellek boş | Bir dakika bekle, hoca hesabıyla sınavı bir kez aç. Sonra öğrencileri al |
| Kodlar "server overload" diyor | Jobe'a aynı anda çok iş geldi | Bekleme süresi 180 sn yapıldı. Kısa süre içinde düzelir. [test/sinav_yuk_testi.py](../test/sinav_yuk_testi.py) ile önceden dene |
| Kapak kapanınca/uyuyunca herkes düştü | Uyku | Kapağı kapatma. Engelin açık olduğunu `systemd-inhibit --list` ile kontrol et |

---

## 8. Sınav bitince geri alma

```bash
# Önce sonuçları yedekle
docker compose exec -T db mariadb-dump -u moodle -p<DB_PASSWORD> --single-transaction moodle | gzip > cikti/sinav-sonrasi-$(date +%F-%H%M).sql.gz

# Sunucu: adresi localhost'a döndürür, lab bağlantısını siler, 8080'i kapatır, uyku engelini kaldırır, Wi‑Fi'ı açar
bash test/lab_hazirla.sh --geri
```

Elle IP verdiğin Pardus PC'lerini okulun ayarına döndür: `bash istemci_hazirla.sh --geri`. Arayüzden yaptıysan yöntemi **Otomatik (DHCP)** yap ya da `sudo nmcli connection delete lab-istemci` çalıştır.

---

## 9. Lab günü kısa kontrol listesi

- [ ] Evde: `docker compose pull`, şifreler değişti, sınav hazır, `test/` USB'de
- [ ] Fiş takılı, kablo dizüstü ↔ switch, port ışığı yanıyor
- [ ] Bir Pardus PC'sinde `ip -4 -br addr` → Durum A / B / C belli
- [ ] Switch okul ağına bağlı değil (ya da `LAB_YONTEM=manual`)
- [ ] `bash test/lab_hazirla.sh` → sunucu kontrolü geçti, adres not edildi
- [ ] Bir lab PC'sinde `istemci_kontrol.sh` → internet YOK, sunucu VAR
- [ ] Hoca hesabıyla sınav ve bir CodeRunner sorusu denendi
- [ ] Adres tahtaya yazıldı: `http://192.168.50.1:8080`
- [ ] Bitince: yedek, `lab_hazirla.sh --geri`, PC'ler eski ayarına döndü
