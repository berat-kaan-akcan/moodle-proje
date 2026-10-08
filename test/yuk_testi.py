#!/usr/bin/env python3
"""Eşzamanlı yük testi.
  python3 test/yuk_testi.py sayfa http://10.42.0.1:8080 50     # giriş sayfasına 50 eşzamanlı istek
  docker compose exec -T jobe python3 - jobe 50 ANAHTAR < test/yuk_testi.py   # Jobe'a 50 eşzamanlı kod
"""
import json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor


def sayfa(url):
    try:
        with urllib.request.urlopen(url + "/login/index.php", timeout=30) as r:
            r.read()
            return r.status
    except Exception as e:
        return type(e).__name__


def jobe(anahtar):
    istek = urllib.request.Request(
        "http://localhost/jobe/index.php/restapi/runs",
        json.dumps({"run_spec": {"language_id": "python3", "sourcecode": "print(sum(range(1000000)))"}}).encode(),
        {"Content-Type": "application/json", "X-API-KEY": anahtar})
    try:
        with urllib.request.urlopen(istek, timeout=60) as r:
            return json.load(r)["outcome"]  # 15 = başarılı
    except Exception as e:
        return type(e).__name__


mod = sys.argv[1]
n = int(sys.argv[3] if mod == "sayfa" else sys.argv[2])
arg = sys.argv[2] if mod == "sayfa" else sys.argv[3]
hedef = (lambda _: sayfa(arg)) if mod == "sayfa" else (lambda _: jobe(arg))


def olc(i):
    t = time.time()
    return hedef(i), time.time() - t


with ThreadPoolExecutor(n) as ex:
    s = list(ex.map(olc, range(n)))
d = [x for x, _ in s]
t = sorted(x for _, x in s)
print("sonuçlar:", {k: d.count(k) for k in set(d)})
print(f"en hızlı {t[0]:.2f}s | ortanca {t[len(t)//2]:.2f}s | en yavaş {t[-1]:.2f}s")
