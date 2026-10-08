# MSKÜ DYS – Proje ve Test Raporu

| | |
|---|---|
| **Proje** | Moodle 4.5 + CodeRunner + Jobe Sandbox + MSKÜ DYS teması (Docker Compose) |
| **Hazırlayan** | Berat Kaan Akcan |
| **Tarih** | 8 Ekim 2026 |
| **Eşlik eden belge** | [KILAVUZ.md](KILAVUZ.md) – kurulum ve kullanım adımları |

Bu rapor iki bölümden oluşur: **A) Proje raporu** (ne yapıldı, nasıl çalışıyor, açık konular) ve **B) Lab testi özeti** (ayrıntılar TEST_KILAVUZU.md içinde).

---

# A. Proje Raporu

## A.1 Amaç ve kapsam
Programlama dersinde otomatik değerlendirmeli, **internetsiz lab ağında** çalışabilen bir Python sınav ortamı kurmak. Sunucu hocanın bilgisayarıdır; öğrenciler tarayıcıdan bağlanır.

## A.2 Bileşenler
| Bileşen | Görev |
|---|---|
| Moodle 4.5 (PHP 8.3) | Kurs, kullanıcı, sınav yönetimi |
| MariaDB 11.4 | Veritabanı (`init-db/moodle.sql` ile hazır yüklenir) |
| CodeRunner | Kod soruları ve otomatik not verme |
| Jobe | Öğrenci kodunun izole çalıştırıldığı sandbox |
| MSKÜ DYS teması | Üniversite giriş sayfası görünümü |
| Cron konteyneri | Moodle zamanlanmış görevleri |

Ayrıntılı mimari ve klasör yapısı: KILAVUZ §1–2.

## A.3 Yapılanlar (kronolojik)
| Tarih | Commit | Değişiklik |
|---|---|---|
| 6 Eki | `c132d77d` | Moodle 4.5, Jobe, CodeRunner, MSKÜ DYS teması ve veritabanı yedeği |
| 7 Eki | `bb8a3167` | Proje dosyaları güncellendi |
| 8 Eki | `172ba72b` | Yerel ağda erişim için **çevrimdışı** font/CSS (Roboto, FontAwesome) |
| 8 Eki | `7a329e7f` | `alternateloginurl` artık `wwwroot` üzerinden dinamik |
| 8 Eki | `7575c41f` | Geliştirme ortamı IP güncellemesi, hotspot test betiği (`hotspot-test.sh`) |
| 8 Eki | *(commit edilmedi)* | Monaco editör, Ace iyileştirmeleri, `.env` IP değişikliği, belgeler |

## A.4 Python sınav havuzu
- 6 aşama, 34 soru (her biri 10 puan); `python-sinav/sorular.py` içinde tanımlı, `uret.py` ile Moodle XML'e dönüştürülür.
- Çıktılar `python-sinav/cikti/` altında: `asama1–6.xml`, `final_paket_A–D.xml`, `tum_havuz.xml`.
- Cevaplar: `python-sinav/CEVAP_ANAHTARI.md` (yalnızca hoca). Soru yazımı ve yükleme adımları: KILAVUZ §9–12.

## A.5 Kod editörü değişikliği (commit edilmemiş)
**Ne:** CodeRunner'ın varsayılan editörü Ace yerine **Monaco** (VS Code editörü) yapıldı.

| Dosya | Değişiklik |
|---|---|
| `amd/src/ui_monaco.js` (+ `build/ui_monaco.min.js`, `ui_monaco.json`) | Yeni UI eklentisi; Ace ile aynı arayüz |
| `monaco/` (≈4,3 MB) | Monaco dosyaları yerelde; `editor.html` iframe içinde çalışır (Moodle RequireJS ile çakışmasın diye). Dış CDN yok → internetsiz çalışır |
| `classes/util.php`, `question.php`, `renderer.php` | `uiplugin` belirtilmemişse varsayılan `ace` → `monaco` |
| `amd/src/ui_ace.js` (+ build) | Ace için: 4 boşluk sekme, VS Code tarzı Tab davranışı, monospace yazı tipi |

**Fallback:** Monaco sayfası yüklenemezse düz textarea'ya düşer.
**Geri alma:** Soru ayarında UI eklentisi olarak `ace` seçilebilir veya üç PHP dosyasındaki `'monaco'` tekrar `'ace'` yapılır.
**Dikkat:** Moodle'u güncellerken bu dosyalar ezilebilir; değişiklikler yedeklenmeli.

## A.6 Ağ ve çevrimdışı çalışma
- Sunucu adresi `.env` içindeki `MOODLE_WWWROOT` ile belirlenir; her yeni ağda IP değişir ve güncellenmelidir (şu an `http://10.42.0.1:8080`, hotspot IP'si).
- Giriş sayfası fontları/ikonları yerelden yüklenir (dış istek yok).
- `hotspot-test.sh`: hotspot açar, `.env` adresini günceller, servisleri başlatır, güvenlik duvarı durumunu ve gelen istekleri kaydeder.

## A.7 Açık konular ve riskler
| # | Konu | Durum / öneri |
|---|---|---|
| 1 | Monaco ve Ace değişiklikleri commit edilmedi | Lab testinden sonra commit edilmeli |
| 2 | `.env` ve `config.php` repoda; şifreler varsayılan (`root_degistir`, `Admin.1234!`) | Gerçek sınavdan önce değiştirilmeli (KILAVUZ §20) |
| 3 | `moodledata_filedir.tar.gz` (~11 MB) ve `init-db/moodle.sql` repoda | Gerekli ama güncel yedek alınmalı (KILAVUZ §18) |
| 4 | Lab testi (Bölüm B) henüz yapılmadı | Sınavdan önce T1–T10 [TEST_KILAVUZU.md](TEST_KILAVUZU.md) ile yapılmalı |
| 5 | Monaco internetsiz ve öğrenci tarayıcılarında denenmedi | Test T4/T5 içinde kontrol edilmeli |
| 6 | `python-sinav/__pycache__` ve `.pdf` takipsiz | `.gitignore`'a `__pycache__/` eklenmeli |

---

# B. Lab Ortamı Testi

Test planı, terminal komutları, hazır betikler ve sonuç formu ayrı belgeye taşındı: **[TEST_KILAVUZU.md](TEST_KILAVUZU.md)**. Test sonucu orada doldurulur; bu rapora yalnızca özet eklenir.

| Durum | Açıklama |
|---|---|
| Lab testi (T1–T10) | Henüz yapılmadı |
| Sunucu otomatik kontrolleri | `test/sunucu_kontrol.sh` çalıştırıldı: servisler ve Jobe geçti; varsayılan şifreler ve `debugdisplay` açık olduğu için güvenlik maddeleri kaldı; hotspot kapalı olduğundan adres/erişim maddeleri çalışmadı |
| Jobe yükü | 50 eşzamanlı python3 işi hepsi başarılı, en yavaş ~1,6 sn |
