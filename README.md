# Moodle Sınav Sistemi (Moodle + CodeRunner + Jobe)

Muğla Sıtkı Koçman Üniversitesi DYS görünümlü giriş sayfasına sahip, Docker ile çalışan bir Moodle 4.5 kurulumu. CodeRunner soruları öğrenci kodunu izole Jobe sunucusunda otomatik değerlendirir. Sistem internetsiz lab ağında sınav yapmak için hazırlanmıştır.

Dersler, sınavlar, sorular, hesaplar ve Türkçe dil paketi projeyle birlikte gelir.

## İçindekiler

1. [Kurulum](#1-kurulum)
2. [Hesaplar](#2-hesaplar)
3. [Dersler ve sınavlar](#3-dersler-ve-sınavlar)
4. [Lab sınavı](#4-lab-sınavı)
5. [Yük testi](#5-yük-testi)
6. [Yardımcı betikler](#6-yardımcı-betikler)
7. [Yönetim komutları](#7-yönetim-komutları)
8. [Proje yapısı](#8-proje-yapısı)

## 1. Kurulum

Gereken tek şey Docker'dır: Windows ve Mac için [Docker Desktop](https://www.docker.com/products/docker-desktop/), Linux için `docker` ve `docker-compose-plugin`. İlk kurulum imajları indirdiği için internet ister.

Komutları proje klasöründe çalıştırın:

```bash
# 1) Projeyi alın (klasör elinizdeyse bu adımı atlayıp klasöre girin)
git clone https://github.com/berat-kaan-akcan/moodle-proje.git
cd moodle-proje

# 2) Sistemi başlatın. Veritabanı ilk açılışta otomatik yüklenir.
docker compose up -d

# 3) Yüklenen dosyaları ve Türkçe dil paketini geri yükleyin (yalnızca ilk kurulumda)
docker compose cp moodledata_filedir.tar.gz moodle:/tmp/
docker compose exec moodle sh -c "tar xzf /tmp/moodledata_filedir.tar.gz -C /var/www/moodledata && chown -R www-data:www-data /var/www/moodledata && rm /tmp/moodledata_filedir.tar.gz"

# 4) Önbelleği temizleyin
docker compose exec -u www-data moodle php /var/www/html/admin/cli/purge_caches.php
```

Sonra tarayıcıda **http://localhost:8080** adresini açın ve [Hesaplar](#2-hesaplar) bölümündeki bir hesapla giriş yapın.

`docker compose ps` çıktısında `db`, `moodle`, `cron` ve `jobe` servisleri çalışır görünmelidir.

8080 portu doluysa `.env` içindeki `MOODLE_PORT` ve `MOODLE_WWWROOT` değerlerini değiştirip `docker compose up -d` çalıştırın.

## 2. Hesaplar

| Rol | Kullanıcı adı | Şifre |
|---|---|---|
| Yönetici | `admin` | `Admin.1234!` |
| Öğretmen | `ogretmen_test1` | `Test1234*` |
| Öğrenci | `dogukan` | `Dd.123456` |
| Öğrenci | `ogrenci_test1` | `Test1234*` |
| Öğrenci | `ogrenci_test2` | `Test1234*` |

Bu şifreler herkese açıktır. Gerçek sınavdan önce en azından `admin` şifresini arayüzden değiştirin.

## 3. Dersler ve sınavlar

| Ders | Kısa ad | Sınav | Soru sayısı | Sınav adresi |
|---|---|---|---|---|
| programing | `se1001` | python deneme | 3 | `/mod/quiz/view.php?id=2` |
| programing_2 | `se102` | sınav | 4 | `/mod/quiz/view.php?id=4` |

Kayıtlar:

- `se1001`: `dogukan`, `ogrenci_test1`, `ogrenci_test2` öğrenci; `admin`, `ogretmen_test1` öğretmen
- `se102`: `ogrenci_test1` öğrenci; `admin`, `ogretmen_test1` öğretmen

## 4. Lab sınavı

Laptop sunucu olur, lab PC'leri yalnızca tarayıcıyla bağlanır. Lab PC'lerinde hiçbir dosya çalıştırılmaz. Adımların yazdırılabilir hali: [Lab_Sinavi_Baglanti_Adimlari.pdf](Lab_Sinavi_Baglanti_Adimlari.pdf). 16 Ekim 2026'da labda denendi, 37 PC IP aldı.

**Tahtaya yazılacak adres: `http://192.168.50.1:8080`**

Sunucu laptopunda Linux, NetworkManager (`nmcli`) ve `dnsmasq` gerekir. Aşağıdaki komutlardaki `eno1` laptopun kablolu ağ arayüzüdür. Sizde adı farklıysa `ip -br link` ile bulun, kendi adını yazın ve `lab_hazirla.sh` komutuna da argüman olarak verin.

### Lab ağı nasıl çalışıyor?

| Durum | Ne oluyor |
|---|---|
| Normal gün (uplink takılı) | Switch okul ağına bağlı. PC'ler adresi okulun DHCP sunucusundan (10.2.2.7) alır: 172.16.41.x. İnternet vardır. |
| Sınav (uplink çıkarılmış) | Okulun DHCP'si yok. Laptop 192.168.50.1 olur ve paylaşım modunda (dnsmasq) PC'lere 192.168.50.x dağıtır. İnternet yoktur. |
| Lab PC'leri | Otomatik (DHCP) ayarında. Adresi kim dağıtırsa ondan alırlar, PC'lerde ayar değiştirilmez. |

> **Altın kural:** Laptopta paylaşım modu (192.168.50.1) yalnızca switch'in okul kablosu çıkarıldıktan sonra açılır. Uplink takılıyken açılırsa okul ağına sahte DHCP dağıtılır ve başka cihazların bağlantısı bozulur.

### Adım 0: Önceden (internet varken)

- [Kurulumu](#1-kurulum) tamamlayın, imajlar yerelde olsun.
- `which dnsmasq` ile dnsmasq'ı kontrol edin. Kurulu değilse PC'lere IP dağıtılamaz.
- Moodle admin şifresini arayüzden değiştirin.
- Şarj aleti ve switch'e yetecek ethernet kablosu alın. Sınav hazır, öğrenci hesapları yüklü olsun.

### Adım 1: Kablolama

- Laptopun ethernet girişini (`eno1`) switch'e bağlayın. Bir lab PC'sinin kablosunu kullanabilirsiniz, öbür ucu zaten switch'tedir.
- Switch'ten duvara veya başka dolaba giden **okul (uplink) kablosunu çıkarın**.

### Adım 2: Uplink gerçekten çıktı mı? (laptopta)

```bash
nmcli radio wifi off
nmcli device connect eno1
ip -4 -br addr show eno1
```

| Görülen | Anlamı |
|---|---|
| 172.16.41.x adresi geldi | **DURUN.** Okul ağı hâlâ bağlı, yanlış kablo çıkmış olabilir. Devam etmeyin. |
| Adres gelmedi veya komut bekleyip hata verdi | Doğru. Uplink çıkmış, devam edin. |

### Adım 3: Laptopu sunucu yapın

```bash
nmcli device disconnect eno1
bash test/lab_hazirla.sh
```

Betik sudo şifresini sorar (güvenlik duvarı adımı). Çıktıda şunlar olmalı:

- `yöntem: shared` ve `IP: 192.168.50.1`
- `Sunucuda internet yok.` ("internet VAR" yazıyorsa Wi-Fi açık ya da uplink takılı)
- Sunucu kontrolünde servisler, adres, güvenlik duvarı ve Jobe maddeleri **GEÇTİ**

Betik ayrıca veritabanını `cikti/` klasörüne yedekler ve 8 saat uyku engeli koyar. **Fişi takılı tutun, kapağı kapatmayın.**

### Adım 4: Lab PC'leri

- **Kapalı PC'ler:** Normal açın. Adresi laptoptan kendileri alır.
- **Açık PC'ler:** Ağ simgesinden kablolu bağlantıyı kapatıp açın, kabloyu çıkarıp takın ya da yeniden başlatın.
- Tarayıcıya `http://192.168.50.1:8080` yazılır (başında `http://` olsun).

### Adım 5: Doğrulama

a) Kaç PC adres aldı? (laptopta)

```bash
ip neigh show dev eno1
ip neigh show dev eno1 | wc -l
```

b) Hepsi laptopa ulaşıyor mu? (laptopta, fish'te de çalışır)

```bash
bash -c 'ok=0; no=0
for ip in $(ip neigh show dev eno1 | awk "{print \$1}"); do
  if ping -c1 -W1 $ip >/dev/null 2>&1; then ok=$((ok+1))
  else no=$((no+1)); echo "yanıt yok: $ip"; fi
done
echo "yanıt veren: $ok  yanıt vermeyen: $no"'
```

c) İnternet gerçekten kesik mi? Laptopta `ping -c2 8.8.8.8` yanıt **vermemeli**. Bir lab PC'sinde `google.com` **açılmamalı**, Moodle adresi açılmalı.

d) Hangi PC'ler sayfayı açtı? (girenlerin IP listesi)

```bash
docker compose logs --since 30m moodle | grep -oE '192\.168\.50\.[0-9]+' | sort -uV
```

e) Kod çalıştırma: Öğretmen hesabıyla sınavı açın, bir CodeRunner sorusunda **Kontrol et**'e basın. Bu Jobe'u dener ve önbelleği ısıtır.

f) İsteğe bağlı: [yük testi](#5-yük-testi).

### Wi-Fi uyarısı

Paylaşım modu, laptopun internetini lab PC'lerine dağıtır. **Laptopta Wi-Fi (eduroam) açıksa lab PC'lerinde de internet olur.** Sınav boyunca Wi-Fi kapalı kalmalı: `nmcli radio wifi off`. Kapattığınız anda PC'lerin interneti kesilir, Moodle bağlantısı etkilenmez, yeniden başlatma gerekmez. Telefonu USB ile laptopa bağlamayın. Yalnızca eduroam bağlantısını kesmek yetmez, laptop kendiliğinden yeniden bağlanabilir. Radyoyu kapatın.

### Sorun giderme

| Belirti | Çözüm |
|---|---|
| Betik "NO-CARRIER" diyor | Kablo veya port sorunu. Başka port deneyin. `cat /sys/class/net/eno1/carrier` çıktısı `1` olmalı. |
| Betik 172.16.41.x adresini kullandı | Uplink takılı ya da `disconnect` atlandı. Uplink'i çıkarın, adım 2 ve 3'ü tekrarlayın. |
| PC adres almıyor | Laptopta `nmcli connection show --active` içinde `lab` olmalı. PC'de kabloyu çıkarıp takın ya da yeniden başlatın. |
| Ping gidiyor, sayfa açılmıyor | `docker compose ps` ile servislere bakın. Betiği yeniden çalıştırın (güvenlik duvarını açar). Tarayıcıda proxy varsa "Proxy yok" seçin. |
| Sayfa localhost'a veya eski IP'ye gidiyor | `grep WWWROOT .env` sonucu `http://192.168.50.1:8080` olmalı. Betiği yeniden çalıştırın. |
| PC'lerde internet var | Laptopta `nmcli radio wifi off`. Uplink kablosunu kontrol edin. |
| Kodlar "server overload" diyor | Jobe yoğun. Bekleme süresi 180 sn, kısa sürede düzelir. |
| Herkes düştü | Laptop uyudu ya da kapak kapandı. Fiş takılı, kapak açık kalmalı. |

### Bitince: geri alma

```bash
# 1) Sonuçları yedekleyin
mkdir -p cikti
docker compose exec -T db sh -c 'mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" --single-transaction "$MARIADB_DATABASE"' | gzip > cikti/sinav-sonrasi.sql.gz

# 2) Adres localhost'a döner, lab bağlantısı silinir, 8080 kapanır, uyku engeli kalkar, Wi-Fi açılır
bash test/lab_hazirla.sh --geri
```

- Switch'in okul (uplink) kablosunu geri takın.
- Laptopa aldığınız lab PC kablosunu kendi PC'sine geri takın.
- Lab PC'lerinde bağlantıyı kapatıp açın ya da yeniden başlatın: okulun DHCP'sinden yeniden 172.16.41.x alırlar.

### Kısa kontrol listesi

- [ ] Uplink çıkarıldı, laptop switch'e bağlı, fiş takılı
- [ ] `nmcli device connect eno1` sonucunda 172.16.41.x **gelmedi**
- [ ] `nmcli device disconnect eno1` ve `bash test/lab_hazirla.sh`: shared, 192.168.50.1, internet yok
- [ ] Wi-Fi kapalı (`nmcli radio wifi off`)
- [ ] PC'ler açıldı, `ip neigh` sayısı PC sayısına yakın, ping hepsine gidiyor
- [ ] Bir PC'de Moodle açılıyor, `google.com` açılmıyor, CodeRunner **Kontrol et** çalışıyor
- [ ] Adres tahtada: `http://192.168.50.1:8080`
- [ ] Bitince: yedek, `--geri`, uplink ve kablolar yerine

## 5. Yük testi

Sahte öğrenciler aynı anda giriş yapar, sınavı başlatır, her soruda **Kontrol et**'e basar ve teslim eder. Python 3 dışında bir şey gerekmez.

```bash
python3 test/sinav_yuk_testi.py hazirla 40 4   # yuk01..yuk40 hesaplarını oluşturur; 4 = sınav adresindeki id
python3 test/sinav_yuk_testi.py calistir       # testi çalıştırır, adresi .env'den alır
python3 test/sinav_yuk_testi.py temizle        # hesapları ve denemelerini siler
```

**Gerçek sınavdan önce `temizle` şarttır.** Sınavda şifre ya da tek deneme hakkı varsa betik sınavı başlatamaz, bu yüzden yük testini bu ayarlardan önce yapın.

`test/yuk_testi.py` ise giriş sayfasına ve Jobe'a doğrudan eşzamanlı istek gönderir:

```bash
python3 test/yuk_testi.py sayfa http://localhost:8080 50
```

Hesap oluşturan yardımcı dosya `test/yuk_hesaplari.php`'dir ve doğrudan çalıştırılmaz.

## 6. Yardımcı betikler

| Betik | Ne yapar |
|---|---|
| `test/lab_hazirla.sh` | Laptopu lab ağına hazırlar, `--geri` ile geri alır |
| `test/sunucu_kontrol.sh` | Servisleri, adresi, güvenlik duvarını ve Jobe'u denetler |
| `test/istemci_hazirla.sh`, `test/istemci_kontrol.sh`, `test/istemci_kontrol.ps1` | Yalnızca sorun çıkarsa: bir lab PC'sinde ağı ve erişimi denetler (Linux/Windows). DHCP alamayan Linux PC'ye sabit IP verir |
| `scripts/sifre_uret.py` | Öğrenci listesinden Moodle yükleme CSV'si ve şifre dağıtım listesi üretir |
| `scripts/sinav_dok.php` | Sınav denemelerini JSON olarak döker (salt okunur) |

## 7. Yönetim komutları

| İş | Komut |
|---|---|
| Durum | `docker compose ps` |
| Durdur (veri kalır) | `docker compose stop` |
| Yeniden başlat | `docker compose start` |
| Kaldır (veri kalır) | `docker compose down` |
| Önbelleği temizle | `docker compose exec -u www-data moodle php /var/www/html/admin/cli/purge_caches.php` |
| Cron'u elle çalıştır | `docker compose exec -u www-data moodle php /var/www/html/admin/cli/cron.php` |

> `docker compose down -v` **bütün veriyi siler**. Sıfırdan başlamak için kullanılır; ardından [kurulum](#1-kurulum) adımlarını yeniden uygulayın.

Projedeki başlangıç verisini güncel haliyle değiştirmek için:

```bash
docker compose exec -T db sh -c 'mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" --single-transaction --default-character-set=utf8mb4 "$MARIADB_DATABASE"' > init-db/moodle.sql
docker compose exec -T moodle tar czf - -C /var/www/moodledata filedir lang > moodledata_filedir.tar.gz
```

## 8. Proje yapısı

| Yol | İçerik |
|---|---|
| `docker-compose.yml` | Servisler: `moodle` (PHP 8.3), `db` (MariaDB 11.4), `cron`, `jobe` |
| `.env` | Port, Moodle adresi ve veritabanı bilgileri |
| `config.php` | Moodle yapılandırması, değerleri `.env`'den okur |
| `init-db/moodle.sql` | Başlangıç veritabanı, boş veritabanına otomatik yüklenir |
| `moodledata_filedir.tar.gz` | Yüklenen dosyalar ve Türkçe dil paketi |
| `moodle/` | Moodle kaynak kodu, CodeRunner ve DYS giriş sayfası (`login/index_auth.php`) |
| `test/` | Lab hazırlığı, kontrol ve yük testi betikleri |
| `scripts/` | Öğrenci ve sınav sonucu yardımcıları |
| `cikti/` | Betik çıktıları ve yedekler. Gerektiğinde oluşur, Git'e girmez |
