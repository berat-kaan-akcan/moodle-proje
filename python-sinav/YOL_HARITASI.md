# Python Sınavı Kurulum Yol Haritası

Bu belge, soruları Moodle'a **nasıl kuracağınızı** adım adım anlatır. Her adımın sonunda "✔ Doğrula" kutusu vardır. Doğrulama geçmeden sonraki adıma geçmeyin.

```
Adım 0  Sistemi kontrol et
Adım 1  Soruları Moodle'a yükle (XML içe aktarma)
Adım 2  Bir soruyu elle dene (önizleme)
Adım 3  Aşama bazlı pratik sınavları kur (1–6)
Adım 4  Test öğrenci hesapları ve kayıt
Adım 5  Aşamaları öğrenci gözüyle dene
Adım 6  Final sınavını kur (Paket A–D)
Adım 7  Gerçek sınav provası
Adım 8  Sonuçları incele, havuzu düzelt
```

**Elinizdeki hazır malzeme** (`python-sinav/` klasörü):

| Dosya | Ne için |
|---|---|
| `cikti/asama1.xml` … `asama6.xml` | Aşama aşama soru dosyaları (Adım 1, 3) |
| `cikti/tum_havuz.xml` | 34 sorunun hepsi tek dosyada |
| `cikti/final_paket_A.xml` … `D.xml` | Final sınav paketleri (Adım 6) |
| `CEVAP_ANAHTARI.md` | Çözümler ve test case'ler. **Öğrenciyle paylaşmayın** |
| `sorular.py` + `uret.py` | Soruları değiştirmek/genişletmek için |
| `SORU_YAZIM_KILAVUZU.md` | **Soru nasıl yazılır:** soru türü seçimi, test case'ler, XML alanları |
| `ice.php` | XML'i terminalden içe aktaran betik (isteğe bağlı) |

> **Şu anki durum:** `programing` kursunun (id 2) soru bankasında `Python Sinav` kategorisi altında 34 soru + 4 final paketi **zaten yüklü**. Adım 1'i, yeni bir kurs veya yeni bir Moodle'a kurarken ya da yeniden yüklerken kullanın. Şimdilik Adım 0'dan sonra doğrudan Adım 2'ye geçebilirsiniz.

---

## Adım 0 — Sistemi kontrol et

```bash
cd ~/moodle-proje
docker compose up -d
docker compose ps          # moodle, db, cron, jobe: dördü de "Up"
```

Tarayıcıda `http://localhost:8080` → yönetici olarak giriş.

