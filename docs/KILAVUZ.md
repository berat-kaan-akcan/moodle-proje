# MSKÜ DYS – Moodle + CodeRunner + Jobe
## Detaylı Kullanım Kılavuzu

| | |
|---|---|
| **Proje** | Moodle 4.5 LMS, CodeRunner soru türü, Jobe Sandbox, MSKÜ DYS teması (Docker Compose) |
| **Sürüm** | Moodle 4.5.x (build 2024100714), PHP 8.3, MariaDB 11.4 |
| **Hazırlayan** | Berat Kaan Akcan (beratkaanakcan@gmail.com) |
| **Tarih** | 8 Ekim 2026 |

> Bu belge projedeki tüm kılavuzları (eski KULLANIM_KILAVUZU, HOCA_LAB_KILAVUZU ve python-sinav kılavuzları) tek çatı altında toplar ve sıfırdan başlayan biri için baştan sona adım adım anlatır.

---

## İçindekiler

1. [Projeye genel bakış](#1-projeye-genel-bakış)
2. [Klasör ve dosya yapısı](#2-klasör-ve-dosya-yapısı)
3. [Kurulum](#3-kurulum)
4. [İlk giriş ve hesaplar](#4-ilk-giriş-ve-hesaplar)
5. [Rol mantığı](#5-rol-mantığı)
6. [Kullanıcı yönetimi](#6-kullanıcı-yönetimi)
7. [Kategori ve kurs yönetimi](#7-kategori-ve-kurs-yönetimi)
8. [Kursa kayıt (enrolment)](#8-kursa-kayıt-enrolment)
9. [CodeRunner ile kodlama sorusu hazırlama](#9-coderunner-ile-kodlama-sorusu-hazırlama)
10. [Hazır Python sınav havuzu](#10-hazır-python-sınav-havuzu)
11. [Soruları Moodle'a yükleme](#11-soruları-moodlea-yükleme)
12. [Sınav (Quiz) kurma](#12-sınav-quiz-kurma)
13. [Öğrenci kılavuzu](#13-öğrenci-kılavuzu)
14. [Lab günü: sınavı kendi bilgisayarınızdan yayınlama](#14-lab-günü-sınavı-kendi-bilgisayarınızdan-yayınlama)
15. [İnternetsiz ağ testi (hotspot)](#15-internetsiz-ağ-testi-hotspot)
16. [Sınav sırasında izleme ve müdahale](#16-sınav-sırasında-izleme-ve-müdahale)
17. [Sonuçlar, notlar ve istatistik](#17-sonuçlar-notlar-ve-istatistik)
18. [Yedekleme ve geri yükleme](#18-yedekleme-ve-geri-yükleme)
19. [Bakım komutları](#19-bakım-komutları)
20. [Güvenlik](#20-güvenlik)
21. [Sorun giderme](#21-sorun-giderme)
22. [Kontrol listeleri](#22-kontrol-listeleri)
23. [Sözlük ve hızlı başvuru](#23-sözlük-ve-hızlı-başvuru)

---

## 1. Projeye genel bakış

Bu proje, programlama derslerinde **otomatik değerlendirmeli kod sınavı** yapabilmek için hazırlanmış, Docker tabanlı bir eğitim platformudur.

### Ne işe yarar?

- Öğrenci tarayıcıda Python (veya C, Java vb.) kodu yazar.
- **Kontrol et** düğmesine basınca kod, izole bir kutuda (Jobe) çalıştırılır.
- Çıktı, hocanın tanımladığı test senaryolarıyla karşılaştırılır ve **anında not** verilir.
- Hoca tek bir bilgisayarda tüm sistemi çalıştırıp, internet olmayan bir laboratuvarda sınav yapabilir.

### Bileşenler

| Servis | Görev | Erişim |
|---|---|---|
| **moodle** | Web arayüzü, kurslar, sınavlar (Apache + PHP 8.3 + Moodle 4.5) | Dışarıya açık, port **8080** |
| **db** | MariaDB 11.4 veritabanı (kullanıcılar, sorular, cevaplar) | Yalnızca iç ağ |
| **cron** | Moodle zamanlanmış görevlerini her 60 sn'de bir çalıştırır | Yalnızca iç ağ |
| **jobe** | Öğrenci kodunu güvenle çalıştıran sandbox (`trampgeek/jobeinabox`) | Yalnızca iç ağ, `jobe` adıyla |

### Mimari şema

```
 Öğrenci tarayıcısı ──► [ moodle :8080 ] ──► [ db ]  (MariaDB)
                              │
                              └──► [ jobe ]  (kodu çalıştırır, sonucu döner)
                       [ cron ]  (arka plan görevleri)
```

Öğrenci bilgisayarlarına **hiçbir şey kurulmaz**; yalnızca tarayıcı yeterlidir.

### Projeyle gelenler

- Hazır **Moodle 4.5** kurulumu ve **CodeRunner** eklentisi
- **MSKÜ DYS** temalı giriş sayfası (yerel ağda çalışması için Roboto ve FontAwesome yazı tipleri çevrimdışı dahil edilmiştir)
- Veritabanı dökümü (`init-db/moodle.sql`): hazır kurs, kullanıcılar ve ayarlar
- **34 soruluk Python sınav havuzu**, 6 aşama, 4 final paketi
- Lab günü ve ağ testi dokümanları

---

## 2. Klasör ve dosya yapısı

```
moodle-proje/
├── docker-compose.yml        Servis tanımları (db, moodle, cron, jobe)
├── .env                      Ayarlar: port, adres, veritabanı bilgileri
├── config.php                Moodle yapılandırması (.env değerlerini okur)
├── init-db/moodle.sql        İlk kurulumda otomatik yüklenen veritabanı dökümü
├── moodledata_filedir.tar.gz Moodle dosya deposu yedeği
├── moodle/                   Moodle kaynak kodu (eklentiler, tema dahil)
├── python-sinav/             Python sınav havuzu (sorular, üretici, XML, cevap anahtarı)
│   ├── sorular.py            Tüm soruların tanımı
│   ├── uret.py               Doğrular ve XML + cevap anahtarı üretir
│   ├── ice.php               XML'i terminalden içe aktaran betik
│   ├── CEVAP_ANAHTARI.md     Çözümler (SADECE HOCA)
│   ├── YOL_HARITASI.md       Sınav kurulum adımları
│   ├── SORU_YAZIM_KILAVUZU.md
│   └── cikti/*.xml           Moodle'a yüklenecek soru dosyaları
├── hotspot-test.sh           Wi-Fi hotspot açıp erişim testi yapan betik
├── README.md                 Kısa kurulum özeti
├── KULLANIM_KILAVUZU.md      Yönetim kılavuzu
├── HOCA_LAB_KILAVUZU.md      Lab günü kılavuzu
├── LAB_TEST_RAPORU.md        Lab ortamı test planı
└── DETAYLI_KULLANIM_KILAVUZU.md  Bu belge
```

### `.env` dosyası

| Değişken | Anlamı | Örnek |
|---|---|---|
| `MOODLE_PORT` | Dışarıya açılan port | `8080` |
| `MOODLE_WWWROOT` | Sitenin tam adresi. **Öğrencilerin yazdığı adresle aynı olmalı** | `http://localhost:8080` |
| `DB_ROOT_PASSWORD`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Veritabanı bilgileri | |
| `ADMIN_USER`, `ADMIN_PASS`, `ADMIN_EMAIL` | Yönetici bilgileri | |

> `.env` dosyası şifre içerir. Başkalarıyla paylaşmayın.

---

## 3. Kurulum

### 3.1 Ön gereksinimler

| İşletim sistemi | Gerekli |
|---|---|
| Windows / macOS | [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulu ve açık |
| Linux | `docker` ve `docker-compose-plugin` |

Önerilen donanım: en az 4 GB boş RAM, 10 GB disk. Lab sınavı için 4 çekirdek ve 8 GB RAM rahat eder.

### 3.2 Projeyi alma

```bash
git clone https://github.com/berat-kaan-akcan/moodle-proje.git
cd moodle-proje
```

### 3.3 Başlatma

```bash
docker compose up -d
```

İlk çalıştırmada imajlar indirilir ve `init-db/moodle.sql` otomatik yüklenir (1–2 dakika).

### 3.4 Durumu kontrol etme

```bash
docker compose ps
```

`db`, `moodle`, `cron`, `jobe` servislerinin dördü de **Up** olmalıdır (`db` ve `jobe` için *healthy*).

### 3.5 Tarayıcıdan açma

`http://localhost:8080` adresini açın. MSKÜ DYS giriş sayfası gelir.

> **Önemli:** İnternetli ortamda ilk kez çalıştırın. İmajlar bir kez inmelidir. İnternetsiz lab'a bu şekilde hazır gidilir.

---

## 4. İlk giriş ve hesaplar

### Hazır hesaplar

| Rol | Kullanıcı adı | E-posta | Şifre |
|---|---|---|---|
| Yönetici | `admin` | beratkaanakcan@gmail.com | `Admin.1234!` |
| Öğrenci | `dogukan` | dd@mu.edu.tr | `Admin.1234!` (değişmiş olabilir) |

- Kullanıcı adı yerine **e-posta ile de giriş** yapılabilir.
- **Gerçek bir sınav öncesi yönetici şifresini mutlaka değiştirin** (bkz. [20. Güvenlik](#20-güvenlik)).

### Hazır kurs

- Ad: **programing**, kısa ad: **se1001** (kurs id: 2)
- Python sınav havuzu bu kursun soru bankasında yüklüdür.

### Şifre unutulursa

```bash
docker compose exec moodle php /var/www/html/admin/cli/reset_password.php
```

Komut kullanıcı adını ve yeni şifreyi sorar.

---

## 5. Rol mantığı

Moodle'da iki ayrı işlem vardır:

1. **Kullanıcı oluşturma:** Kişi sisteme hesap olarak eklenir.
2. **Kursa kayıt:** Kişi bir kursa **bir rolle** eklenir.

| Rol | CSV kodu | Yapabildikleri |
|---|---|---|
| **Yönetici (Admin)** | – | Tüm site |
| **Öğretmen** | `editingteacher` | İçerik ekler, sınav ve soru hazırlar, not verir |
| **Düzenleyemeyen öğretmen (asistan)** | `teacher` | İçeriği değiştiremez, değerlendirir, not verir |
| **Öğrenci** | `student` | İçeriği görür, sınava girer |
| **Yönetici (kurs düzeyi)** | `manager` | Kurs düzeyinde yönetim |

---

## 6. Kullanıcı yönetimi

### 6.1 Tek tek kullanıcı ekleme

1. Yönetici olarak giriş yapın.
2. **Site yönetimi → Kullanıcılar → Hesaplar → Yeni bir kullanıcı ekle**
3. Alanlar:

| Alan | Açıklama |
|---|---|
| Kullanıcı adı | Küçük harf (örn. `ahmet.yilmaz` veya `20240101`) |
| Yeni şifre | Kalem simgesine tıklayıp yazın. Karmaşıklık kuralı vardır (büyük/küçük harf, rakam, sembol) |
| Ad, Soyad | Zorunlu |
| E-posta | Geçerli biçimde olmalı |
| İlk girişte şifre değiştir | İsterseniz işaretleyin |

4. **Kullanıcı oluştur**.

### 6.2 CSV ile toplu yükleme

**Site yönetimi → Kullanıcılar → Hesaplar → Kullanıcıları yükle**

UTF-8 kodlamalı `ogrenciler.csv`:

```csv
username,password,firstname,lastname,email,course1,role1
2024001,Sifre.1234!,Ali,Demir,ali.demir@mu.edu.tr,se1001,student
2024002,Sifre.1234!,Ayse,Kaya,ayse.kaya@mu.edu.tr,se1001,student
mehmet.hoca,Hoca.1234!,Mehmet,Yildiz,mehmet.yildiz@mu.edu.tr,se1001,editingteacher
```

- `course1`: kursun **kısa adı**, `role1`: rol kodu. Kullanıcı oluşturulurken aynı anda kursa atanır.
- Dosyayı sürükleyin, **Kullanıcıları yükle** deyin. Önizlemede alanları kontrol edip onaylayın.
- Türkçe karakterler bozuluyorsa dosyayı **UTF-8** olarak kaydedin.

### 6.3 Kullanıcıyı düzenleme, askıya alma, silme

**Site yönetimi → Kullanıcılar → Hesaplar → Kullanıcıları göz at.** Satırdaki simgelerle düzenleme, askıya alma, silme yapılır. Sınav verisi olan kullanıcıyı silmek yerine **askıya almak** daha güvenlidir.

---

## 7. Kategori ve kurs yönetimi

### 7.1 Kategori

**Site yönetimi → Kurslar → Kursları ve kategorileri yönet → Yeni kategori oluştur.** Örnek yapı: *Mühendislik Fakültesi → Bilgisayar Mühendisliği → 1. Sınıf*.

### 7.2 Yeni kurs

**Site yönetimi → Kurslar → Yeni bir kurs ekle.**

| Alan | Açıklama |
|---|---|
| Kurs tam adı | örn. `Programlamaya Giriş (Python)` |
| Kurs kısa adı | Benzersiz kod, örn. `SE1001`. CSV yüklemede bu kullanılır |
| Kategori | Kursun ait olduğu kategori |
| Başlangıç / bitiş tarihi | Dönem |
| Kurs biçimi | *Konular* (önerilen) veya *Haftalık* |

**Kaydet ve göster** ile bitirin.

### 7.3 Kursta düzenleme

Kurs sayfasında sağ üstteki **Düzenleme modunu aç** anahtarı ile bölüm ekleyebilir, etkinlik/kaynak ekleyebilir, sıralamayı değiştirebilirsiniz.

---

## 8. Kursa kayıt (enrolment)

### Yöntem 1: Elle kayıt (hoca veya yönetici)

1. Kurs → **Katılımcılar → Kullanıcıları kaydet**
2. **Rol ata:** Öğrenci / Öğretmen / Düzenleyemeyen öğretmen
3. Arama kutusuna ad veya kullanıcı adı yazıp seçin.
4. **Kayıtlı kullanıcıları seçin** ile tamamlayın.

### Yöntem 2: Kendi kendine kayıt (anahtar ile)

1. Kurs → **Katılımcılar** → üstteki açılır menüden **Kayıt yöntemleri**
2. **Kendi kendine kayıt (Öğrenci)** satırında göz simgesiyle yöntemi **etkinleştirin**.
3. Çark simgesi → **Kayıt anahtarı** girin (örn. `Python2024!`), varsayılan rol **Öğrenci**.
4. Değişiklikleri kaydedin. Öğrenci kursu bulup anahtarı girerek kendisi kaydolur.

### Yöntem 3: CSV ile (bkz. 6.2)

### Gruplar (paket dağıtımı için)

**Katılımcılar → Gruplar → Grup oluştur.** Final sınavında A, B, C, D paketlerini farklı gruplara vermek için kullanılır (bkz. [12.5](#125-paketleri-gruplara-dağıtma)).

---

## 9. CodeRunner ile kodlama sorusu hazırlama

### 9.1 Soru türünü seçme

CodeRunner'da dil olarak `python3` seçilir. İki biçim vardır:

| | **Program** (`stdin → stdout`) | **Fonksiyon / sınıf** |
|---|---|---|
| Öğrenci ne yazar? | `input()` ile okuyup `print()` eden tam program | Yalnızca `def f(...)` veya `class ...` |
| Test girdisi | **Standard input** alanında | **Test** alanında (`print(f(3))`) |
| Ne zaman? | Girdi/çıktı, döngü, biçimlendirme | Fonksiyon, koleksiyon, OOP |

Kural: "Klavyeden oku" diyorsanız **program**, "`f(x)` fonksiyonunu yazın" diyorsanız **fonksiyon**.

### 9.2 Moodle bu testi nasıl çalıştırır?

```
[öğrencinin kodu]
[test kodu]          ← fonksiyon sorularında; program sorularında boş
```

Bu dosya Jobe'da çalıştırılır. **stdout, beklenen çıktıyla satır satır karşılaştırılır** (satır sonu boşlukları yok sayılır).

### 9.3 Arayüzden soru oluşturma (adım adım)

1. Kurs → **Daha fazla → Soru bankası** → kategoriyi seçin → **Yeni soru oluştur**.
2. **CodeRunner** → **Ekle**.
3. Alanları doldurun:

| Alan | Yazılacak |
|---|---|
| Question type | `python3` |
| Question name | `s3_asal - Asal mı?` |
| Question text | Öğrenciye görünen açıklama |
| Default mark | örn. 10 |
| Penalty regime | `10, 20, ...` (her yanlış denemede %10, %20… kesinti) |
| Answer box lines | 18 |

4. **Customisation** bölümünü kapalı bırakın.
5. **Test cases:**
   - *Fonksiyon sorusu:* Test = `print(asal_mi(7))`, Expected = `True`
   - *Program sorusu:* Test boş, Standard input = `3` ve `4` (ayrı satırlar), Expected = `7`
   - **Show**: öğrenci görür, **Hide**: gizli test. **Use as example**: soru sayfasında örnek olarak da gösterir.
   - Daha fazla test için **Add another test case**.
6. **Sample answer** kutusuna doğru çözümü yazın.
7. **Kaydet**, ardından **Önizle** ile önce doğru, sonra hatalı çözüm deneyin.

### 9.4 Altın kurallar

- İlk **1–2 test görünür**, kalanı **gizli** olsun. Aksi halde `if n == 7: return True` gibi hileler geçer.
- Her soruya **en az 5 test** koyun: tipik, sınır (0, 1), negatif, özel yapı, hile engeli.
- Çıktı biçimini soruda açık yazın ("iki ondalık basamakla").
- Küme/sözlük çıktısı sırasızdır; sıra gerekiyorsa soruda belirtin.
- Kayan nokta eşitliği yerine `round()` veya `.2f` kullanın.
- Program sorularında boş satır testi koymayın (boş stdin EOF hatası verir).
- Jobe ~5 sn zaman sınırıyla çalışır.

### 9.5 Tipik hata ve onu yakalayan test

| Tipik hata | Yakalayan test |
|---|---|
| `range(1, n)` (son dahil değil) | küçük `n` (1, 5) |
| `>` yerine `>=` | sınır değer (örn. 89/90) |
| Büyük/küçük harf duyarlılığı | `"Aa"` gibi karışık |
| Girdi listesini değiştirmek | testte listeyi yazdırın |
| Boş koleksiyonda çökme | `[]`, `""`, `{}` |

### 9.6 Toplu üretim: `sorular.py`

Çok soru için en güvenli yol [python-sinav/sorular.py](python-sinav/sorular.py) dosyasıdır. Beklenen çıktıları siz yazmazsınız; referans çözüm çalıştırılarak otomatik üretilir.

**Fonksiyon sorusu örneği:**

```python
q(id="s3_toplam", asama=3, baslik="1'den n'e toplam", tur="fonksiyon",
  metin="`toplam(n)` fonksiyonu 1'den n'e kadar olan sayıların toplamını döndürsün. `n < 1` ise `0`.",
  cozum="def toplam(n):\n    t = 0\n    for i in range(1, n + 1):\n        t += i\n    return t\n",
  testler=[f"print(toplam({n}))" for n in (1, 5, 10, 100, 0, -3, 1000)],
  yanlislar=["def toplam(n):\n    t=0\n    for i in range(1,n):\n        t+=i\n    return t\n"])
```

**Program sorusu örneği:**

```python
q(id="s1_topla", asama=1, baslik="İki sayının toplamı", tur="program",
  metin="Klavyeden iki tam sayı (ayrı satırlarda) okuyun ve toplamlarını yazdırın.",
  cozum="a = int(input())\nb = int(input())\nprint(a + b)\n",
  testler=["3\n4\n", "-5\n5\n", "0\n0\n", "1000000\n2345678\n"],
  yanlislar=["a=int(input())\nb=int(input())\nprint(a-b)\n"])
```

- `yanlislar`: bilerek hatalı çözümler. Test seti bunları yakalamak zorundadır.

**Üretme ve doğrulama:**

```bash
cd python-sinav
python3 uret.py                   # doğrula + XML ve cevap anahtarı üret
python3 uret.py --sadece-dogrula  # yalnızca kontrol
```

Doğrulayıcı şunları denetler: referans çözüm tüm testlerde çalışıyor mu, en az 5 test ve 2 farklı çıktı var mı, **her hatalı çözüm en az bir testte yakalanıyor mu**, final paketleri tam 100 puan mı.

### 9.7 Tuzaklar

1. Aynı XML'i iki kez yüklemek soruları çoğaltır.
2. Kategori adında `/` kullanmayın (alt kategoriye bölünür).
3. Kod ve çok satırlı metinleri XML'de `<![CDATA[ ... ]]>` içine alın.
4. `sorted()` gibi yöntem yasaklarını CodeRunner kendiliğinden denetlemez; yalnızca çıktıya bakar.

---

## 10. Hazır Python sınav havuzu

**34 soru · 235 test · 6 aşama · 4 final paketi.** Tüm referans çözümler gerçek CodeRunner/Jobe hattında tam not almıştır. Cevaplar için [python-sinav/CEVAP_ANAHTARI.md](python-sinav/CEVAP_ANAHTARI.md) (**öğrenciyle paylaşmayın**).

| Aşama | Konu | Sorular |
|---|---|---|
| 1 | Temeller: girdi, çıktı, aritmetik | topla, ortalama, daire, saniye, bolme |
| 2 | Koşullar (if-elif-else) | ciftmi, artikyil, harf, ucgen, enbuyuk |
| 3 | Döngüler (for-while) | toplam, faktoriyel, asal, fizzbuzz, basamak, ucgen_yildiz |
| 4 | Fonksiyonlar ve string | palindrom, sesli, kelime, sezar, anagram |
| 5 | Liste, sözlük, küme, matris | ikinci, tekrarsiz, frekans, matris, notlar, toplam_ikili |
| 6 | Özyineleme, istisna, OOP, algoritma | fibonacci, guvenli_bol, banka, satir_say, ikili_arama, siralama, parantez |

Her soru 10 puandır (final paketlerinde ağırlıklar farklıdır).

### Final paketleri (her biri 100 puan)

| Paket | Aşama 1 | Aşama 2 | Aşama 3 | Aşama 4 | Aşama 5 | Aşama 6 |
|---|---|---|---|---|---|---|
| **A** | ortalama (10) | harf (15) | asal (15) | palindrom (15) | frekans (20) | banka (25) |
| **B** | saniye | ucgen | fizzbuzz | sezar | tekrarsiz | parantez |
| **C** | bolme | artikyil | basamak | anagram | toplam_ikili | guvenli_bol |
| **D** | daire | enbuyuk | faktoriyel | kelime | notlar | ikili_arama |

Komşu öğrencilere farklı paket vererek kopyayı zorlaştırabilirsiniz.

### Soru bankasındaki ağaç

```
Python Sinav
 ├─ Asama 1 - Temeller: girdi, çıktı, aritmetik   (5 soru)
 ├─ Asama 2 - Koşullar (if-elif-else)             (5)
 ├─ Asama 3 - Döngüler (for-while)                (6)
 ├─ Asama 4 - Fonksiyonlar ve string işlemleri    (5)
 ├─ Asama 5 - Liste, sözlük, küme, matris         (6)
 ├─ Asama 6 - Özyineleme, istisna, OOP, ...       (7)
 └─ Final - Paket A / B / C / D                   (6'şar)
```

### Dosyalar

| Dosya | Ne için |
|---|---|
| `cikti/asama1.xml` … `asama6.xml` | Aşama aşama soru dosyaları |
| `cikti/tum_havuz.xml` | 34 sorunun tamamı |
| `cikti/final_paket_A.xml` … `D.xml` | Final paketleri |

---

## 11. Soruları Moodle'a yükleme

> **Şu anki durum:** `programing` kursunda `Python Sinav` kategorisi altında 34 soru ve 4 paket **zaten yüklüdür**. Bu bölümü yeni bir kursa/Moodle'a kurarken kullanın.

### 11.1 Arayüzden (önerilen)

1. Kurs → **Daha fazla → Soru bankası**
2. **İçe aktar (Import)** sekmesi
3. Dosya biçimi: **Moodle XML format**
4. *Kategoriyi dosyadan al:* ✔ işaretli, *Bağlamı dosyadan al:* boş
5. `tum_havuz.xml` dosyasını sürükleyin → **İçe aktar** → **Devam**

Aşama aşama açmak isterseniz her seferinde tek dosya yükleyin (`asama1.xml`, sonra `asama2.xml`…).

### 11.2 Terminalden

```bash
docker cp python-sinav/ice.php moodle-proje-moodle-1:/tmp/
docker cp python-sinav/cikti/tum_havuz.xml moodle-proje-moodle-1:/tmp/
docker exec moodle-proje-moodle-1 php /tmp/ice.php /tmp/tum_havuz.xml 2   # 2 = kurs id
```

### 11.3 Doğrulama

Soru bankasında yukarıdaki kategori ağacı görünmeli, önizlemede soru metinleri düzgün olmalıdır.

> **Aynı dosyayı iki kez içe aktarmayın.** Gerekirse önce `Python Sinav` kategorisini silin (Soru bankası → Kategoriler).

### 11.4 Bir soruyu elle deneme

1. Soru bankasında `Asama 1` kategorisini seçin → `s1_topla` satırında **⋮ → Önizle**
2. Şunu yazın:
   ```python
   a = int(input())
   b = int(input())
   print(a + b)
   ```
3. **Kontrol et** → tüm satırlar yeşil ✔ olmalı.
4. Bilerek `print(a - b)` yazın → kırmızı ✘ ve beklenen/alınan fark görünmeli.
5. `while True: pass` yazın → birkaç saniye sonra **zaman aşımı** gelmeli, sunucu donmamalı.

Beklenen: doğru çözüm tam not, yanlış çözüm kırmızı, sonsuz döngü zaman aşımı.

---

## 12. Sınav (Quiz) kurma

### 12.1 Pratik sınavı (aşama bazlı)

1. Kurs → **Düzenlemeyi aç** → **Bir etkinlik ya da kaynak ekle → Sınav**
2. Ad: `Aşama 1 – Temeller (pratik)`
3. Önerilen ayarlar:

| Ayar | Değer | Neden |
|---|---|---|
| Zaman sınırı | kapalı (veya 40 dk) | Rahat denesin |
| Deneme sayısı | sınırsız | Tekrar çalışsın |
| Not yöntemi | En yüksek not | |
| Soru davranışı | **Uyarlamalı mod** | Soru başına birçok kez "Kontrol et" |
| Gözden geçirme | Deneme sırasında ve sonrasında doğru/yanlış ve geri bildirim açık | Öğrenme amaçlı |
| Soru düzeni | Her soru yeni sayfada | Tek ekran |

4. **Kaydet ve göster** → **Sınavı düzenle**
5. **Ekle → + Soru bankasından** → kategori `Python Sinav / Asama 1` → soruları işaretleyin → **Seçili soruları sınava ekle**
6. **Maksimum not** değerini 100 yapın, kaydedin.

Diğer aşamalar için **Sınav → ⋮ → Çoğalt** ile kopyalayıp kategoriyi değiştirmek hızlıdır.

### 12.2 Final sınavı

Gerçek sınav ayarları pratikten farklıdır:

| Ayar | Değer |
|---|---|
| Aç / kapa | Sınav günü ve saati |
| **Zaman sınırı** | 90 dakika |
| Zaman dolunca | **Açık denemeler otomatik gönderilir** |
| Deneme sayısı | **1** |
| Soru davranışı | *Ertelenmiş geri bildirim* (çözerken not görünmez) veya *Uyarlamalı* |
| Gözden geçirme | Sonra: **not** görünür, doğru cevap **gizli** |
| Soru düzeni | Tek sayfa veya 1 soru/sayfa, gezinme serbest |
| Ek kısıtlar | **Şifre** (sınav anında söylenir), gerekirse **IP adresi kısıtı** (lab alt ağı) |
| Tarayıcı güvenliği | *Tam ekran açılır pencere* (Safe Exam Browser yoksa) |

Soruları `Final - Paket A` kategorisinden ekleyin; puanlar (10/15/15/15/20/25) hazır gelir, **Maksimum not = 100**.

### 12.3 Test öğrenci hesapları

Prova için gerçek öğrenci kullanmayın:

| Kullanıcı | Senaryo |
|---|---|
| `test_guclu` | Her soruyu doğru çözer |
| `test_orta` | Sınır durumlarını kaçırır |
| `test_sorunlu` | Hatalı ve sonsuz döngülü kod gönderir |
| `test_yuk` | Aynı anda çok sekme |

```csv
username,password,firstname,lastname,email,course1,role1
test_guclu,Test1234!,Güçlü,Test,guclu@example.com,se1001,student
test_orta,Test1234!,Orta,Test,orta@example.com,se1001,student
test_sorunlu,Test1234!,Sorunlu,Test,sorunlu@example.com,se1001,student
test_yuk,Test1234!,Yük,Test,yuk@example.com,se1001,student
```

### 12.4 Beklenen prova sonuçları

| Hesap | Yapılacak | Beklenen |
|---|---|---|
| `test_guclu` | Referans çözümler | %100 |
| `test_orta` | `s2_harf` için `>` kullan | Gizli testlerde ✘, kısmi puan |
| `test_sorunlu` | Sonsuz döngü, `import os; os.system("ls")`, syntax hatası, boş cevap | Hata mesajı gelir, sistem ayakta kalır |
| `test_yuk` | 5–10 sekmede aynı anda **Kontrol et** | Her biri ~10 sn altında yanıtlanır |

### 12.5 Paketleri gruplara dağıtma

- **Kolay yol:** Her paket için ayrı **Grup** oluşturun (Katılımcılar → Gruplar). Her sınavın **Erişimi kısıtla** ayarında "Grup = Paket A" seçin. Öğrenci yalnızca kendi paketini görür.
- **Basit yol:** Küçük sınıfta tek sınav, tek paket (A).

Doğrulama: `test_guclu` hesabını Paket A grubuna ekleyin; yalnızca Paket A görünmeli.

---

## 13. Öğrenci kılavuzu

*Bu bölümü öğrencilere dağıtabilirsiniz.*

### Giriş

1. Tarayıcıyı açın (Chrome, Firefox, Edge).
2. Hocanın tahtaya yazdığı adresi **adres çubuğuna** yazın (örn. `http://192.168.1.25:8080`). Arama kutusuna değil.
3. Kullanıcı adınızı (veya e-postanızı) ve şifrenizi girin.
4. Kurs listesinden dersi açın, gerekirse hocanın verdiği **kayıt anahtarını** girin.

### Sınava girme

1. Kursta sınavın adına tıklayın, **Denemeyi başlat**'a basın. Şifre istenirse hoca söyleyecektir.
2. Soruyu okuyun. Altta kod kutusu vardır; **kodu buraya yazın**.
3. **Kontrol et** düğmesi kodunuzu çalıştırır ve test sonuçlarını gösterir:
   - ✔ yeşil: test geçti
   - ✘ kırmızı: test geçmedi (beklenen ve alınan çıktı yan yana görünür)
4. Sorular arasında sağdaki **Sınav gezinmesi** kutusundan geçebilirsiniz.
5. Bitirince **Denemeyi bitir → Tümünü gönder ve bitir**.

### Önemli ipuçları

- **Program sorularında** `input()` ile oku, `print()` ile yazdır.
- **Fonksiyon sorularında** yalnızca istenen `def` bloğunu yazın; `input()` veya kendi test çağrılarınızı eklemeyin.
- Çıktı biçimine dikkat edin: boşluk, noktalama, ondalık basamak sayısı sonucu etkiler.
- Bazı testler **gizlidir**; yalnızca örnek testleri geçmek yetmez, genel çözüm yazın.
- Cevaplar otomatik kaydedilir. Sayfa takılırsa **yenileyin (F5)**; cevaplar kaybolmaz.
- Süre dolunca denemeniz otomatik gönderilir.
- Uyarlamalı modda her yanlış denemede küçük bir puan kesintisi olabilir (ceza rejimi).

---

## 14. Lab günü: sınavı kendi bilgisayarınızdan yayınlama

Öğrenciler internete bağlanmaz; yalnızca sizin bilgisayarınızdaki Moodle adresini açar.

```
[Sizin PC: Moodle + Veritabanı + Jobe] ── lab ağı (internetsiz) ── [Öğrenci PC'leri]
```

### 14.1 Sınavdan önce (evde/ofiste, internetli)

1. Kurs, öğrenci listesi ve soruları hazırlayın.
2. **Sistemi bir kez internetle çalıştırın** (`docker compose up -d`). Docker imajları inmiş olmalı; lab'da internet yok.
3. **Deneme sınavı** yapın (öğrenci hesabıyla giriş, soru çözme, bitirme).
4. **Yönetici şifresini değiştirin.**
5. **Yedek alın** (bkz. [18](#18-yedekleme-ve-geri-yükleme)).
6. **Güç ayarları:** uyku, ekran kilidi ve otomatik güncellemeyi kapatın; şarj cihazını alın.

### 14.2 Lab'a gelince (sınavdan ~20 dk önce)

**Adım 1 – Ağa bağlanın.** Ağ kablosunu lab switch'ine takın veya lab Wi-Fi'ına bağlanın.

**Adım 2 – IP adresinizi öğrenin.**

```bash
ip -4 -br addr
```

Lab ağındaki arayüzün adresini not edin (örn. `192.168.1.25`). Bu sizin sunucu adresinizdir; öğrenci bilgisayarları aynı bloktan (`192.168.1.xxx`) olmalıdır.

**Adım 3 – Moodle adresini güncelleyin.** `.env` içinde:

```
MOODLE_WWWROOT=http://192.168.1.25:8080
```

Sonra:

```bash
docker compose up -d
```

> Bu adım atlanırsa giriş yapınca adres `localhost`'a döner ve öğrenci bağlanamaz.

**Adım 4 – Güvenlik duvarında 8080'i açın.**

```bash
sudo firewall-cmd --add-port=8080/tcp
```

**Adım 5 – Önce kendiniz deneyin.** Kendi tarayıcınızda `http://192.168.1.25:8080` açın; sonra bir öğrenci bilgisayarından aynı adresi deneyin.

**Adım 6 – Adresi duyurun.** Tahtaya adresi yazın. Öğrenciler adres çubuğuna aynen yazar.

### 14.3 Zaman çizelgesi

| Zaman | İş |
|---|---|
| T−30 dk | `docker compose ps`; IP ve `MOODLE_WWWROOT` doğru; kendi hesabınızla giriş |
| T−10 dk | Öğrenciler giriş yapar, sınav sayfası hazır |
| T−0 | Sınav açılır, şifre söylenir |
| Sınav sırasında | `docker stats`; takılan öğrenciye yardım |
| T+90 | Otomatik gönderim; ayar değiştirmeyin |

### 14.4 Sınav sırasında yapılmayacaklar

- Bilgisayarı **kapatmayın, uyutmayın, ağ kablosunu çıkarmayın**.
- Laptop kapağını kapatmayın (kapak ayarı "bir şey yapma" olsun).
- Yeni ayar veya güncelleme yapmayın.

### 14.5 Sınav sonrası

1. Notları görün ve dışa aktarın (bkz. [17](#17-sonuçlar-notlar-ve-istatistik)).
2. Yedek alın.
3. Kapatmak isterseniz `docker compose stop` (veriler silinmez).
4. Normal kullanıma dönmek için `.env`'i `http://localhost:8080` yapıp `docker compose up -d` çalıştırın.

> **`docker compose down -v` komutunu çalıştırmayın.** Tüm verileri (sınav, öğrenci, cevap) siler.

---

## 15. İnternetsiz ağ testi (hotspot)

Lab günü sürpriz yaşamamak için laboratuvarı küçük ölçekte taklit edin. **Telefonla girip çalışması yeterli kanıt değildir**; iki kanıt birlikte gerekir:

| Kanıt | Soru | Nasıl doğrulanır |
|---|---|---|
| **A** | İstemcinin interneti gerçekten yok mu? | `google.com` açılmıyor, `ping 8.8.8.8` yanıt vermiyor |
| **B** | İstemci yine de Moodle'a erişebiliyor mu? | `http://SUNUCU_IP:8080` açılıyor |

Önce A, sonra B doğrulanır. Gizli internet yolları: mobil veri, ikinci Wi-Fi, Ethernet, USB paylaşım, VPN, Tailscale.

### 15.1 Test ağı kurma

**Seçenek 1 (önerilen): sunucu PC kendi hotspot'unu yayar**

```bash
nmcli device wifi hotspot ifname wlan0 ssid MOODLE-TEST password test12345
nmcli -g IP4.ADDRESS device show wlan0     # genelde 10.42.0.1/24
```

- Bu komut PC'nin Wi-Fi üzerindeki internet bağlantısını koparır; istenen durumdur.
- PC'ye takılı Ethernet/USB internet varsa istemcilere internet paylaşılır ve test geçersiz olur. Önce bunları çıkarın (`nmcli device disconnect <arayüz>`).
- Geri almak için: `nmcli connection down Hotspot`.

**Seçenek 2:** WAN kablosu takılmamış bir router'a sunucu ve istemcileri bağlayın. Sunucuya sabit IP verin.

### 15.2 Hazır betik

[hotspot-test.sh](hotspot-test.sh) tek komutla şunları yapar: hotspot'u açar, `.env`'deki adresi `10.42.0.1` yapar, servisleri başlatır, güvenlik duvarı durumunu yazar, 180 saniye boyunca gelen ping/8080 paketlerini sayar ve sonucu `hotspot-log.txt`'ye kaydeder.

```bash
sudo bash ~/moodle-proje/hotspot-test.sh
```

Çalışırken arkadaşınız/diğer cihaz **MOODLE-TEST** ağına bağlanıp (mobil veri kapalı) sırayla `http://10.42.0.1:8091` (basit test sunucusu) ve `http://10.42.0.1:8080` (Moodle) adreslerini açar. Log'a bakarak paketlerin ulaşıp ulaşmadığını görürsünüz.

> Betik `.env` dosyasını değiştirir. Test bitince adresi geri alın.

### 15.3 Test senaryoları özeti

| # | Test | Beklenen |
|---|---|---|
| T1 | İstemcide internet yok (kanıt A) | Google açılmaz, ping yanıtsız |
| T2 | İstemci sunucuya ulaşır (kanıt B) | Moodle açılır |
| T3 | Giriş ve sayfa yüklenmesi | Giriş yapılır, sayfa bozuk değil |
| T4 | Dış kaynak bağımlılığı | Font/ikon/stil internetsiz de yüklenir |
| T5 | CodeRunner + Jobe | Kod çalışır, not gelir |
| T6 | Sınav akışı baştan sona | Başla → çöz → bitir → not |
| T7 | Eşzamanlı yük | Lab kapasitesi kadar öğrenci rahat çalışır |
| T8 | Sunucu dayanıklılığı | Yeniden başlatmada veri kaybı olmaz |
| T9 | Güvenlik / yetki | Öğrenci yönetici sayfalarına giremez |

Sonuçları [LAB_TEST_RAPORU.md](LAB_TEST_RAPORU.md) içindeki tabloya işleyin. Hepsi **Geçti** olmadan lab gününe çıkmayın.

### 15.4 Tailscale (isteğe bağlı)

Uzaktan erişim gerekirse sunucuya ve istemciye Tailscale kurup `MOODLE_WWWROOT`'u Tailscale IP'siyle ayarlayabilirsiniz. Ayrıntı: LAB_TEST_RAPORU.md §5.1. Test sonrası `.env`'i geri alın.

---

## 16. Sınav sırasında izleme ve müdahale

| İhtiyaç | Nasıl |
|---|---|
| Girenleri izlemek | Sınav sayfasında **Devam eden denemeler**; Kurs → Katılımcılar |
| Ek süre / özel hak | Sınav → **Kullanıcı geçersiz kılmaları (Overrides)** |
| Takılan öğrenci | Sayfayı yenilemesini söyleyin; olmazsa başka PC'den aynı hesapla devam edebilir |
| Sunucu durumu | `docker compose ps` (4 servis Up) |
| Yavaşlama | `docker stats` ile CPU/RAM'e bakın |
| Hızlı yeniden başlatma | `docker compose restart` (cevaplar veritabanında kalır) |

---

## 17. Sonuçlar, notlar ve istatistik

1. Sınav → **Sonuçlar → Notlar**: öğrenci bazlı notlar; tek tek deneme açıp kodları görebilirsiniz.
2. **Dışa aktar:** Kurs → **Notlar → Dışa aktar** (CSV/Excel) ya da Sonuçlar sayfasından indirme.
3. **İstatistik:** Sınav → Sonuçlar → İstatistik.
   - Soru ortalaması **%30 altı**: soru veya test hatalı/aşırı zor olabilir.
   - Soru ortalaması **%95 üstü**: fazla kolay.
4. Soruda en çok başarısız olan **gizli test** hangisi? Eksik sınır durumunun işaretidir.
5. Düzeltme gerekiyorsa `sorular.py`'yi değiştirin, `python3 uret.py` ile yeniden üretin; eski kategoriyi silip yeni XML'i içe aktarın.

---

## 18. Yedekleme ve geri yükleme

Sistemin verisi iki yerdedir: **veritabanı** ve **moodledata** (yüklenen dosyalar).

### 18.1 Veritabanı yedeği

```bash
docker compose exec -T db sh -c 'mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' > init-db/moodle.sql
```

Bu dosya yeni bir kurulumda otomatik yüklenir. Komutu çalıştırmadan önce mevcut dosyanın kopyasını alın.

### 18.2 moodledata yedeği

```bash
docker compose exec -T moodle tar czf - -C /var/www/moodledata filedir > moodledata_filedir.tar.gz
```

### 18.3 Moodle içinden kurs yedeği

Kurs → **Daha fazla → Yedekleme**. Tek kursu taşımak için uygundur; **Geri yükle** ile başka sisteme alınır.

### 18.4 Geri yükleme (yeni makine)

1. Projeyi klonlayın, `docker compose up -d` (SQL otomatik yüklenir).
2. Dosya deposunu açın:
   ```bash
   docker compose cp moodledata_filedir.tar.gz moodle:/tmp/
   docker compose exec moodle sh -c 'tar xzf /tmp/moodledata_filedir.tar.gz -C /var/www/moodledata && chown -R www-data:www-data /var/www/moodledata'
   ```
3. Önbelleği temizleyin (bkz. 19).

> `init-db/` yalnızca **boş** veritabanında çalışır. Var olan kurulumun üzerine yüklemek için önce hacmi silmek gerekir (`docker compose down -v`, **bütün veriyi siler**, yalnızca yedeğiniz varsa).

---

## 19. Bakım komutları

Hepsi proje klasöründe çalıştırılır.

| İş | Komut |
|---|---|
| Başlat | `docker compose up -d` |
| Durum | `docker compose ps` |
| Durdur (veri kalır) | `docker compose stop` |
| Yeniden başlat | `docker compose restart` |
| Tek servisi yeniden başlat | `docker compose restart jobe` |
| Kapat (konteynerleri kaldırır, veri kalır) | `docker compose down` |
| Log izle | `docker compose logs -f moodle` |
| Kaynak kullanımı | `docker stats` |
| Önbelleği temizle | `docker compose exec -T moodle php /var/www/html/admin/cli/purge_caches.php` |
| Cron'u elle çalıştır | `docker compose exec -T moodle php /var/www/html/admin/cli/cron.php` |
| Şifre sıfırla | `docker compose exec moodle php /var/www/html/admin/cli/reset_password.php` |

**Tehlikeli:** `docker compose down -v` veritabanı ve moodledata hacimlerini siler.

### Port değiştirme

`.env` içinde `MOODLE_PORT` ve `MOODLE_WWWROOT` portunu birlikte değiştirin, sonra `docker compose up -d`.

---

## 20. Güvenlik

- **Yönetici şifresini değiştirin** (Site yönetimi → Kullanıcılar → Hesaplar → admin → düzenle). Varsayılan şifre repoda yazılıdır.
- **Veritabanı şifrelerini** `.env` içinde değiştirin; `.env` dosyasını paylaşmayın.
- **Jobe dışarıya açık değildir**; yalnızca Moodle iç ağdan erişir. Port açmayın.
- Öğrenci kodu Jobe sandbox'ında çalışır: `import os; os.system(...)` denemeleri sistemi etkilememelidir. Prova sırasında `test_sorunlu` ile bunu doğrulayın.
- **Cevap anahtarını** (`CEVAP_ANAHTARI.md`) ve `python-sinav/` klasörünü öğrenciyle paylaşmayın.
- Sınavda **şifre**, **tek deneme** ve **IP kısıtı** kullanın.
- Güvenlik duvarında yalnızca gerekli portu (8080) açın; sınav sonrası kapatın:
  ```bash
  sudo firewall-cmd --remove-port=8080/tcp
  ```
- Moodle ve imaj güncellemelerini sınav haftasında yapmayın; ayrı bir bakım günü seçin.

---

## 21. Sorun giderme

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Öğrenci sayfayı hiç açamıyor | Farklı ağ veya güvenlik duvarı | IP bloğunu ve 8080'i kontrol edin; öğrenci PC'sinden `ping SUNUCU_IP` |
| Bir öğrenci açıyor, diğeri açamıyor | O PC'nin ağ kablosu/IP'si | O PC'nin ağını kontrol edin |
| Giriş yapınca adres `localhost` oluyor | `.env` güncellenmemiş | `MOODLE_WWWROOT`'u düzeltip `docker compose up -d` |
| Sayfa bozuk görünüyor (font/ikon yok) | Dış kaynak bekleniyor | Çevrimdışı font/CSS dahildir; önbelleği temizleyin |
| Sayfa çok yavaş | Yoğunluk | `docker stats`; sayfayı yenileyin |
| "Kontrol et" hata veriyor / sonuç gelmiyor | Jobe çalışmıyor | `docker compose ps`; `docker compose restart jobe` |
| "Jobe server error / unreachable" | Jobe sağlıksız | Aynı; Site yönetimi → Eklentiler → Soru türleri → CodeRunner'da sandbox'ın Jobe ve sunucunun `jobe` olduğunu doğrulayın |
| Tüm testlerde "Run error" | Program sorusunda `input()` yerine fonksiyon yazılmış (veya tersi) | Soru türünü ve öğrenci kodunu kontrol edin |
| Boş girdi testi hep patlıyor | Boş stdin EOF verir | Program sorularında boş girdi testi koymayın |
| Sorular çift görünüyor | XML iki kez yüklenmiş | `Python Sinav` kategorisini silip bir kez yükleyin |
| İçe aktarma "tanınmayan biçim" | Biçim yanlış | *Moodle XML* seçili mi, dosya `cikti/` içinden mi |
| Süre dolunca cevap kayboldu | Otomatik gönderim kapalı | "Açık denemeler otomatik gönderilir" ayarını açın |
| Her şey durdu | Konteynerler düşmüş | `docker compose up -d` (veri korunur) |
| Giriş şifresi hatalı | Yanlış hesap/şifre | `reset_password.php` ile sıfırlayın |
| Port 8080 dolu | Başka program kullanıyor | `.env`'de `MOODLE_PORT` ve `MOODLE_WWWROOT` değiştirin |
| Değişiklik ekranda görünmüyor | Önbellek | `purge_caches.php` |

---

## 22. Kontrol listeleri

### Kurulum sonrası

- [ ] `docker compose ps` dört servis Up
- [ ] `http://localhost:8080` açılıyor, admin ile giriş yapıldı
- [ ] Soru bankasında `Python Sinav` ağacı var
- [ ] Bir soru önizlemede doğru çözümle tam not verdi

### Sınav öncesi (evde)

- [ ] Docker imajları indirildi, deneme sınavı yapıldı
- [ ] Yönetici şifresi değiştirildi
- [ ] Yedek alındı (veritabanı + moodledata)
- [ ] Sınav ayarları: süre, tek deneme, otomatik gönderim, şifre
- [ ] Öğrenciler kursa kayıtlı, paketler gruplara atandı
- [ ] Uyku modu kapalı, şarj bağlı

### Lab günü

- [ ] Lab ağına bağlanıldı, IP öğrenildi
- [ ] `.env` yeni IP ile güncellendi, `docker compose up -d` yapıldı
- [ ] 8080 portu açıldı
- [ ] Bir öğrenci PC'sinden giriş denendi
- [ ] Kod sorusu çalıştırıldı (Jobe çalışıyor)
- [ ] Adres tahtaya yazıldı

### Sınav sonrası

- [ ] Notlar dışa aktarıldı
- [ ] Yedek alındı
- [ ] Port kapatıldı, `.env` eski haline getirildi
- [ ] `docker compose stop` (kapatılacaksa)

---

## 23. Sözlük ve hızlı başvuru

| Terim | Anlamı |
|---|---|
| **Moodle** | Açık kaynak öğrenme yönetim sistemi (LMS) |
| **CodeRunner** | Moodle'a kod yazma/test etme sorusu ekleyen eklenti |
| **Jobe** | Kodu izole çalıştıran sandbox sunucusu |
| **Soru bankası** | Soruların kurs içinde kategoriler halinde saklandığı yer |
| **Sınav (Quiz)** | Soru bankasından soru seçip öğrenciye sunan etkinlik |
| **Deneme (attempt)** | Öğrencinin sınavı bir kez çözmesi |
| **Ceza rejimi** | Her yanlış denemede puandan kesinti |
| **Stdin / Stdout** | Programın girdisi (klavye) / çıktısı (ekran) |
| **Gizli test** | Öğrencinin görmediği ama nota katılan test |
| **Override** | Tek öğrenciye özel süre/deneme hakkı |
| **Enrolment key** | Derse kendi kendine kayıt şifresi |

### Tek bakışta en sık kullanılan işler

| İş | Nerede / komut |
|---|---|
| Sistemi aç | `docker compose up -d` |
| Admin paneli | Site yönetimi (üst menü) |
| Kullanıcı ekle | Site yönetimi → Kullanıcılar → Hesaplar |
| Toplu kullanıcı | Site yönetimi → Kullanıcılar → Hesaplar → Kullanıcıları yükle |
| Kursa kayıt | Kurs → Katılımcılar → Kullanıcıları kaydet |
| Soru ekle | Kurs → Daha fazla → Soru bankası |
| Soru içe aktar | Soru bankası → İçe aktar → Moodle XML |
| Sınav oluştur | Kurs → Düzenlemeyi aç → Etkinlik ekle → Sınav |
| Ek süre | Sınav → Kullanıcı geçersiz kılmaları |
| Notları indir | Kurs → Notlar → Dışa aktar |
| Jobe sorunu | `docker compose restart jobe` |
| Hızlı yeniden başlat | `docker compose restart` |

**İletişim:** Berat Kaan Akcan, beratkaanakcan@gmail.com
