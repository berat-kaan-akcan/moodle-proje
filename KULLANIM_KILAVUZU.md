# Moodle Projesi Kapsamlı Kullanım Kılavuzu

Bu kılavuz, yerel Docker ortamınızda çalışan **Moodle 4.5 LMS** ve entegre **Jobe/CodeRunner** platformunun yönetimi için hazırlanmıştır.

---

## 📌 İçindekiler
1. [Sisteme Erişim ve Giriş Bilgileri](#1-sisteme-erişim-ve-giriş-bilgileri)
2. [Moodle Mantığı: Kullanıcı ve Rol Mimarisi](#2-moodle-mantığı-kullanıcı-ve-rol-mimarisi)
3. [Kullanıcı Ekleme (Öğrenci ve Hoca Hesapları)](#3-kullanıcı-ekleme-öğrenci-ve-hoca-hesapları)
   - [Yöntem A: Arayüzden Tek Tek Ekleme](#yöntem-a-arayüzden-tek-tek-kullanıcı-ekleme)
   - [Yöntem B: CSV ile Toplu Kullanıcı Yükleme](#yöntem-b-csv-ile-toplu-kullanıcı-yükleme-bulk-upload)
4. [Kurs (Ders) ve Kategori Yönetimi](#4-kurs-ders-ve-kategori-yönetimi)
   - [Kategori Oluşturma ve Düzenleme](#kategori-oluşturma)
   - [Yeni Kurs Ekleme](#yeni-kurs-ekleme)
5. [Kursa Öğrenci ve Hoca Atama (Kayıt İşlemleri)](#5-kursa-öğrenci-ve-hoca-atama-kayıt-işlemleri)
   - [Yöntem 1: Manuel Kayıt (Hoca/Yönetici Tarafından)](#yöntem-1-manuel-kayıt-yönetici-veya-hoca-tarafından)
   - [Yöntem 2: Kendi Kendine Kayıt (Öğrenci Şifre ile Kayıt - Enrolment Key)](#yöntem-2-kendi-kendine-kayıt-self-enrolment-ile-kayıt-anahtarı)
6. [Bu Projeye Özel: CodeRunner & Jobe ile Kodlama Sınavı Hazırlama](#6-bu-projeye-özel-coderunner--jobe-ile-kodlama-sınavı-hazırlama)
7. [Faydalı Docker & Bakım Komutları](#7-faydalı-docker--bakım-komutları)

---

## 1. Sisteme Erişim ve Giriş Bilgileri

- **Web Arayüzü:** [http://localhost:8080](http://localhost:8080)
- **Varsayılan Yönetici (Admin) Bilgileri:**
  - **Kullanıcı Adı:** `admin`
  - **Şifre:** `Admin.1234!`
- **Sistem Dili:** Türkçe (`tr`)
- **Moodle Sürümü:** 4.5.14+ (Modern Boost Arayüzü)

> Servislerin çalıştığından emin olmak için terminalden `docker compose ps` komutunu çalıştırabilirsiniz.

---

## 2. Moodle Mantığı: Kullanıcı ve Rol Mimarisi

Moodle'da kullanıcı açma ile kursa atama birbirinden ayrıdır:
1. **Adım 1:** Kişi sisteme **kullanıcı** olarak kaydedilir (öğrenci ya da hoca fark etmeksizin temel hesaptır).
2. **Adım 2:** Kişi ilgili **kursa** atanırken rolü belirlenir:
   - **Öğretmen (Editing Teacher):** Kurs içeriği ekleyebilir, sınav hazırlayabilir, not verebilir.
   - **Düzenleyemeyen Öğretmen (Non-editing Teacher / Asistan):** İçeriği değiştiremez, öğrencileri değerlendirip not verebilir.
   - **Öğrenci (Student):** Ders materyallerini görüntüler, ödev teslim eder ve sınavları çözer.
   - **Yönetici (Manager):** Kurs seviyesinde tam idari yetkiye sahiptir.

---

## 3. Kullanıcı Ekleme (Öğrenci ve Hoca Hesapları)

### Yöntem A: Arayüzden Tek Tek Kullanıcı Ekleme

1. Admin hesabınızla Moodle'a giriş yapın.
2. Üst menü çubuğundaki **Site yönetimi** sekmesine tıklayın.
3. **Kullanıcılar** sekmesini açın.
4. **Hesaplar** başlığı altındaki **Yeni bir kullanıcı ekle** bağlantısına tıklayın.
5. Gerekli alanları doldurun:
   - **Kullanıcı adı:** Küçük harflerden oluşmalıdır (örn: `ahmet.yilmaz` veya `20240101`).
   - **Yeni şifre:** Kalem simgesine tıklayarak şifre belirleyin (örn: `Ogrenci.2024!`) veya *Kullanıcının ilk girişte şifre değiştirmesini zorunlu kıl* kutucuğunu işaretleyin.
   - **Ad:** Kullanıcının adı.
   - **Soyadı:** Kullanıcının soyadı.
   - **E-posta adresi:** Geçerli bir e-posta formatı (örn: `ahmet@mu.edu.tr`).
6. Sayfanın en altındaki **Kullanıcı oluştur** butonuna tıklayın.

---

### Yöntem B: CSV ile Toplu Kullanıcı Yükleme (Bulk Upload)

Sınıf listesini veya tüm hocaları tek seferde yüklemek için en pratik yoldur.

1. **Site yönetimi > Kullanıcılar > Hesaplar > Kullanıcıları yükle** sayfasına gidin.
2. Bir `.csv` dosyası hazırlayın (UTF-8 kodlamasında).

#### Örnek CSV İçeriği (`ogrenciler.csv`):
```csv
username,password,firstname,lastname,email,course1,role1
2024001,Sifre.1234!,Ali,Demir,ali.demir@mu.edu.tr,se1001,student
2024002,Sifre.1234!,Ayse,Kaya,ayse.kaya@mu.edu.tr,se1001,student
mehmet.hoca,Hoca.1234!,Mehmet,Yildiz,mehmet.yildiz@mu.edu.tr,se1001,editingteacher
```

> **İpucu:** `course1` sütununa kursun **kısa adı** (örn: `se1001`), `role1` sütununa ise rol kodu (`student`, `editingteacher`, `teacher`) yazılırsa, kullanıcılar oluşturulurken **aynı anda kursa da atanır**.

3. Dosyayı sürükleyip bırakın ve **Kullanıcıları yükle** butonuna basın.
4. Önizleme ekranında alanların doğruluğunu teyit edip işlemi onaylayın.

---

## 4. Kurs (Ders) ve Kategori Yönetimi

### Kategori Oluşturma
Dersleri düzenli tutmak için (örn: *Mühendislik Fakültesi > Bilgisayar Mühendisliği > 1. Sınıf*):
1. **Site yönetimi > Kurslar > Kursları ve kategorileri yönet** sayfasına gidin.
2. **Yeni kategori oluştur** butonuna tıklayın.
3. Kategori adını girip **Kategori oluştur** deyin.

### Yeni Kurs Ekleme
1. **Site yönetimi > Kurslar > Yeni bir kurs ekle** yolunu izleyin (veya kategori içinden *Yeni kurs oluştur* deyin).
2. **Genel Ayarlar:**
   - **Kurs tam adı:** Kursun tam adı (örn: `Programlamaya Giriş (Python)`).
   - **Kurs kısa adı:** Moodle içindeki benzersiz kod (örn: `SE1001`). *Formüllerde ve toplu yüklemelerde bu kod kullanılır.*
   - **Kurs kategorisi:** Kursun ait olduğu kategori.
   - **Kurs başlangıç / bitiş tarihi:** Dersin dönemi.
3. **Kurs biçimi (Course format):**
   - **Haftalık biçim:** Haftalara bölünmüş ders yapısı.
   - **Konular biçimi (Tavsiye edilen):** Modül ve ünitelere bölünmüş esnek yapı.
4. Sayfanın altından **Kaydet ve göster** butonuna tıklayın.

---

## 5. Kursa Öğrenci ve Hoca Atama (Kayıt İşlemleri)

Oluşturduğunuz bir kursa kullanıcıları eklemenin 2 temel yolu vardır:

### Yöntem 1: Manuel Kayıt (Yönetici veya Hoca Tarafından)
1. Kurs sayfasına gidin (Örn: *programing - se1001*).
2. Kurs menüsünden **Katılımcılar** (Participants) sekmesine tıklayın.
3. Sağ üstteki mavi **Kullanıcıları kaydet** (Enrol users) butonuna tıklayın.
4. Açılan pencerede:
   - **Rol ata:** Ekleyeceğiniz kişinin rolünü seçin:
     - Hoca için: `Öğretmen` (Editing teacher)
     - Asistan için: `Düzenleyemeyen Öğretmen` (Non-editing teacher)
     - Öğrenci için: `Öğrenci` (Student)
   - **Kullanıcıları seçin:** Arama kutusuna öğrencinin veya hocanın adını/kullanıcı adını yazıp listeden seçin.
5. **Kayıtlı kullanıcıları seçin** butonuna tıklayarak tamamlayın.

---

### Yöntem 2: Kendi Kendine Kayıt (Self-Enrolment ile Kayıt Anahtarı)
Hocanın tek tek öğrenci eklemesi yerine, öğrencilerin ders şifresini (anahtarını) girerek kendilerinin derse kaydolması:

1. Kursa girin > **Katılımcılar** sekmesine tıklayın.
2. Sayfanın üst kısmındaki açılır menüden **Kayıt yöntemleri** (Enrolment methods) seçeneğini seçin.
3. Listede **Kendi kendine kayıt (Öğrenci)** satırını bulun:
   - Eğer yanında üzeri çizili göz ikonu varsa, göze tıklayarak **aktif** hale getirin.
4. Satırın sağındaki **Çark (Ayarlar)** simgesine tıklayın:
   - **Kayıt anahtarı (Enrolment key):** Derse özel bir şifre belirleyin (örn: `Python2024!`).
   - **Varsayılan atanmış rol:** `Öğrenci` olarak kalsın.
5. Sayfanın altından **Değişiklikleri kaydet** butonuna basın.
6. Artık öğrenciler Moodle'a giriş yaptıklarında bu kursu bulup belirlediğiniz anahtarı girerek anında derse kaydolabilirler.

---

## 6. Bu Projeye Özel: CodeRunner & Jobe ile Kodlama Sınavı Hazırlama

Bu projede kodları güvenli ve izole bir konteynerde çalıştıran **Jobe sandbox** (`jobeinabox`) ve **CodeRunner** soru tipi entegre durumdadır.

### Adım Adım Kodlama Sorusu / Sınavı Oluşturma:
1. Kurs sayfasına gidin.
2. Sağ üstteki **Düzenleme modunu aç** (Edit mode) anahtarını açın.
3. İlgili haftada/konuda **Yeni bir etkinlik veya kaynak ekle** butonuna tıklayın.
4. Listeden **Sınav** (Quiz) seçeneğini seçin. Sınava isim verip (örn: `Hafta 1 - Python Pratik Sınavı`) kaydedin.
5. Oluşturduğunuz sınava tıklayın ve **Sorular** (Questions) sekmesine geçin.
6. **Ekle > Yeni bir soru** yolunu izleyin.
7. Soru tipleri listesinden **CodeRunner** seçeneğini seçip **Ekle**'ye tıklayın.
8. **Soru Ayarları:**
   - **Soru adı:** örn: `Faktöriyel Fonksiyonu`
   - **CodeRunner soru türü:** Dili seçin (örn: `python3`, `c_program`, `java` vb.)
   - **Soru metni:** Öğrencinin yapması gereken görevi yazın (örn: *`faktoriyel(n)` adında bir fonksiyon yazınız...*).
   - **Örnek Çözüm:** Doğru çalışan python fonksiyonunu yazın.
   - **Test Senaryoları (Test Cases):**
     - *Test 1:* Test kodu: `print(faktoriyel(5))` | Beklenen çıktı: `120`
     - *Test 2:* Test kodu: `print(faktoriyel(0))` | Beklenen çıktı: `1`
     - İsterseniz bazı testleri *Gizli (Hidden)* yaparak öğrencinin kopya çekmesini engelleyebilirsiniz.
9. **Değişiklikleri kaydet** deyin.

> Öğrenci kodu yazdığında Moodle arka planda Jobe konteynerine HTTP isteği atar, kod güvenle çalıştırılır, çıktılar test senaryolarıyla karşılaştırılır ve öğrenciye anında otomatik not verilir.

---

## 7. Faydalı Docker & Bakım Komutları

Gerektiğinde terminalden hızlı müdahale yapabileceğiniz komutlar:

### Moodle Önbelleğini Temizleme (Purge Caches):
```bash
docker compose exec -T moodle php /var/www/html/admin/cli/purge_caches.php
```

### Zamanlanmış Görevleri (Cron) Manuel Çalıştırma:
```bash
docker compose exec -T moodle php /var/www/html/admin/cli/cron.php
```

### Unutulan Admin Şifresini Terminalden Sıfırlama:
```bash
docker compose exec -T moodle php /var/www/html/admin/cli/reset_password.php
```

### Konteyner Durumunu Kontrol Etme:
```bash
docker compose ps
```