**Jobe (kod çalıştırıcı) hızlı testi:** Site yönetimi → Eklentiler → Soru türleri → CodeRunner → varsayılan sandbox **Jobe**, sunucu adresi docker ağındaki `jobe` olmalı. (Zaten kurulu. Bozulduysa Adım 2'de hata verir.)

✔ **Doğrula:** `docker compose ps` çıktısında dört servis çalışıyor, Moodle'a giriş yapabiliyorsunuz.

---

## Adım 1 — Soruları Moodle'a yükle

### 1a. Tek dosya ile (hızlı yol)

1. Kursu açın → üstteki menüden **Daha fazla ▾ → Soru bankası**.
2. Sekmeyi **Import** (İçe aktar) yapın.
3. Dosya biçimi: **Moodle XML format**.
4. **Genel** bölümünde:
   * *Kategoriyi dosyadan al:* ✔ işaretli (kategoriler otomatik açılır)
   * *Bağlamı dosyadan al:* ✘ boş
5. **Import** kutusuna `tum_havuz.xml` dosyasını sürükleyin → **Import** düğmesi → sonraki sayfada **Devam**.

> Önizleme sayfasında soru metinleri düzgün görünüyor, "hata" yazmıyorsa yükleme tamamdır.

### 1b. Aşama aşama (aşamaları kademeli açmak isterseniz)

Aynı adımları her seferinde yalnızca bir dosya ile yapın: `asama1.xml`, sonra `asama2.xml` … Final paketleri için Adım 6'ya kadar bekleyin.

### 1c. Terminalden yükleme (Moodle arayüzü açmadan)

Docker üzerinde kullandığımız komut dizisi (PHP CLI betiği gerektirir; arayüz yolu yeterliyse atlayın):

```bash
docker cp python-sinav/ice.php moodle-proje-moodle-1:/tmp/
docker cp python-sinav/cikti/tum_havuz.xml moodle-proje-moodle-1:/tmp/
docker exec moodle-proje-moodle-1 php /tmp/ice.php /tmp/tum_havuz.xml 2   # 2 = kurs id
```

✔ **Doğrula:** Soru bankasında şu ağaç görünür:

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

> ⚠ **Aynı dosyayı iki kez içe aktarmayın.** Kategori ve sorular çoğalır. Yeniden yüklemek gerekirse önce `Python Sinav` kategorisini silin (Soru bankası → Kategoriler).

---

## Adım 2 — Bir soruyu elle dene (önizleme)

Her aşamadan en az bir soruyu denemek, Jobe'un çalıştığını ve test case'lerin doğru yüklendiğini gösterir.

1. Soru bankasında `Asama 1` kategorisini seçin → `s1_topla` satırının sağındaki **⋮ → Önizle**.
2. Kutuya şunu yazın:
   ```python
   a = int(input())
   b = int(input())
   print(a + b)
   ```
3. **Kontrol et**. Tüm satırlar yeşil ✔ olmalı, "Doğru" yazmalı.
4. Şimdi bilerek hatalı yapın (`print(a - b)`) → **Kontrol et** → kırmızı ✘ ve beklenen/alınan çıktı farkı görünmeli. Gizli testler "Gizli" olarak görünür ama başarısızlık yine hesaba katılır.
5. Sonsuz döngü deneyin (`while True: pass`) → birkaç saniye sonra **zaman aşımı** hatası gelmeli, sunucu donmamalı.

**Her aşamadan bir temsilci deneyin:**

| Aşama | Soru | Çözümü nerede? |
|---|---|---|
| 1 | `s1_topla` | `CEVAP_ANAHTARI.md` |
| 2 | `s2_harf` | " |
| 3 | `s3_asal` | " |
| 4 | `s4_palindrom` | " |
| 5 | `s5_frekans` | " |
| 6 | `s6_banka` | " |

Her sorunun editöründe aslında **Örnek çözüm** kayıtlıdır. Soru düzenleme sayfasında "Answer" alanına bakın.

✔ **Doğrula:** 6 soruda doğru çözüm → tam not, yanlış çözüm → kırmızı, sonsuz döngü → zaman aşımı.

> **Hata verirse:**
> * "Jobe server error / unreachable" → `docker compose ps`; jobe "healthy" değilse `docker compose restart jobe`.
> * "Sandbox disabled" → Site yönetimi → CodeRunner → Jobe seçili mi?

---

## Adım 3 — Aşama bazlı pratik sınavlarını kur

Her aşama için ayrı bir pratik sınavı. Öğrenciler konuyu bitirdikçe çözer.

**Bir aşama için (örnek: Aşama 1):**

1. Kurs sayfasında **Düzenlemeyi aç** → bölüm içinde **Bir etkinlik ya da kaynak ekle → Sınav**.
2. **Ad:** `Aşama 1 – Temeller (pratik)`.
3. Ayarlar (pratik sınavı için):

| Ayar | Değer | Neden |
|---|---|---|
| Zaman sınırı | kapalı (veya 40 dk) | Öğrenci rahat denesin |
| Deneme sayısı | sınırsız | Tekrar çalışsın |
| Not için yöntem | En yüksek not | |
| Soru davranışı | **Uyarlamalı mod** (*Adaptive mode*) | Soru başına birçok kez "Kontrol et" |
| Gözden geçirme seçenekleri | Deneme sırasında **ve** sonrasında: doğru/yanlış, geri bildirim açık | Öğrenme amaçlı |
| Soru düzeni | Yeni sayfa: her soru | Tek soru bir ekran |

4. **Kaydet ve göster** → sağ üstte **Sınavı düzenle**.
5. **Ekle → + Soru bankasından** → bağlam olarak kursu seçin → kategori: `Python Sinav / Asama 1 …` → tüm soruları işaretleyin → **Seçili soruları sınava ekle**.
6. Sağ üstte **Toplam not** 100 olacak şekilde ayarlayın (her sorunun puanı 10 ise 5 soruda 50 → "Maksimum not" 100 yapın). **Kaydet**.

Aşama 2–6 için aynı adımları, ilgili kategoriyle tekrarlayın.

> **İpucu (hızlı kopyalama):** İlk sınavı kurduktan sonra **Sınav → ⋮ → Çoğalt** ile kopyalayıp ad/kategoriyi değiştirmek daha hızlıdır.

> **Önerilen alternatif:** Tek bir `Python Pratik` sınavında altı bölüm (*Bölüm başlığı*) + her bölümde aşama soruları. Öğrenci tek sayfadan ilerler.

✔ **Doğrula:** Sınav önizlemesinde (Sınav → **Önizle**) tüm sorular sırayla geliyor, "Kontrol et" çalışıyor.

---

## Adım 4 — Test öğrenci hesapları ve kayıt

Prova için gerçek öğrenci kullanmadan 4 hesap açın.

**Hesap açma:** Site yönetimi → Kullanıcılar → Hesaplar → **Yeni kullanıcı ekle** (ya da CSV ile toplu).

| Kullanıcı adı | Ad Soyad | Rol (senaryo) |
|---|---|---|
| `test_guclu` | Güçlü Test | Her soruyu doğru çözer |
| `test_orta` | Orta Test | Sınır durumlarını kaçırır |
| `test_sorunlu` | Sorunlu Test | Hatalı/sonsuz döngü gönderir |
| `test_yuk` | Yük Test | Aynı anda çok sekme |

**Kursa kaydetme:** Kurs → **Katılımcılar → Kullanıcı kaydet** → rol **Öğrenci**. Alternatif: **Kayıt anahtarı** ile kendi kayıt (bkz. `KULLANIM_KILAVUZU.md` §Kurs oluşturma).

**Toplu CSV örneği** (Kullanıcıları yükle):
```
username,password,firstname,lastname,email,course1,role1
test_guclu,Test1234!,Güçlü,Test,guclu@example.com,se1001,student
test_orta,Test1234!,Orta,Test,orta@example.com,se1001,student
test_sorunlu,Test1234!,Sorunlu,Test,sorunlu@example.com,se1001,student
test_yuk,Test1234!,Yük,Test,yuk@example.com,se1001,student
```

✔ **Doğrula:** Gizli pencerede `test_guclu` ile giriş yapınca kursu ve pratik sınavlarını görüyor.

---

## Adım 5 — Aşamaları öğrenci gözüyle dene

Gizli pencereden **`test_guclu`** ile her pratik sınavı çözün (çözümler `CEVAP_ANAHTARI.md`'de).

| Hesap | Yapılacak | Beklenen sonuç |
|---|---|---|
| `test_guclu` | Tüm sorulara referans çözüm | %100 |
| `test_orta` | `s2_harf` için `>` kullan (sınır hatası) | Gizli testlerde ✘, kısmi puan |
| `test_sorunlu` | Sonsuz döngü, `import os; os.system("ls")`, syntax hatası, boş cevap | Mesaj gelir, sistem ayakta, dosya sistemi korunur |
| `test_yuk` | 5–10 sekmeden aynı anda **Kontrol et** | Her biri ~10 sn altında yanıtlanır |

Ayrıca yönetici hesabından **Sınav → Sonuçlar** sayfasını açıp notların listelendiğini görün.

✔ **Doğrula:** Beklenen sonuçlar yukarıdaki tabloyla örtüşüyor. Örtüşmeyen soru varsa `sorular.py`'de düzeltip `python3 uret.py` ile yeniden üretin.

---

## Adım 6 — Final sınavını kur (Paket A–D)

Gerçek sınav ayarları pratikten farklıdır (kısıtlı, süreli, tek deneme).

### 6a. Soruları yükle
Final soruları `Python Sinav / Final - Paket A…D` kategorilerinde zaten var. Yeni kursa yüklüyorsanız `final_paket_A.xml` … `D.xml` dosyalarını Adım 1a ile içe aktarın.

### 6b. Final paketleri

| Paket | Aşama 1 | Aşama 2 | Aşama 3 | Aşama 4 | Aşama 5 | Aşama 6 | Puan |
|---|---|---|---|---|---|---|---|
| A | ortalama (10) | harf (15) | asal (15) | palindrom (15) | frekans (20) | banka (25) | 100 |
| B | saniye | ucgen | fizzbuzz | sezar | tekrarsiz | parantez | 100 |
| C | bolme | artikyil | basamak | anagram | iki_toplam | guvenli_bol | 100 |
| D | daire | enbuyuk | faktoriyel | kelime | notlar | ikili_arama | 100 |

Komşu öğrencilere farklı paket vererek kopyayı zorlaştırın.

### 6c. Final sınavı ayarları (her paket için)

1. **Sınav ekle** → ad: `Python Final – Paket A`.
2. Ayarlar:

| Ayar | Değer |
|---|---|
| Aç/Kapa | Sınav günü ve saati |
| **Zaman sınırı** | 90 dakika |
| Zaman dolunca | **Açık denemeler otomatik gönderilir** |
| Deneme sayısı | **1** |
| Soru davranışı | **Ertelenmiş geri bildirim** (çözerken not görünmez) *ya da* Uyarlamalı (test sonuçlarını görmeleri istenirse) |
| Gözden geçirme | Deneme sırasında: yalnızca deneme · Sonra: **not** görünür, doğru cevap **gizli** |
| Soru düzeni | Hepsi tek sayfada **ya da** 1 soru/sayfa; gezinme **serbest** |
| Ek kısıtlar | **Şifre** (sınav anında söylenir) · gerekirse **IP adresi kısıtı** (lab alt ağı) |
| Tarayıcı güvenliği | *Tam ekran açılır pencere* (Safe Exam Browser yoksa) |

3. **Sınavı düzenle → Ekle → Soru bankasından** → `Final - Paket A` → 6 soru ekle.
4. Puanlar zaten 10/15/15/15/20/25 olarak yüklenir, **Maksimum not = 100**.
5. Paket B–D için kopyalayın ya da aynı adımları yineleyin.

### 6d. Paketleri öğrencilere dağıtma
* **Kolay yol:** Her paket için ayrı **Grup** (Katılımcılar → Gruplar) oluşturun, sınavın **Erişimi kısıtla** ayarında "Grup = Paket A" yapın. Öğrenci yalnızca kendi paketini görür.
* **Basit yol:** Tek sınav, tek paket (A). Küçük sınıflarda yeterli.

✔ **Doğrula:** `test_guclu` hesabını **Paket A grubuna** ekleyin: yalnızca Paket A sınavını görüyor, B/C/D görünmüyor.

---

## Adım 7 — Gerçek sınav provası

Yukarıdaki test hesaplarıyla, **gerçek koşullarda** tam bir prova: aynı saat, aynı süre, mümkünse lab ağı.

| Zaman | Adım |
|---|---|
| T−30 dk | `docker compose ps`; IP ve `MOODLE_WWWROOT` doğru; kendi hesabınızla giriş (bkz. `HOCA_LAB_KILAVUZU.md` §2) |
| T−10 dk | Öğrenci hesapları giriş yapar, sınav sayfası hazır |
| T−0 | Sınav açılır, şifre söylenir |
| Sınav sırasında | `docker stats`; takılan olursa sayfa yenile; ek süre için **Sınav → Kullanıcı geçersiz kılmaları** |
| T+90 | Otomatik gönderim; hiçbir ayar değiştirmeyin |

**Prova başarı ölçütleri:**
- [ ] İnternetsiz ağda tüm hesaplar giriş yaptı (telefon + 2. bilgisayarla bile olur).
- [ ] Referans çözümler 100, bilerek yanlışlar düşük puan aldı.
- [ ] Sonsuz döngü / `import os` denemeleri sistemi bozmadı.
- [ ] 90. dakikada cevaplar otomatik gönderildi, kayıp yok.
- [ ] Sunucu yük altında yanıt veriyor (`docker stats`'ta CPU takılı değil).

---

## Adım 8 — Sonuçları incele, havuzu düzelt

1. **Sınav → Sonuçlar → İstatistik**: her sorunun ortalama notu ve ayrım gücü.
   * Ortalama **%30 altı** → soru/test hatalı ya da fazla zor olabilir.
   * Ortalama **%95 üstü** → fazla kolay.
2. **Sonuçlar → Notlar → CSV indir**, yedeğe alın.
3. Soru bankasında bir soruyu açıp **gizli test**'lerin hangisinin en çok düştüğüne bakın: eksik sınır durumunun işaretidir.
4. Düzeltme gerekiyorsa `sorular.py`'yi değiştirip:
   ```bash
   cd python-sinav
   python3 uret.py          # doğrular ve XML'leri yeniden üretir
   ```
   Sonra eski kategoriyi silip (Soru bankası → Kategoriler → `Python Sinav` → sil) yeni XML'leri içe aktarın.

---

## Sık sorunlar

| Belirti | Çözüm |
|---|---|
| İçe aktarma "tanınmayan biçim" | Biçim *Moodle XML* seçili mi? Dosya `python-sinav/cikti/` içinden mi? |
| Sorular çift görünüyor | XML iki kez yüklendi → `Python Sinav` kategorisini silip bir kez yükleyin |
| "Kontrol et" sonucu hiç gelmiyor | `docker compose ps` → jobe "healthy" mi? Gerekirse `docker compose restart jobe` |
| Öğrenci tüm testlerde "Run error" alıyor | `input()` kullanan soruda **stdin** gerekir; öğrenci `input()` yerine fonksiyon yazmış olabilir (soru tipini kontrol edin) |
| Boş girdi testi her zaman patlıyor | CodeRunner boş/yalnızca-boşluk stdin'i boş kabul eder; `program` sorularında boş satır testi koymayın |
| Sınav süresi dolunca cevap kayboldu | *Süre dolunca: açık denemeler otomatik gönderilir* ayarı açık olmalı |

**Havuz özeti:** 34 soru · 235 test case · 6 aşama · 4 final paketi. Referans çözümlerin tamamı Moodle'ın gerçek CodeRunner/Jobe hattında tam not almıştır.
