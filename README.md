# 🎓 Moodle LMS & Jobe Sandbox (DYS Temalı)

Bu proje; **Moodle 4.5 LMS**, izole kod çalıştırma ortamı **Jobe Sandbox**, kodlama soruları için **CodeRunner** eklentisi ve **Muğla Sıtkı Koçman Üniversitesi DYS (Uzaktan Eğitim)** oturum açma arayüzü ile donatılmış, Docker tabanlı tam teşekküllü bir eğitim platformudur.

Veritabanı dökümü (`init-db/moodle.sql`) projeye dahil edilmiştir; bu sayede projeyi indiren kişi **hiçbir kurulum veya ayar yapmadan tek komutla** tüm dersleri, kullanıcıları ve sınavları hazır şekilde ayağa kaldırabilir.

---

## 🚀 Hızlı Başlangıç (Kurulum Adımları)

### 1. Ön Gereksinimler
Bilgisayarınızda **Docker** ve **Docker Compose** kurulu ve çalışır durumda olmalıdır:
* **Windows & Mac:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) uygulamasını indirip başlatın.
* **Linux:** `docker` ve `docker-compose-plugin` kurulu olmalıdır.

---

### 2. Projeyi Klonlayın
```bash
git clone https://github.com/berat-kaan-akcan/moodle-proje.git
cd moodle-proje
```

---

### 3. Sistemi Başlatın
Klasörün içinde terminal (veya Windows PowerShell / CMD) açarak şu komutu çalıştırın:

```bash
docker compose up -d
```

> ⏳ **İlk Başlatma Notu:** İlk çalıştırmada Docker imajları indirilecek ve MariaDB veritabanı (`init-db/moodle.sql`) otomatik olarak yüklenecektir. Bu işlem sistem hızınıza bağlı olarak yaklaşık 1-2 dakika sürebilir.

Konteynerlerin durumunu kontrol etmek için:
```bash
docker compose ps
```
Tüm servislerin (`db`, `moodle`, `cron`, `jobe`) **Up** (veya *healthy*) durumda olduğunu gördüğünüzde sistem hazırdır.

---

## 🔑 Sisteme Giriş ve Hesap Bilgileri

Web tarayıcınızda (Chrome, Firefox, Edge vb.) şu adresi açın:

👉 **[http://localhost:8080](http://localhost:8080)**

Sizi otomatik olarak **MSKÜ DYS Giriş Sayfası** karşılayacaktır.

### Hazır Hesaplar:

| Rol | Kullanıcı Adı | E-posta | Şifre |
|---|---|---|---|
| **Yönetici (Admin)** | `admin` | `beratkaanakcan@gmail.com` | `Admin.1234!` |
| **Öğrenci** | `dogukan` | `dd@mu.edu.tr` | `Admin.1234!` *(veya belirlenen şifre)* |

> 💡 **İpucu:** Sistemde e-posta ile giriş desteği aktiftir. Kullanıcı adı yerine doğrudan e-posta adresinizi yazarak da giriş yapabilirsiniz.

---

## 📚 Hazır Dersler ve İçerikler

* **Ders Adı:** `programing` *(Kısa Kod: `se1001`)*
* **Ders İçeriği:** CodeRunner eklentisi entegre edilmiştir.
* **Jobe Sandbox:** Öğrencilerin yazdığı Python / C / Java kodları arka plandaki izole `jobe` Docker konteynerinde güvenle derlenir ve anında otomatik değerlendirilir.

---

## 🛠️ Sistem Mimarisi & Docker Servisleri

* **`moodle`:** Apache & PHP 8.3 üzerinde çalışan Moodle 4.5.14+ çekirdeği. (`8080` portundan yayınlanır)
* **`db`:** MariaDB 11.4 veritabanı sunucusu. (`init-db` ile otomatik ilk kurulum sağlar)
* **`cron`:** Moodle'ın zamanlanmış görevlerini her 60 saniyede bir çalıştıran arka plan servisi.
* **`jobe`:** `trampgeek/jobeinabox` güvenli kod çalıştırma sandbox sunucusu. (Sadece iç Docker ağında çalışır)

---

## ⚙️ Sık Kullanılan Yönetim Komutları

### Sistemi Durdurma:
```bash
docker compose stop
```

### Sistemi Yeniden Başlatma:
```bash
docker compose start
```

### Sistemi Tamamen Kapatma:
```bash
docker compose down
```

### Moodle Önbelleğini Temizleme (Purge Caches):
```bash
docker compose exec -T moodle php /var/www/html/admin/cli/purge_caches.php
```

### Zamanlanmış Görevleri (Cron) Manuel Tetikleme:
```bash
docker compose exec -T moodle php /var/www/html/admin/cli/cron.php
```

### Veritabanının Yeni Bir Yedeğini Alma:
```bash
docker compose exec -T db mariadb-dump -u moodle -pmoodle_degistir moodle > init-db/moodle.sql
```

---

## 📖 Detaylı Kullanım Kılavuzu
Kurs açma, toplu öğrenci/öğretmen yükleme (CSV), rol atama ve CodeRunner soru hazırlama adımları için projedeki [KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md) dosyasını inceleyebilirsiniz.
