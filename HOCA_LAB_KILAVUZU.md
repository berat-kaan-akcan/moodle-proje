# Hoca İçin Lab Günü Kılavuzu

Bu kılavuz, sınavı laboratuvarda **kendi bilgisayarınızdan** yayınlamanız içindir. Öğrenciler internete bağlanmaz; yalnızca sizin bilgisayarınızdaki Moodle adresini açar.

```
[Sizin PC: Moodle + Veritabanı + Kod Çalıştırıcı] ── lab ağı (internetsiz) ── [Öğrenci PC'leri]
```

Moodle, kod çalıştırma sistemi (Jobe) ve veritabanı sizin bilgisayarınızda Docker içinde çalışır. Öğrenci bilgisayarlarına hiçbir şey kurmanız gerekmez, tarayıcı yeterlidir.

---

## 1. Sınavdan önce (evde/ofiste, internetli)

1. **Sınavı hazırlayın:** Kurs, öğrenci listesi ve CodeRunner sorularını önceden girin. Adımlar için [KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md) dosyasına bakın.
2. **Sistemi bir kez internetle çalıştırın:** Gerekli Docker imajlarının bilgisayara inmesi gerekir. Lab'da internet olmadığı için bu adım atlanmamalıdır.
   ```bash
   cd ~/moodle-proje
   docker compose up -d
   ```
3. **Deneme sınavı yapın** (öğrenci hesabıyla giriş, soru çözme, bitirme).
4. **Yönetici şifresini değiştirin** (Site yönetimi → Kullanıcılar → Hesaplar). Varsayılan şifre öğrencilerin de olduğu ağda kalmamalıdır.
5. **Yedek alın** (Site yönetimi → Yedekleme veya proje klasörünün kopyası).
6. **Güç ayarları:** Bilgisayarın uyku, ekran kilidi ve otomatik güncellemesini kapatın. Şarj cihazını yanınıza alın.

---

## 2. Lab'a gelince (sınavdan ~20 dk önce)

### Adım 1 – Bilgisayarı lab ağına bağlayın
Ağ kablosunu lab switch'ine takın (ya da lab Wi‑Fi'ına bağlanın). Lab'da internet olmaması sorun değil.

### Adım 2 – IP adresinizi öğrenin
```bash
ip -4 -br addr
```
Lab ağındaki arayüzün adresini not alın (örn. `192.168.1.25`). Bu sizin **sunucu adresinizdir**. Öğrenci bilgisayarlarının adresleri de aynı bloktan başlamalıdır (`192.168.1.xxx`). Farklıysa lab görevlisine ağ yapısını sorun.

### Adım 3 – Moodle adresini güncelleyin
`.env` dosyasındaki satırı kendi IP'nizle değiştirin:
```
MOODLE_WWWROOT=http://192.168.1.25:8080
```
Sonra:
```bash
docker compose up -d
```

### Adım 4 – Erişime izin verin
Güvenlik duvarında 8080 portunu açın:
```bash
sudo firewall-cmd --add-port=8080/tcp
```

### Adım 5 – Önce kendiniz deneyin
Kendi tarayıcınızda `http://192.168.1.25:8080` adresini açın ve giriş yapın. Sonra bir öğrenci bilgisayarında aynı adresi deneyin.

### Adım 6 – Adresi öğrencilere duyurun
Tahtaya yazın: **`http://192.168.1.25:8080`** (kendi IP'nizle). Öğrenciler tarayıcının adres çubuğuna aynen yazar. Arama kutusuna değil.

---

## 3. Sınav sırasında

| Yapmanız gereken | Nasıl |
|---|---|
| Girenleri izlemek | Kurs → Katılımcılar; sınav sayfasında "Devam eden denemeler" |
| Süre/ek süre vermek | Sınav → Kullanıcı geçersiz kılmaları (Overrides) |
| Takılan öğrenci | Sayfayı yenilemesini söyleyin (cevaplar otomatik kaydedilir). Olmazsa başka PC'den girip aynı hesapla devam edebilir. |
| Sunucu durumu | `docker compose ps` (4 servis "Up" görünmeli) |
| Yavaşlama | `docker stats` ile CPU/RAM'e bakın |

**Önemli:**
- Bilgisayarı **kapatmayın, uyutmayın, ağ kablosunu çıkarmayın**.
- Kapağı kapatmayın. Laptop ise ekranı açık bırakın ya da kapak ayarını "bir şey yapma" yapın.
- Sınav sırasında yeni ayar/güncelleme yapmayın.

---

## 4. Sınav bittikten sonra

1. Sınavdaki **Denemeler** sayfasından notları ve cevapları görün.
2. Notları dışa aktarın: Kurs → Notlar → Dışa aktar (CSV/Excel).
3. Yedek alın.
4. İsterseniz sistemi kapatın: `docker compose stop` (veriler silinmez).
5. Ev/ofis ağında kullanacaksanız `.env`'i `http://localhost:8080`'e geri çevirip `docker compose up -d` çalıştırın.

> `docker compose down -v` komutunu **çalıştırmayın**. Tüm verileri (sınav, öğrenci, cevap) siler.

---

## 5. Sorun giderme

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Öğrenci sayfayı hiç açamıyor | Farklı ağda veya güvenlik duvarı | IP bloğunu ve 8080 portunu kontrol edin; öğrenci PC'sinden `ping 192.168.1.25` |
| Bir öğrenci açıyor, diğeri açamıyor | Öğrencinin ağ kablosu/IP'si | O PC'nin ağına bakın |
| Giriş yapınca adres `localhost` oluyor | `.env` güncellenmemiş | Adım 3'ü yapıp `docker compose up -d` |
| Sayfa açılıyor ama çok yavaş | Yoğunluk veya dış kaynak bekleme | `docker stats`; sayfayı yenileyin |
| "Kodu çalıştır" hata veriyor | Jobe çalışmıyor | `docker compose ps`; `docker compose restart jobe` |
| Her şey durdu | Konteynerler düşmüş | `docker compose up -d` (veriler korunur) |
| Giriş şifresi hatalı | Yanlış hesap | Yönetici ile şifre sıfırlama |

**Hızlı yeniden başlatma:** `docker compose restart` (öğrenci cevapları veritabanında durur, kaybolmaz).

---

## 6. Kısa kontrol listesi

- [ ] İmajlar önceden indirildi, deneme sınavı yapıldı
- [ ] Yönetici şifresi değiştirildi, yedek alındı
- [ ] Uyku modu kapalı, şarj bağlı
- [ ] Lab ağına bağlandı, IP öğrenildi
- [ ] `.env` yeni IP ile güncellendi, `docker compose up -d` yapıldı
- [ ] 8080 portu açıldı
- [ ] Bir öğrenci PC'sinden giriş denendi
- [ ] Adres tahtaya yazıldı

Teknik sorun olursa ekip: Berat Kaan Akcan (beratkaanakcan@gmail.com).
