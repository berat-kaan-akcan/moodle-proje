#!/usr/bin/env python3
"""Sınav yük testi: sahte öğrenciler aynı anda giriş yapar, sınavı başlatır, her soruda "Kontrol et"e basar, teslim eder.

  python3 test/sinav_yuk_testi.py hazirla 40 4      # yuk01..yuk40 hesaplarını oluştur, cmid=4 sınavının kursuna kaydet
  python3 test/sinav_yuk_testi.py calistir [URL]    # URL verilmezse .env içindeki MOODLE_WWWROOT kullanılır
  python3 test/sinav_yuk_testi.py temizle           # hesapları ve denemelerini sil (gerçek sınavdan önce ŞART)

cmid, sınav sayfasının adresindeki sayıdır: /mod/quiz/view.php?id=4
Her aşama (giriş, başlatma, her sayfada kontrol, teslim) bütün öğrenciler için aynı anda tetiklenir.
Sınavda şifre ya da tek deneme hakkı varsa betik sınavı başlatamaz; yük testini bu ayarlardan önce yapın.
"""
import html, json, os, re, secrets, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from http.cookiejar import CookieJar
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AYAR = os.path.join(KOK, "cikti", "yuk-testi.json")
ZAMAN_ASIMI = 240
KOD = "print(sum(range(200000)))"
if os.environ.get("YUK_KOD"):  # ağır kodla denemek için: YUK_KOD=agir.py python3 test/sinav_yuk_testi.py calistir
    with open(os.environ["YUK_KOD"], encoding="utf-8") as f:
        KOD = f.read()


def php(*arg):
    with open(os.path.join(KOK, "test", "yuk_hesaplari.php"), "rb") as f:
        r = subprocess.run(["docker", "compose", "exec", "-T", "-u", "www-data", "moodle", "php", "--", *map(str, arg)],
                           stdin=f, capture_output=True, text=True, cwd=KOK)
    if r.returncode:
        sys.exit(r.stderr.strip() or r.stdout.strip())
    return json.loads(r.stdout)


def env_adresi():
    with open(os.path.join(KOK, ".env"), encoding="utf-8") as f:
        for satir in f:
            if satir.startswith("MOODLE_WWWROOT="):
                return satir.split("=", 1)[1].strip()
    sys.exit(".env içinde MOODLE_WWWROOT yok; adresi elle verin.")


class Ogrenci:
    def __init__(self, ad, sifre, kok, cmid):
        self.ad, self.sifre, self.kok, self.cmid = ad, sifre, kok, cmid
        self.ac = build_opener(HTTPCookieProcessor(CookieJar()))
        self.adres = self.govde = ""
        self.deneme = self.sesskey = None
        self.sayfa = 0  # sıradaki sayfa; -1 = sayfalar bitti

    def iste(self, yol, veri=None):
        try:
            with self.ac.open(self.kok + yol, urlencode(veri).encode() if veri is not None else None,
                              timeout=ZAMAN_ASIMI) as r:
                self.adres, self.govde = r.geturl(), r.read().decode("utf-8", "replace")
        except HTTPError as e:
            m = re.search(r'class="errormessage[^"]*">\s*(.*?)\s*<', e.read().decode("utf-8", "replace"), re.S)
            raise RuntimeError(f"HTTP {e.code} {yol.split('?')[0]}" + (f": {html.unescape(m.group(1))}" if m else ""))

    def bul(self, desen, hata):
        m = re.search(desen, self.govde)
        if not m:
            raise RuntimeError(hata)
        return m.group(1)

    def giris(self):
        self.iste("/login/index.php")
        jeton = self.bul(r'name="logintoken" value="([^"]+)"', "giriş sayfasında logintoken yok")
        self.iste("/login/index.php", {"username": self.ad, "password": self.sifre, "logintoken": jeton})
        if "/login/" in self.adres:
            raise RuntimeError("giriş reddedildi")

    def baslat(self):
        self.iste(f"/mod/quiz/view.php?id={self.cmid}")
        self.sesskey = self.bul(r'"sesskey":"([^"]+)"', "sınav sayfası açılmadı")
        self.iste("/mod/quiz/startattempt.php", {"cmid": self.cmid, "sesskey": self.sesskey})
        if "attempt.php" not in self.adres:
            raise RuntimeError("sınav başlatılamadı (şifre, süre ya da deneme hakkı?)")
        self.deneme = self.bul(r'name="attempt" value="(\d+)"', "deneme numarası bulunamadı")

    def sayfa_ac(self):
        self.iste(f"/mod/quiz/attempt.php?attempt={self.deneme}&cmid={self.cmid}&page={self.sayfa}")
        if "responseform" not in self.govde:
            raise RuntimeError("soru sayfası açılmadı")

    def kontrol(self):
        """Açık sayfadaki kod sorularına KOD yazar ve "Kontrol et"e basar; soru başka türdeyse yalnızca kaydeder."""
        alan = {}
        for etiket in re.findall(r"<(?:input|textarea|button)\b[^>]*>", self.govde):
            oz = dict(re.findall(r'([\w:-]+)="([^"]*)"', etiket))
            ad = oz.get("name", "")
            if oz.get("type") == "hidden" and ad:
                alan[ad] = html.unescape(oz.get("value", ""))
            elif ad.endswith("_answer") and etiket.startswith("<textarea"):
                alan[ad] = KOD
            elif ad.endswith("_-submit"):
                alan[ad] = "1"
        kod_sorusu = any(a.endswith("_-submit") for a in alan)
        sonraki = int(alan.get("nextpage", -1))
        if not kod_sorusu:
            alan["next"] = "1"
        self.iste(f"/mod/quiz/processattempt.php?cmid={self.cmid}", alan)
        if kod_sorusu and "coderunner-test-results" not in self.govde:
            raise RuntimeError("kontrol sonucu gelmedi" + (" (Jobe aşırı yük)" if "overload" in self.govde else ""))
        self.sayfa = sonraki

    def bitir(self):
        self.iste(f"/mod/quiz/processattempt.php?cmid={self.cmid}",
                  {"attempt": self.deneme, "finishattempt": 1, "timeup": 0, "slots": "",
                   "cmid": self.cmid, "sesskey": self.sesskey})
        if "/mod/quiz/review.php" not in self.adres and "/mod/quiz/view.php" not in self.adres:
            raise RuntimeError("teslim onaylanmadı")


