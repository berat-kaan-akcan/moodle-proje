# Lab Ortamı Test Kılavuzu

| | |
|---|---|
| **Amaç** | Sistemin, internetsiz bir lab ağında sınav için hazır olduğunu kanıtlamak |
| **Sunucu** | Hocanın bilgisayarı (Linux, Docker Compose, kendi Wi‑Fi hotspot'unu yayar) |
| **İstemciler** | Bir öğrenci PC'si (PC‑2) ve bir telefon |
| **Hazır betikler** | [test/](../test/) klasörü (aşağıda anlatılıyor) |
| **Sonuç formu** | Bu belgenin sonunda (Bölüm 9) |

> Komutlar proje klasöründe çalıştırılır: `cd ~/moodle-proje`. Kabuk fish ise `heredoc` (`<<EOF`) çalışmaz; bu yüzden betikler dosya olarak hazırlandı ve `bash betik.sh` ile çağrılıyor.

---

## 1. Ne test ediyoruz, başarı ölçütü nedir?

Sınav günü senaryo: Moodle hocanın bilgisayarında çalışır, öğrenciler lab bilgisayarlarından `http://<hoca-IP>:8080` adresine tarayıcıyla bağlanır, **öğrencilerin internet erişimi yoktur**.

Testin cevaplaması gereken sorular:
1. Öğrenci cihazı internetsizken Moodle'a girebiliyor mu?
2. Sayfalar eksiksiz yükleniyor mu? (Dış font/script/CDN bağımlılığı yok mu?)
3. Kod soruları (CodeRunner + Jobe) internetsiz çalışıyor mu? Monaco editör açılıyor mu?
4. Lab kapasitesi kadar öğrenci aynı anda girince sistem dayanıyor mu?
5. Sunucu uykuya geçmeden, yeniden başlatmadan sonra veri kaybetmeden sınav bitiyor mu?

**Başarı ölçütü:** T1–T10 testlerinin hepsi geçmeli. Kalan test varsa düzeltilip tekrarlanır.

**Neden "telefonla girdim, çalıştı" yetmez?** Cihazda gizli bir internet yolu (mobil veri, ikinci Wi‑Fi, VPN) varsa sayfa yine açılır ve test yanlış sonuç verir. Bu yüzden her istemcide önce **internetin yokluğu** (Google açılmıyor), sonra **sunucuya erişim** (Moodle açılıyor) kanıtlanır.

---

## 2. Hazır test betikleri

| Betik | Nerede çalışır | Ne yapar |
|---|---|---|
| [test/sunucu_kontrol.sh](../test/sunucu_kontrol.sh) | Sunucu | Servisler, adres/IP uyumu, güvenlik duvarı, dış bağlantı taraması, Jobe (normal + sonsuz döngü), güvenlik ayarları |
| [test/istemci_kontrol.sh](../test/istemci_kontrol.sh) | PC‑2 (Linux) | İnternet yok kanıtı (ping/DNS/HTTPS), sunucuya erişim, dış kaynak taraması |
| [test/yuk_testi.py](../test/yuk_testi.py) | Sunucu / Jobe konteyneri | Eşzamanlı yük: giriş sayfası ve Jobe |

```bash
sudo bash test/sunucu_kontrol.sh                       # sudo: güvenlik duvarı kontrolü için
bash test/istemci_kontrol.sh http://10.42.0.1:8080     # PC‑2'de
```

Her satır `[GEÇTİ]` / `[KALDI]` yazar, en sonda özet verir. Betik çıktısını ekran görüntüsü olarak rapora ekleyin.

---

## 3. Ön hazırlık (internetli ortamda, evde)

```bash
cd ~/moodle-proje
docker compose pull                  # imajlar güncel/yerelde olsun
docker compose up -d
docker compose ps                    # db, moodle, cron, jobe: Up; db: healthy
```

Güvenlik ayarları (T9'da kontrol edilir; şimdi düzeltmek en kolayı):

```bash
# Moodle admin şifresini arayüzden veya CLI ile değiştirin (KILAVUZ §4), .env'deki ADMIN_PASS değerini de güncelleyin
nano .env
# config.php: sınav sırasında hata ayrıntısı öğrenciye görünmesin
sed -i "s/^\$CFG->debugdisplay = 1;/\$CFG->debugdisplay = 0;/" config.php
grep -n debug config.php
docker compose up -d                 # ortam değişkenleri değiştiyse yeniden oluşturur
```

> **Dikkat:** `DB_PASSWORD` ve `DB_ROOT_PASSWORD` veritabanı ilk oluşturulurken içeri yazılır; sonradan yalnızca `.env`'de değiştirmek Moodle'ın veritabanına bağlanamamasına yol açar. Bu iki şifreyi mevcut kurulumda değiştirmeyin (sunucu ağdan dışarıya DB portu açmıyor). Sınav öncesi değiştirilmesi gereken şey Moodle **admin şifresi**dir (KILAVUZ §4); `test/sunucu_kontrol.sh` içindeki `DB_ROOT_PASSWORD` uyarısı bu durumda bilgi olarak kabul edilir.

Test öğrenci hesapları ve test sınavı hazır olmalı (KILAVUZ §12.3). Ayrıca Monaco editörünün sorularda açıldığını internetli ortamda bir kez deneyin.

---

## 4. İnternetsiz test ağını kurma (sunucu PC)

### Seçenek 1 (önerilen): sunucu kendi Wi‑Fi'ını yayar

```bash
nmcli device status                                           # Wi‑Fi arayüzü adı (örn. wlan0)
nmcli device wifi hotspot ifname wlan0 ssid MOODLE-TEST password test12345
ip -4 -br addr show wlan0                                     # genelde 10.42.0.1/24
```

Hotspot yayınlayan PC'nin kendi internetini istemcilere **paylaşmaması** gerekir. NetworkManager'ın paylaşımlı modu (`ipv4.method shared`) NAT yapar; sunucunun başka bir bağlantısı (Ethernet) internete çıkıyorsa istemciler de internete çıkar. Kanıt A (T1) bunu yakalar. Çözüm: Ethernet'i kapatın.

```bash
nmcli device disconnect eno1          # kablolu bağlantıyı kes (arayüz adını nmcli device status'tan alın)
ping -c2 -W2 8.8.8.8                  # YANIT GELMEMELİ
```

### Seçenek 2: internetsiz router/switch
Sunucu ve istemciler aynı internetsiz router'a bağlanır. IP'yi `ip -4 -br addr` ile öğrenin (örn. `192.168.1.25`).

### Seçenek 3: internetli ağda istemci çıkışını engelleme
Yalnızca mümkün olmazsa. Router'dan istemcilerin internet çıkışını engelleyin. T1 ile doğrulayın.

---

## 5. Sunucuyu yeni adrese göre hazırlama

Moodle, `.env` içindeki `MOODLE_WWWROOT` adresini kullanır. Adres yanlışsa giriş sonrası tarayıcı eski adrese (`localhost` ya da eski IP) yönlenir ve sayfa açılmaz.

```bash
IP=$(ip -4 -br addr show wlan0 | awk '{print $3}' | cut -d/ -f1)
echo $IP
sed -i "s|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://$IP:8080|" .env
grep WWWROOT .env
docker compose up -d                   # moodle ve cron yeni adresle yeniden oluşur
docker compose exec -T moodle php /var/www/html/admin/cli/purge_caches.php
```

Güvenlik duvarı (firewalld). Hotspot arayüzünün hangi bölgede olduğuna bakın ve 8080'i orada açın:

```bash
sudo firewall-cmd --get-zone-of-interface=wlan0
sudo firewall-cmd --zone=$(sudo firewall-cmd --get-zone-of-interface=wlan0) --add-port=8080/tcp   # geçici
# kalıcı olsun istiyorsanız komuta --permanent ekleyip: sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

Sunucu kendi kendini doğrulasın:

```bash
curl -I http://$IP:8080/login/index.php      # 200 veya 303
sudo bash test/sunucu_kontrol.sh             # tamamı GEÇTİ olmalı (T9 maddeleri düzeltildiyse)
```

> `200` = sayfa geldi; `303` = Moodle başka sayfaya yönlendiriyor (normal). `Connection refused` / `timed out` = ulaşılamıyor.

---

## 6. İstemcileri hazırlama ve kontrol etme

| Cihaz | Bağlantı | İnternet |
|---|---|---|
| PC‑1 | Sunucu, hotspot yayıncısı (`10.42.0.1`) | Olmamalı |
| PC‑2 | `MOODLE-TEST` Wi‑Fi'ına bağlı | **Olmamalı**: Ethernet/VPN/USB tethering kapalı |
| Telefon | `MOODLE-TEST` Wi‑Fi'ına bağlı | **Mobil veri kapalı** |

### Telefon
1. Mobil veriyi kapatın (veya uçak modu + yalnızca Wi‑Fi). "Akıllı ağ geçişi / Wi‑Fi+" seçeneklerini kapatın.
2. `MOODLE-TEST` ağına bağlanın (şifre `test12345`). "İnternet yok, bağlı kalınsın mı?" sorusuna **Bağlı kal** deyin.
3. Kontrol:

| # | İşlem | Beklenen |
|---|---|---|
| 1 | `https://www.google.com` | **Açılmaz** |
| 2 | `https://1.1.1.1` | **Açılmaz** |
| 3 | `http://10.42.0.1:8080` | Moodle giriş sayfası |
| 4 | Öğrenci girişi, kurs, sınav | Çalışır |

Adresi **`http://`** ile yazın; Moodle'da HTTPS yok.

### PC‑2 (Linux)
```bash
nmcli device status          # yalnızca Wi‑Fi bağlı olmalı
ip -4 -br addr               # 10.42.0.x
bash test/istemci_kontrol.sh http://10.42.0.1:8080
```
Elle karşılığı:
```bash
ping -c3 8.8.8.8                              # %100 kayıp
getent hosts google.com                       # sonuç dönmemeli
curl -I --max-time 5 https://www.google.com   # hata/zaman aşımı
ping -c3 10.42.0.1                            # yanıt gelmeli
curl -I http://10.42.0.1:8080                 # 200/303
```
Windows PowerShell:
```powershell
ipconfig
ping 8.8.8.8                                  # zaman aşımı
nslookup google.com                           # hata
ping 10.42.0.1                                # yanıt
Test-NetConnection 10.42.0.1 -Port 8080       # TcpTestSucceeded : True
curl.exe -I http://10.42.0.1:8080
```

---

## 7. Test senaryoları

Her test: **ne yapılır → beklenen → başarısızsa ne anlama gelir**.

### T1 – İstemcide internet YOK (kanıt A)
Telefon: Google ve `1.1.1.1` açmayı deneyin. PC‑2: `ping 8.8.8.8`, `getent hosts google.com`, `curl https://www.google.com`.
**Beklenen:** Hiçbiri çalışmaz.
**Kaldıysa:** Gizli internet yolu var (mobil veri, ikinci ağ, VPN, sunucunun NAT paylaşımı). **Sonraki testler geçersiz**; önce çözün.

### T2 – İstemci sunucuya ulaşıyor (kanıt B)
```bash
ping -c3 10.42.0.1
curl -I http://10.42.0.1:8080
```
**Beklenen:** Ping yanıtlı, `curl` 200/303, telefonda giriş sayfası.
**Kaldıysa:** Farklı alt ağ, yanlış IP ya da güvenlik duvarı. Sunucuda:
```bash
sudo firewall-cmd --list-all
ip neigh show dev wlan0          # bağlı cihazlar görünüyor mu?
```
Hâlâ yoksa [hotspot-test.sh](../hotspot-test.sh) paketlerin sunucuya ulaşıp ulaşmadığını (nft sayaçları) gösterir: `sudo bash hotspot-test.sh` (180 sn boyunca istemciden `ping 10.42.0.1` ve tarayıcıdan `:8091`/`:8080` açın).

### T3 – Giriş ve sayfa yükleme
Öğrenci hesabıyla giriş yapın, kursa girin, birkaç sayfa gezin.
**Beklenen:** Stil, simge ve fontlar tam, hata yok, adres çubuğu `10.42.0.1` kalıyor.
**Kaldıysa:** Çıplak sayfa → dış kaynak (T4). Adres `localhost` ya da eski IP oluyorsa `.env` güncel değil (Bölüm 5).

### T4 – Dış kaynak bağımlılığı
Otomatik:
```bash
curl -s -L http://10.42.0.1:8080/login/index.php | grep -oE '(src|href)="https?://[^"]+"' | grep -v 10.42.0.1 | sort -u
```
Çıktı boş olmalı. Elle: istemci tarayıcıda **F12 → Network**, sayfayı yenileyin; `10.42.0.1` dışına giden veya kırmızı biten istek olmamalı. Giriş sayfası, kurs sayfası, **sınav sayfası** (Monaco editör dahil) için ayrı ayrı bakın.
**Kaldıysa:** Dış alan adlarını listeleyip rapora yazın. Genelde Moodle ayarlarından kapatılır (gravatar, güncelleme bildirimi). Monaco editör dış dosya istiyorsa `monaco/` klasörü eksiktir.

### T5 – CodeRunner + Jobe
Önce sunucuda otomatik:
```bash
KEY=$(docker compose exec -T db mariadb -N -u moodle -p"$(grep ^DB_PASSWORD .env | cut -d= -f2)" moodle \
  -e "select value from mdl_config_plugins where plugin='qtype_coderunner' and name='jobe_apikey'")
docker compose exec -T moodle curl -s http://jobe/jobe/index.php/restapi/languages        # python3 listede
docker compose exec -T moodle curl -s -X POST http://jobe/jobe/index.php/restapi/runs \
  -H 'Content-Type: application/json' -H "X-API-KEY: $KEY" \
  -d '{"run_spec":{"language_id":"python3","sourcecode":"print(6*7)"}}'                   # "stdout":"42\n"
```
Sonra istemciden bir CodeRunner sorusunda (örn. `s1_topla`) şunları deneyin:

| Deneme | Beklenen |
|---|---|
| Doğru çözüm → **Kontrol et** | Tüm testler yeşil |
| Söz dizimi hatası | Anlaşılır hata mesajı |
| `while True: pass` | Zaman aşımıyla kesilir, sistem donmaz |
| Monaco: Tab girintisi, renklendirme | Çalışır |

**Kaldıysa:** `docker compose ps jobe`; `docker compose restart jobe`; `docker compose logs --tail=50 jobe`.

### T6 – Sınav akışı
Giriş → sınavı başlat → cevap yaz → sayfayı yenile → sınavı bitir → hoca hesabında denemeyi ve notu gör.
**Beklenen:** Cevaplar kaybolmaz, oturum düşmez, hocada deneme ve not görünür.
Not kontrolü terminalden:
```bash
docker compose exec -T db mariadb -u moodle -p"$(grep ^DB_PASSWORD .env | cut -d= -f2)" moodle \
  -e "select id,userid,state,sumgrades from mdl_quiz_attempts order by id desc limit 10;"
```

### T7 – Eşzamanlı yük
Lab kapasitesi (örn. 30–50 öğrenci) için. Önce sayfa yükü, sonra Jobe:
```bash
python3 test/yuk_testi.py sayfa http://10.42.0.1:8080 50
KEY=$(docker compose exec -T db mariadb -N -u moodle -p"$(grep ^DB_PASSWORD .env | cut -d= -f2)" moodle \
  -e "select value from mdl_config_plugins where plugin='qtype_coderunner' and name='jobe_apikey'")
docker compose exec -T jobe python3 - jobe 50 "$KEY" < test/yuk_testi.py
```
Başka bir terminalde izleyin:
```bash
docker stats
```
**Beklenen:** Hiç hata yok (`{200: 50}` ve `{15: 50}`), en yavaş yanıt birkaç saniyeyi geçmez, CPU/RAM sürekli %100'de kalmaz.
Referans (bu bilgisayarda, internetsiz değil, tek sunucu üzerinde): 50 eşzamanlı Jobe işi hepsi başarılı, en yavaş ~1,6 sn.
Gerçek yük için 3–5 cihazda aynı anda çok sekme açıp **Kontrol et**'e basın.
**Kaldıysa:** Sunucuya RAM/CPU eksik ya da Jobe eşzamanlı iş sınırı; sonuçları (kaç kişi, kaç sn) rapora yazın.

### T8 – Sunucu dayanıklılığı
```bash
# Uyku/askıya almayı sınav süresince kapat (GNOME/KDE güç ayarlarından da yapılabilir)
systemd-inhibit --what=sleep:idle --why="Sinav" sleep 4h &

# Konteynerleri yeniden başlat, veri korunuyor mu?
docker compose restart
docker compose ps
```
Ayrıca 10–15 dk bekleyip sistemin yanıt verdiğini, hotspot'tan kısa kopma sonrası öğrenci oturumunun devam ettiğini doğrulayın. Bilgisayar fişte olmalı, kapak kapanınca uyumamalı.
**Beklenen:** Yeniden başlatma sonrası sistem kendiliğinden kalkar (`restart: unless-stopped`), cevaplar korunur.

### T9 – Güvenlik ve yetki
```bash
sudo bash test/sunucu_kontrol.sh        # "5. Güvenlik" bölümü
```
Elle: öğrenci hesabıyla `http://10.42.0.1:8080/admin/` açılmamalı. `ADMIN_PASS` ve `DB_ROOT_PASSWORD` varsayılan olmamalı; `config.php` içinde `debugdisplay = 0` olmalı.

### T10 – Yedek ve geri dönüş
Sınavdan önce yedek alın, sorun olursa dönebilmek için:
```bash
docker compose exec -T db mariadb-dump -u moodle -p"$(grep ^DB_PASSWORD .env | cut -d= -f2)" moodle > ~/moodle-yedek-$(date +%F).sql
ls -lh ~/moodle-yedek-*.sql
```
Tüm yedekleme/geri yükleme adımları: [KILAVUZ.md §18](KILAVUZ.md).

---

## 8. Test sonrası geri alma

```bash
nmcli connection down Hotspot            # hotspot'u kapat
sed -i "s|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://localhost:8080|" .env
docker compose up -d
sudo firewall-cmd --zone=$(sudo firewall-cmd --get-default-zone) --remove-port=8080/tcp   # geçici açtıysanız
```
Kalıcı yapılandırmada adres sabit bir IP ise `.env` içinde o IP kalır.

---

## 9. Sonuç formu

| | |
|---|---|
| **Test tarihi** | ____ / ____ / ________ |
| **Testi yapanlar** | ______________________ |
| **Sunucu PC** | ______________________ (işletim sistemi, model) |
| **Öğrenci PC** | ______________________ |
| **Telefon** | ______________________ (marka/model, Android/iOS) |
| **Ağ** | ☐ Hotspot  ☐ İnternetsiz router  ☐ Diğer: ________ |
| **Sunucu adresi** | http://____________:8080 |

| # | Test | Cihaz | Beklenen | Sonuç | Not / ekran görüntüsü |
|---|---|---|---|---|---|
| T1 | İstemcide internet yok | | Google/ping/DNS başarısız | ☐ Geçti ☐ Kaldı | |
| T2 | Sunucuya erişim | | Ping yanıtlı, 200/303 | ☐ Geçti ☐ Kaldı | |
| T3 | Giriş ve sayfa yükleme | | Tam yüklenir, adres doğru | ☐ Geçti ☐ Kaldı | |
| T4 | Dış kaynak yok | | Dış istek yok (Monaco dahil) | ☐ Geçti ☐ Kaldı | |
| T5 | CodeRunner / Jobe | | Doğru/hata/sonsuz döngü doğru | ☐ Geçti ☐ Kaldı | |
| T6 | Sınav akışı | | Uçtan uca, not görünür | ☐ Geçti ☐ Kaldı | |
| T7 | Eşzamanlı yük (__ kişi) | | Hata yok, yanıt < __ sn | ☐ Geçti ☐ Kaldı | |
| T8 | Dayanıklılık | | Uyku yok, yeniden başlatma sonrası veri duruyor | ☐ Geçti ☐ Kaldı | |
| T9 | Güvenlik | | Şifreler değişik, debug kapalı, admin kapalı | ☐ Geçti ☐ Kaldı | |
| T10 | Yedek | | Yedek dosyası alındı | ☐ Geçti ☐ Kaldı | |

**Genel değerlendirme**
- [ ] Tüm testler geçti, lab günü için hazır.
- [ ] Bazı testler kaldı. Sorunlar ve çözüm planı: ______________________________

---

## 10. Lab günü kısa kontrol listesi

- [ ] Fiş takılı, uyku kapalı (`systemd-inhibit` / güç ayarları)
- [ ] Hotspot açık, `ip -4 -br addr show wlan0` ile IP alındı
- [ ] `.env` adresi güncel, `docker compose up -d` yapıldı
- [ ] Güvenlik duvarında 8080 açık
- [ ] `sudo bash test/sunucu_kontrol.sh` tamamı geçti
- [ ] Bir istemciden `istemci_kontrol.sh` tamamı geçti
- [ ] Hoca hesabıyla sınav açık, test öğrencisiyle bir soru denendi
- [ ] Adres öğrencilere duyuruldu (`http://` ile, HTTPS değil)
- [ ] Yedek alındı
