# Lab Ortamı Test Planı ve Raporu

| | |
|---|---|
| **Proje** | MSKÜ DYS – Moodle 4.5 + CodeRunner + Jobe (Docker Compose) |
| **Test tarihi** | ____ / ____ / ________ |
| **Testi yapanlar** | ______________________ |
| **Sunucu PC (PC‑1)** | ______________________ (işletim sistemi, model) |
| **Öğrenci PC (PC‑2)** | ______________________ |
| **Telefon** | ______________________ (marka/model, Android/iOS) |

---

## 0. Bu doküman ne için?

### Senaryo
Hocamız sınavı laboratuvarda yapacak. Hoca **kendi bilgisayarını** laba getirecek, Moodle onun bilgisayarında çalışacak. Öğrenciler lab bilgisayarlarından tarayıcıyla hocanın bilgisayarının adresini (örn. `http://192.168.1.25:8080`) açacak. **Öğrencilerin internete erişimi olmayacak**, ama hocanın bilgisayarına erişebilecekler.

```
 [Hoca PC: Moodle + Veritabanı + Jobe (Docker)]
                     │
        lab ağı (switch/router, internet YOK)
                     │
        ┌────────────┼────────────┐
   [Öğrenci PC] [Öğrenci PC]  [Öğrenci PC] ...
```

### Bu testin cevaplaması gereken sorular
1. Öğrenci cihazı internetsizken Moodle'a girebiliyor mu?
2. Sayfalar eksiksiz yükleniyor mu? (Moodle bazen dışarıdan font/script çekmeye çalışır; internet yoksa sayfa bozuk görünebilir.)
3. Kod soruları (CodeRunner) internetsiz çalışıyor mu?
4. Lab kapasitesi kadar öğrenci aynı anda girince sistem dayanıyor mu?
5. Hoca laba gidince hangi adımları, hangi sırayla yapacak?

### Test cihazları ve rolleri
Laboratuvarı küçük ölçekte taklit ediyoruz:

| Cihaz | Lab'daki karşılığı |
|---|---|
| **PC‑1** | Hocanın bilgisayarı (sunucu) |
| **PC‑2** | Bir öğrenci bilgisayarı |
| **Telefon** | İkinci bir öğrenci cihazı. Özellikle "gerçekten internetsiz mi?" kontrolü için iyidir |

### Başarı ölçütü
T1–T9 testlerinin hepsi **Geçti** olmalı. Herhangi biri Kaldı ise lab günü öncesi düzeltilip tekrar denenmelidir.

---

## 1. Neden "telefonla girdim, çalıştı" yeterli değil?

Telefon mobil veriye ya da internetli bir Wi‑Fi'a bağlıysa, Moodle'a girebilmesi **internetsiz çalıştığını göstermez**. Çünkü sayfa, ağınızdaki sunucudan da gelmiş olabilir, internetten dolaşarak da. Test ancak şu **iki kanıt birlikte** varsa geçerlidir:

| Kanıt | Soru | Nasıl doğrulanır | Neyi önler? |
|---|---|---|---|
| **A** | İstemcinin interneti **gerçekten yok** mu? | `google.com` açılmıyor, `ping 8.8.8.8` yanıt vermiyor | Cihazın gizlice mobil veri/başka ağ kullanması |
| **B** | İstemci yine de Moodle'a **erişebiliyor** mu? | `http://SUNUCU_IP:8080` açılıyor | Ağ ya da güvenlik duvarı sorunlarını gözden kaçırmak |

> **Kural:** Önce A'yı, sonra B'yi doğrulayın. A başarısızsa (yani Google açılıyorsa) test geçersizdir: önce o cihazdaki gizli internet yolunu kapatın.

Gizli internet yolu örnekleri: mobil veri, aynı anda bağlı ikinci Wi‑Fi, Ethernet kablosu, USB ile telefon interneti paylaşımı, VPN, Tailscale.

---

## 2. İnternetsiz test ağının kurulması

### Seçenek 1 (önerilen): Sunucu PC kendi Wi‑Fi'ını (hotspot) yayar
Ek donanım gerekmez. Sunucu bir Wi‑Fi ağı oluşturur, diğer cihazlar ona bağlanır. Bu ağın internet çıkışı yoktur, yani lab'ın küçük bir kopyasıdır.