def asama(ad, ogrenciler, is_):
    """is_ işlevini bütün öğrenciler için aynı anda çalıştırır; hata alanları listeden düşürür."""
    def olc(o):
        t = time.time()
        try:
            is_(o)
            return o, time.time() - t, None
        except Exception as e:
            return o, time.time() - t, f"{type(e).__name__}: {e}"

    with ThreadPoolExecutor(len(ogrenciler)) as ex:
        s = list(ex.map(olc, ogrenciler))
    sure = sorted(t for _, t, _ in s)
    hata = [(o.ad, h) for o, _, h in s if h]
    print(f"{ad:<22} {len(s) - len(hata):>3}/{len(s):<3} başarılı | ortanca {sure[len(sure) // 2]:6.2f}s"
          f" | en yavaş {sure[-1]:6.2f}s")
    for kim, h in hata[:5]:
        print(f"    [HATA] {kim}: {h}")
    if len(hata) > 5:
        print(f"    ... ve {len(hata) - 5} hata daha")
    return [o for o, _, h in s if not h], len(hata)


def calistir(kok):
    if not os.path.exists(AYAR):
        sys.exit("Önce hesapları oluşturun: python3 test/sinav_yuk_testi.py hazirla 40 <cmid>")
    with open(AYAR, encoding="utf-8") as f:
        a = json.load(f)
    print(f"Hedef: {kok} | sınav: {a['sinav']} (cmid {a['cmid']}) | {a['adet']} öğrenci\n")
    ogr = [Ogrenci(f"yuk{i:02d}", a["sifre"], kok, a["cmid"]) for i in range(1, a["adet"] + 1)]
    hata, t0 = 0, time.time()
    for ad, is_ in (("Giriş", Ogrenci.giris), ("Sınavı başlatma", Ogrenci.baslat)):
        ogr, h = asama(ad, ogr, is_)
        hata += h
    no = 1
    while ogr and any(o.sayfa >= 0 for o in ogr):
        kalan = [o for o in ogr if o.sayfa >= 0]
        bitmis = [o for o in ogr if o.sayfa < 0]
        kalan, h1 = asama(f"Sayfa {no} açma", kalan, Ogrenci.sayfa_ac)
        kalan, h2 = asama(f"Sayfa {no} kontrol", kalan, Ogrenci.kontrol) if kalan else ([], 0)
        ogr, hata, no = bitmis + kalan, hata + h1 + h2, no + 1
    if ogr:
        ogr, h = asama("Teslim", ogr, Ogrenci.bitir)
        hata += h
    print(f"\nToplam {time.time() - t0:.1f}s | {len(ogr)}/{a['adet']} öğrenci sınavı sorunsuz bitirdi | {hata} hata")
    return 1 if hata else 0


if __name__ == "__main__":
    islem = sys.argv[1] if len(sys.argv) > 1 else ""
    if islem == "hazirla" and len(sys.argv) == 4:
        sifre = secrets.token_urlsafe(9) + "#Aa1"
        bilgi = php("olustur", int(sys.argv[2]), int(sys.argv[3]), sifre)
        os.makedirs(os.path.dirname(AYAR), exist_ok=True)
        with open(AYAR, "w", encoding="utf-8") as f:
            json.dump({**bilgi, "sifre": sifre}, f, ensure_ascii=False)
        print(f"{bilgi['adet']} hesap hazır (yuk01..), kurs: {bilgi['kurs']}, sınav: {bilgi['sinav']}")
    elif islem == "calistir":
        sys.exit(calistir((sys.argv[2] if len(sys.argv) > 2 else env_adresi()).rstrip("/")))
    elif islem == "temizle":
        print(php("sil"))
        if os.path.exists(AYAR):
            os.remove(AYAR)
    else:
        sys.exit(__doc__)
