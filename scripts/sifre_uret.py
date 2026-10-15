#!/usr/bin/env python3
"""Öğrenci listesinden Moodle yükleme CSV'si ve dağıtım listesi üretir.

Kullanım: python3 scripts/sifre_uret.py ogrenciler.csv [kurs_kisa_adi] [kohort_id]
Girdi CSV başlıkları: numara,ad,soyad[,email]
Çıktı (cikti/ klasörü):
  moodle-yukle.csv   -> Moodle'a yüklenecek dosya
  sifre-dagitim.csv  -> Sizde kalacak numara/ad/şifre listesi (öğrencilere dağıtım)
"""
import csv, os, secrets, string, sys

KURS = sys.argv[2] if len(sys.argv) > 2 else "se1001"
KOHORT = sys.argv[3] if len(sys.argv) > 3 else "ogrenciler-2026-guz"
UPPER, LOWER, DIGIT, SYMBOL = "ABCDEFGHJKLMNPQRSTUVWXYZ", "abcdefghijkmnpqrstuvwxyz", "23456789", "!#$%*+?"


def sifre(n=10):
    # Moodle politikası: >=8 karakter, büyük/küçük harf, rakam, sembol (karışan karakterler çıkarıldı)
    ch = [secrets.choice(s) for s in (UPPER, LOWER, DIGIT, SYMBOL)]
    ch += [secrets.choice(UPPER + LOWER + DIGIT) for _ in range(n - 4)]
    secrets.SystemRandom().shuffle(ch)
    return "".join(ch)


girdi = sys.argv[1]
os.makedirs("cikti", exist_ok=True)
with open(girdi, newline="", encoding="utf-8-sig") as f, \
     open("cikti/moodle-yukle.csv", "w", newline="", encoding="utf-8") as y, \
     open("cikti/sifre-dagitim.csv", "w", newline="", encoding="utf-8") as d:
    yw = csv.writer(y); dw = csv.writer(d)
    yw.writerow(["username", "password", "firstname", "lastname", "email", "course1", "role1", "cohort1"])
    dw.writerow(["numara", "ad", "soyad", "kullanici_adi", "sifre"])
    for r in csv.DictReader(f):
        no = r["numara"].strip().lower()
        s = sifre()
        mail = (r.get("email") or "").strip() or f"{no}@okul.local"
        yw.writerow([no, s, r["ad"].strip(), r["soyad"].strip(), mail, KURS, "student", KOHORT])
        dw.writerow([no, r["ad"].strip(), r["soyad"].strip(), no, s])
print("Hazır: cikti/moodle-yukle.csv ve cikti/sifre-dagitim.csv")