```bash
# PC‑1'de
nmcli device wifi hotspot ifname wlan0 ssid MOODLE-TEST password test12345
nmcli -g IP4.ADDRESS device show wlan0     # çıktı genelde 10.42.0.1/24
```

- Bu komut `wlan0`'ı hotspot'a çevirir; PC‑1'in Wi‑Fi üzerinden olan internet bağlantısı **kopar**. Bu istenen durumdur.
- **Dikkat:** PC‑1'e takılı bir **Ethernet kablosu** ya da USB internet varsa, NetworkManager hotspot'u o bağlantı üzerinden istemcilere **internet paylaşır** (NAT). Bu durumda PC‑2 ve telefon internete çıkar ve test geçersiz olur. Testten önce bu bağlantıları çıkarın veya kapatın (`nmcli device disconnect <arayüz>`).
- Geri almak için: `nmcli connection down Hotspot`.

### Seçenek 2: İnternetsiz router/switch
Bir router'ın internet (WAN) kablosunu takmadan, sunucu ve istemcileri ona bağlayın. Gerçek lab'a en çok benzeyen kurulumdur. Router DHCP verecekse sunucuya sabit IP ayarlamayı unutmayın.

### Seçenek 3: İnternetli ağda istemcinin çıkışını engellemek
Yalnızca ek donanım yoksa. Karmaşık ve hataya açıktır; kanıt A'yı güvenilir şekilde sağlamak zordur. Seçenek 1 daha güvenilirdir.

---

## 3. Sunucu (PC‑1) hazırlığı

### Neden `.env` değişmeli?
Moodle, kendi adresini `.env` içindeki `MOODLE_WWWROOT` değerinden öğrenir. Şu an değer `http://localhost:8080`. `localhost` "bu bilgisayarın kendisi" demektir; öğrenci cihazında `localhost` öğrencinin kendi bilgisayarına gider. Ayrıca Moodle giriş sonrası yönlendirmeleri bu adrese göre yapar. Adres yanlış kalırsa sayfa açılsa bile giriş sırasında `localhost`'a atar ve kopar.

```bash
cd ~/moodle-proje

# 1) Sunucunun IP'sini öğren (hotspot açıksa genelde 10.42.0.1)
ip -4 -br addr

# 2) .env içindeki adresi bu IP ile değiştir
sed -i 's|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://10.42.0.1:8080|' .env

# 3) Servisleri yeniden başlat
docker compose up -d

# 4) Güvenlik duvarında 8080 portunu aç (firewalld kullanılıyorsa)
sudo firewall-cmd --add-port=8080/tcp          # geçici, yeniden başlatınca silinir
```

**Beklenen:** `docker compose ps` komutunda `moodle`, `db` (healthy), `cron`, `jobe` hepsi **Up**. PC‑1'in kendi tarayıcısında `http://10.42.0.1:8080` açılır.

**Güvenlik duvarı hakkında:** Sunucuda güvenlik duvarı varsa 8080 kapalıyken **PC‑1 kendi kendine açar ama diğer cihazlar açamaz**. "Bende açılıyor, diğerinde açılmıyor" durumunun en yaygın nedeni budur.

---

## 3.1 İstemci cihazların hazırlanması ve kontrolü

Her cihazı teste başlamadan önce aşağıdaki sırayla kontrol edin ve sonuçları not alın.

| Cihaz | Rol | Ağa nasıl bağlı | İnternet durumu |
|---|---|---|---|
| PC‑1 | Sunucu (Docker) | Kendi hotspot'unu yayar (`10.42.0.1`) | Yok |
| PC‑2 | Öğrenci PC'si | `MOODLE-TEST` ağına Wi‑Fi ile bağlı | Yok olmalı |
| Telefon | Öğrenci cihazı | `MOODLE-TEST` ağına Wi‑Fi ile bağlı, **mobil veri kapalı** | Yok olmalı |

> PC‑2'de ikinci bir ağ bağlantısı (Ethernet, USB tethering, VPN) varsa kapatın. Yoksa internet o yoldan gelir ve test geçersiz olur.

### A) Telefon

**Hazırlık**
1. Ayarlar → **Mobil veri: Kapalı**. (Alternatif: Uçak modu açıp sonra yalnızca Wi‑Fi'ı açın.)
2. Wi‑Fi'dan `MOODLE-TEST` ağına bağlanın (şifre `test12345`).
3. Telefon "Bu ağda internet yok, yine de bağlı kalınsın mı?" diye sorarsa **Bağlı kal / Evet** deyin. Android bazen internet yok diye ağı otomatik bırakıp mobil veriye geçer. Bunu önlemek için mobil veriyi kapalı tutun ve varsa "Akıllı ağ geçişi / Wi‑Fi+" gibi seçenekleri kapatın.
4. Durum çubuğunda mobil veri simgesi **görünmemeli**.

**Kontrol**

| # | Yapılacak | Beklenen | Ne anlama gelir? |
|---|---|---|---|
| 1 | Tarayıcıda `https://www.google.com` aç | Açılmaz | Kanıt A: internet yok |
| 2 | Tarayıcıda `https://1.1.1.1` aç | Açılmaz | Kanıt A'yı güçlendirir (alan adı çözümü olmadan da internet yok) |
| 3 | Tarayıcıda `http://10.42.0.1:8080` aç | Moodle giriş sayfası | Kanıt B: sunucuya erişim var |
| 4 | Öğrenci hesabıyla giriş yap, kursu aç, sınavı başlat | Sorunsuz çalışır | Uçtan uca çalışıyor |

**Yorum:** 1 ve 2 başarısız **ve** 3 ve 4 başarılıysa telefon testi geçerlidir.
**Sorun giderme:**
- 3 açılmıyorsa telefonun aldığı IP'ye bakın (Wi‑Fi ayrıntıları). `10.42.0.x` olmalı.
- Adresi `https://` ile değil **`http://`** ile yazın. Moodle'ımız HTTPS kullanmıyor, `https` ile deneyince açılmaz.
- Hâlâ açılmıyorsa PC‑1'de güvenlik duvarını kontrol edin (Bölüm 3).

### B) PC‑2 (öğrenci PC'si)

**Hazırlık**
```bash
# Linux
nmcli device status        # yalnızca Wi‑Fi bağlı olmalı (MOODLE-TEST); Ethernet/VPN yok
ip -4 -br addr             # 10.42.0.x adresi almış olmalı
ip route                   # varsayılan çıkış 10.42.0.1 görünebilir; internet çıkışı olmadığı için işe yaramaz
```
Windows: `ipconfig` (IPv4 `10.42.0.x`), `route print`.

**Kontrol**

| # | Komut / işlem | Beklenen | Ne anlama gelir? |
|---|---|---|---|
| 1 | `ping -c 3 8.8.8.8` (Windows: `ping 8.8.8.8`) | %100 kayıp / zaman aşımı | A: internet yok |
| 2 | `nslookup google.com` (veya `getent hosts google.com`) | Çözümlenemez / hata | A: DNS de yok |
| 3 | `curl -I --max-time 5 https://www.google.com` | Hata, zaman aşımı | A: web erişimi yok |
| 4 | `ping -c 3 10.42.0.1` | Yanıt gelir | B: sunucu ağda görünüyor |
| 5 | `curl -I http://10.42.0.1:8080` | `HTTP/1.1 200` veya `303` | B: Moodle yanıt veriyor |
| 6 | Tarayıcıdan `http://10.42.0.1:8080`, giriş ve sınav akışı | Çalışır | Gerçek kullanım |
| 7 | F12 → Network sekmesi | Dış alan adına istek yok | T4 |

> **200 ve 303 ne demek?** 200 = sayfa geldi. 303 = Moodle başka bir sayfaya yönlendiriyor (ör. giriş sayfası). İkisi de normaldir. `Connection refused` ya da `timed out` ise sunucuya ulaşılamıyordur.

### C) PC‑1 (sunucu) – kendi kontrolü
```bash
ip -4 -br addr                      # wlan0 = 10.42.0.1/24
docker compose ps                   # 4 servis "Up", db "healthy"
curl -I http://10.42.0.1:8080       # 200/303
sudo firewall-cmd --list-ports      # 8080/tcp görünmeli
ping -c 2 8.8.8.8                   # yanıt gelmemeli (sunucu da internetsiz)
```
Sunucunun da internetsiz olduğunu doğrulamak önemlidir: internet varsa bir bağımlılığın dışarıdan çekilip test sonucunu gizlemesi mümkündür.

### D) Neden bu kadar kontrol? (özet)
Tek başına "Moodle açıldı" yetmez. Cihazda gizli bir internet yolu varsa sayfa yine açılır ve yanlış sonuç alırız. Önce **internetin yokluğu** (Google/ping başarısız), sonra **sunucuya erişim** (Moodle açılıyor) kanıtlanır. Mümkünse ekran görüntüsü alın: telefonda Google hatası + Moodle girişi, PC‑2'de `ping 8.8.8.8` hatası + `curl` 200 çıktısı.

---

## 4. Test senaryoları

Her testte: **ne yapılır**, **beklenen**, **başarısız olursa ne anlama gelir**.

### T1 – İstemcide internet YOK (kanıt A)
İstemci tarayıcısında `https://www.google.com` ve `https://1.1.1.1` açmayı deneyin; PC'de ayrıca `ping 8.8.8.8` ve `nslookup google.com`.
**Beklenen:** Hiçbiri çalışmaz.
**Başarısızsa:** Cihazın gizli bir internet yolu var. Mobil veri, ikinci Wi‑Fi/Ethernet, VPN, hotspot'un NAT'la internet paylaşması olabilir. Sonraki testler **geçersizdir**; önce bunu çözün.

### T2 – İstemci sunucuya ulaşıyor (kanıt B)
```bash
ping 10.42.0.1
curl -I http://10.42.0.1:8080
```
Telefonda tarayıcıdan `http://10.42.0.1:8080`.
**Beklenen:** Ping yanıt verir, `curl` 200/303 döner, telefonda giriş sayfası açılır.
**Başarısızsa:** Ağ farklı alt ağda, IP yanlış, ya da PC‑1'de 8080 portu kapalı.

### T3 – Moodle girişi ve sayfa yüklenmesi
Öğrenci hesabıyla giriş yapın, kursa girin, birkaç sayfa gezin.
**Beklenen:** Stil, simgeler ve fontlar tam yüklenir, hata mesajı yoktur.
**Başarısızsa:** Sayfa çıplak/bozuk görünüyorsa dışarıdan kaynak çekilmeye çalışılıyordur (T4'e bakın). Giriş sonrası adres `localhost` oluyorsa `.env` güncel değildir (Bölüm 3).

### T4 – Dış kaynak bağımlılığı
İstemci tarayıcısında **F12 → Network**, sayfayı yenileyin. Alan adı `10.42.0.1` dışında olan istekleri (Google Fonts, CDN, gravatar vb.) arayın.
**Beklenen:** Dış alan adına istek ya da kırmızı (başarısız) istek yok.
**Başarısızsa:** İstekleri listeleyin. Genellikle Moodle ayarından kapatılır (ör. gravatar, güncelleme bildirimi). Bu liste rapora eklenmelidir.

### T5 – CodeRunner + Jobe
Bir CodeRunner sorusu olan sınavda şu üç durumu deneyin: doğru kod, hatalı kod (söz dizimi hatası), sonsuz döngü.
**Beklenen:** Doğru kod geçer; hatalı kod anlaşılır bir hata verir; sonsuz döngü zaman aşımıyla kesilir. Jobe aynı sunucuda iç ağdan (`jobe` adıyla) çalıştığı için internet gerekmez.
**Başarısızsa:** `docker compose ps` ile `jobe` servisini kontrol edin; `docker compose restart jobe`. CodeRunner ayarlarında Jobe adresi `jobe` olmalı.

### T6 – Sınav akışı (baştan sona)
Giriş → sınavı başlat → cevap yaz/kaydet → sayfayı yenile → sınavı bitir. Hoca hesabında notun/denemenin göründüğünü doğrulayın.
**Beklenen:** Cevaplar kaybolmaz, yenilemede oturum düşmez, hocada deneme listelenir.

### T7 – Eşzamanlı yük
Lab kapasitesi kadar (örn. 30) öğrenci aynı anda sınava girip CodeRunner çalıştırsın. Gerçek cihaz yoksa birkaç cihazla çok sayıda sekme açıp aynı anda kod çalıştırın. Sunucuda izleyin:
```bash
docker stats
```
**Beklenen:** CPU/RAM sürekli %100'e dayanmaz; sayfa yanıtı birkaç saniyeyi geçmez; kod çalıştırma birkaç saniyede sonuç verir.
**Başarısızsa:** Sunucuya daha fazla RAM/CPU gerekir ya da Jobe eşzamanlı iş sınırı ayarlanmalı. Sonuçları (kaç kişi, kaç saniye) tabloya yazın.

### T8 – Sunucu dayanıklılığı
- PC‑1 uyku moduna geçiyor mu? (Güç ayarlarında kapatın ve 10–15 dk bekleyin.)
- Ağ bağlantısı kısa süre koptuktan sonra öğrenci oturumu devam ediyor mu?
- `docker compose restart` sonrası sistem kendiliğinden ayağa kalkıyor mu? Cevaplar korunuyor mu?
**Beklenen:** Uyku olmaz; kısa kopmadan sonra devam edilir; yeniden başlatma sonrası veri korunur.

### T9 – Güvenlik / yetki
- Öğrenci hesabı `http://10.42.0.1:8080/admin` sayfasına giremiyor mu?
- Varsayılan yönetici şifresi (`.env`'deki `ADMIN_PASS`) değiştirildi mi?
- `config.php` içinde `debugdisplay = 0` yapıldı mı? (Açıkken öğrenciye teknik hata mesajları görünür.)
**Beklenen:** Öğrenci yönetim sayfasına giremez; varsayılan şifre kalmamıştır; hata ayrıntıları gizlidir.

---

## 5. Sonuç tablosu (doldurulacak)

Cihaz sütununa testi hangi cihazla yaptığınızı yazın (Telefon / PC‑2 / PC‑1).

| # | Test | Cihaz | Beklenen | Sonuç | Not / ekran görüntüsü |
|---|---|---|---|---|---|
| T1 | İstemcide internet yok | | Google açılmaz | ☐ Geçti ☐ Kaldı | |
| T2 | Sunucuya erişim | | 200/303, giriş sayfası | ☐ Geçti ☐ Kaldı | |
| T3 | Giriş ve sayfa yükleme | | Tam yüklenir | ☐ Geçti ☐ Kaldı | |
| T4 | Dış kaynak yok | | Başarısız istek yok | ☐ Geçti ☐ Kaldı | |
| T5 | CodeRunner / Jobe | | Kod çalışır | ☐ Geçti ☐ Kaldı | |
| T6 | Sınav akışı | | Uçtan uca çalışır | ☐ Geçti ☐ Kaldı | |
| T7 | Eşzamanlı yük | | Takılma yok | ☐ Geçti ☐ Kaldı | |
| T8 | Dayanıklılık | | Toparlanır | ☐ Geçti ☐ Kaldı | |
| T9 | Güvenlik | | Yetkisiz erişim yok | ☐ Geçti ☐ Kaldı | |

### Genel değerlendirme
- [ ] Tüm testler geçti, lab günü için hazır.
- [ ] Bazı testler kaldı. Sorunlar ve çözüm planı: ______________________________________

**Test sonrası geri alma:** `.env` içindeki adresi `http://localhost:8080` yapıp `docker compose up -d` çalıştırın; hotspot için `nmcli connection down Hotspot`.

---

## 5.1 Ek test: Tailscale ile uzak erişim (isteğe bağlı)

> **Önemli sınırlama:** Tailscale giriş ve cihaz eşleştirmesi için internetli bir kontrol sunucusuna bağlanır. Bu nedenle **internetsiz lab senaryosunu doğrulamaz**. Telefon Tailscale ile bağlıysa cihazın interneti vardır ve kanıt A sağlanmaz. Bu test yalnızca "farklı ağdan erişim" ve geliştirme kolaylığı içindir. Ana test (Bölüm 2–4, hotspot) geçmeden lab hazır sayılmaz. Lab günü `.env`'de yerel IP kullanılır, Tailscale adresi kullanılmaz.

### Ne zaman işe yarar?
Ekipten biri aynı ağda değilken sunucuya bakmak ya da evden telefonla deneme yapmak için. Port yönlendirme veya ağ ayarı gerektirmez.

### Kurulum (hepsi internetli ortamda)

**PC‑1 (sunucu), Linux:**
```bash
sudo pacman -S tailscale             # veya: curl -fsSL https://tailscale.com/install.sh | sh
sudo systemctl enable --now tailscaled
sudo tailscale up
tailscale ip -4                      # 100.x.y.z adresi
```
**Telefon / PC‑2:** Tailscale uygulamasını kurun, **aynı hesapla** giriş yapın. Cihazlar yönetim panelinde (login.tailscale.com → Machines) görünmelidir.

### Moodle adresini ayarlama
```bash
sed -i 's|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://100.x.y.z:8080|' .env   # 100.x.y.z = sunucunun Tailscale IP'si
docker compose up -d
```
Gerekirse güvenlik duvarında: `sudo firewall-cmd --zone=trusted --add-interface=tailscale0`.

### Test senaryoları

| # | Test | Beklenen |
|---|---|---|
| TS1 | Telefonda mobil veri **açık**, Wi‑Fi kapalı, Tailscale açık. `http://100.x.y.z:8080` aç | Moodle girişi gelir (farklı ağdan erişim) |
| TS2 | Telefon Tailscale **kapalıyken** aynı adresi aç | Açılmaz (adres yalnızca Tailscale içinde geçerli) |
| TS3 | PC‑2'de `tailscale status` ve `tailscale ping <sunucu>` | Sunucu görünür, yanıt gelir (doğrudan mı, DERP üzerinden mi yazın) |
| TS4 | PC‑2'de `curl -I http://100.x.y.z:8080` | HTTP 200/303 |
| TS5 | Giriş + sınav + CodeRunner | Hotspot testiyle aynı sonuç |
| TS6 | Sunucu ve istemcilerde internet kesilince (hotspot'a geçince) Tailscale bağlantısı | Beklenen: kopar ya da kararsızlaşır. Bu, **lab için Tailscale'e güvenilmemesi gerektiğini** gösterir |

### Sonuç tablosu

| # | Test | Sonuç | Not |
|---|---|---|---|
| TS1 | Mobil veriyle erişim | ☐ Geçti ☐ Kaldı | |
| TS2 | Tailscale kapalıyken erişim yok | ☐ Geçti ☐ Kaldı | |
| TS3 | Cihazlar görünür / ping | ☐ Geçti ☐ Kaldı | |
| TS4 | curl 200/303 | ☐ Geçti ☐ Kaldı | |
| TS5 | Sınav akışı | ☐ Geçti ☐ Kaldı | |
| TS6 | İnternet kesilince davranış | ☐ Geçti ☐ Kaldı | |

### Tailscale testi sonrası geri alma
```bash
sudo tailscale down
sed -i 's|^MOODLE_WWWROOT=.*|MOODLE_WWWROOT=http://localhost:8080|' .env
docker compose up -d
```
Lab öncesi `.env` mutlaka lab IP'sine çevrilmeli (Bölüm 3).

---

## 6. Lab günü kontrol listesi

Hocanın yapacağı adımların ayrıntısı için: [HOCA_LAB_KILAVUZU.md](HOCA_LAB_KILAVUZU.md).

- [ ] Docker imajları sunucuda önceden indirilmiş (internetsiz `docker compose up` sorunsuz)
- [ ] Sunucu sabit IP'de, `.env` doğru IP ile güncel
- [ ] Güvenlik duvarında 8080 açık
- [ ] Veritabanı yedeği alındı
- [ ] Admin şifresi değiştirildi, debug kapalı
- [ ] Sunucu güç kablosuna bağlı, uyku modu kapalı
- [ ] Öğrenci hesapları ve sınav önceden hazırlandı
- [ ] Bir öğrenci PC'sinden son deneme yapıldı
