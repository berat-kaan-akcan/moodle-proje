#!/usr/bin/env python3
"""Soru havuzunu doğrular ve Moodle/CodeRunner XML + cevap anahtarı üretir.

Kullanım:  python3 uret.py          (doğrula + üret)
           python3 uret.py --sadece-dogrula
"""
import subprocess, sys, tempfile, os, html
from pathlib import Path
from sorular import S, ASAMALAR, SINAVLAR

KOK = Path(__file__).parent
CIKTI = KOK / "cikti"
ZAMAN = 5


def calistir(kod, stdin=""):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "k.py"
        p.write_text(kod, encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-I", str(p)], input=stdin, capture_output=True,
                               text=True, timeout=ZAMAN, cwd=d)
        except subprocess.TimeoutExpired:
            return "__ZAMAN_ASIMI__"
    return (r.stdout if r.returncode == 0 else f"__HATA__ {r.stderr.strip().splitlines()[-1:]}")


def norm(s):
    return "\n".join(l.rstrip() for l in s.rstrip().split("\n"))


def tam_kod(soru, kod, test):
    return (kod, test) if soru["tur"] == "program" else (kod + "\n" + test + "\n", "")


def beklenenler(soru):
    out = []
    for t in soru["testler"]:
        k, si = tam_kod(soru, soru["cozum"], t)
        o = calistir(k, si)
        if o.startswith("__"):
            sys.exit(f"HATA: {soru['id']} referans çözümü başarısız: {o}")
        out.append(norm(o))
    return out


def dogrula():
    hata = 0
    ids = set()
    for s in S:
        assert s["id"] not in ids, f"yinelenen id {s['id']}"
        ids.add(s["id"])
        exp = beklenenler(s)
        if len(s["testler"]) < 5:
            print(f"UYARI {s['id']}: test sayısı < 5"); hata += 1
        if len(set(exp)) < 2:
            print(f"UYARI {s['id']}: beklenen çıktılar çok benzer (zayıf test seti)"); hata += 1
        if not s["yanlislar"]:
            print(f"UYARI {s['id']}: hatalı çözüm örneği yok"); hata += 1
        for i, y in enumerate(s["yanlislar"]):
            yakalandi = 0
            for t, e in zip(s["testler"], exp):
                k, si = tam_kod(s, y, t)
                if norm(calistir(k, si)) != e:
                    yakalandi += 1
            if not yakalandi:
                print(f"HATA {s['id']}: yanlış çözüm #{i} hiçbir testte yakalanmadı"); hata += 1
        print(f"  ok  {s['id']:<18} {len(s['testler'])} test, yanlış çözümler yakalandı")
    kimlik = {s["id"] for s in S}
    for p, sorular in SINAVLAR.items():
        assert sum(sorular.values()) == 100, f"paket {p} 100 puan değil"
        assert set(sorular) <= kimlik, f"paket {p}: bilinmeyen soru"
    return hata


def cdata(x):
    return "<![CDATA[" + x.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def metin_html(m):
    """Basit markdown -> html (kod bloğu, satır içi kod, kalın, liste)."""
    out, kod, liste = [], False, False
    for satir in m.split("\n"):
        if satir.startswith("```"):
            out.append("</pre>" if kod else "<pre>"); kod = not kod; continue
        if kod:
            out.append(html.escape(satir)); continue
        e = html.escape(satir)
        import re
        e = re.sub(r"`([^`]+)`", r"<code>\1</code>", e)
        e = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", e)
        if e.startswith("* "):
            if not liste: out.append("<ul>"); liste = True
            out.append(f"<li>{e[2:]}</li>"); continue
        if liste: out.append("</ul>"); liste = False
        out.append(f"<p>{e}</p>" if e.strip() else "")
    if liste: out.append("</ul>")
    return "\n".join(out)


def soru_xml(s, exp, puan, ek=""):
    n = len(s["testler"])
    gorunen = 2 if n > 3 else 1
    tc = []
    for i, (t, e) in enumerate(zip(s["testler"], exp)):
        goster = i < gorunen
        if s["tur"] == "program":
            kod, stdin = "", t
        else:
            kod, stdin = t, ""
        tc.append(f'''   <testcase testtype="0" useasexample="{1 if goster else 0}" hiderestiffail="0" mark="1.0000000">
    <testcode><text>{cdata(kod)}</text></testcode>
    <stdin><text>{cdata(stdin)}</text></stdin>
    <expected><text>{cdata(e)}</text></expected>
    <extra><text></text></extra>
    <display><text>{"SHOW" if goster else "HIDE"}</text></display>
   </testcase>''')
    etiket = {"program": "stdin/stdout programı", "fonksiyon": "fonksiyon/sınıf"}[s["tur"]]
    return f'''  <question type="coderunner">
   <name><text>{html.escape(s["id"] + " - " + s["baslik"] + ek)}</text></name>
   <questiontext format="html"><text>{cdata(metin_html(s["metin"]))}</text></questiontext>
   <generalfeedback format="html"><text></text></generalfeedback>
   <defaultgrade>{puan}</defaultgrade>
   <penalty>0.1</penalty>
   <hidden>0</hidden>
   <coderunnertype>python3</coderunnertype>
   <prototypetype>0</prototypetype>
   <allornothing>0</allornothing>
   <penaltyregime>10, 20, ...</penaltyregime>
   <precheck>0</precheck>
   <hidecheck>0</hidecheck>
   <showsource>0</showsource>
   <answerboxlines>18</answerboxlines>
   <answerboxcolumns>100</answerboxcolumns>
   <answerpreload></answerpreload>
   <globalextra></globalextra>
   <useace>1</useace>
   <resultcolumns></resultcolumns>
   <template></template>
   <iscombinatortemplate></iscombinatortemplate>
   <allowmultiplestdins></allowmultiplestdins>
   <answer>{cdata(s["cozum"])}</answer>
   <validateonsave>1</validateonsave>
   <testsplitterre></testsplitterre>
   <language></language>
   <acelang></acelang>
   <sandbox></sandbox>
   <grader></grader>
   <cputimelimitsecs></cputimelimitsecs>
   <memlimitmb></memlimitmb>
   <sandboxparams></sandboxparams>
   <testcases>
{chr(10).join(tc)}
   </testcases>
  </question>'''


def kategori(yol):
    return f'''  <question type="category">
   <category><text>$course$/top/{yol}</text></category>
  </question>'''


def xml_yaz(ad, parcalar):
    (CIKTI / ad).write_text('<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n' + "\n".join(parcalar) + "\n</quiz>\n", encoding="utf-8")


def uret():
    CIKTI.mkdir(exist_ok=True)
    beklenen = {s["id"]: beklenenler(s) for s in S}
    kimlik = {s["id"]: s for s in S}
    tum = []
    for a, baslik in ASAMALAR.items():
        p = [kategori(f"Python Sinav/Asama {a} - {baslik}")]
        p += [soru_xml(s, beklenen[s["id"]], s["puan"]) for s in S if s["asama"] == a]
        xml_yaz(f"asama{a}.xml", p)
        tum += p
    xml_yaz("tum_havuz.xml", tum)
    for paket, sorular in SINAVLAR.items():
        p = [kategori(f"Python Sinav/Final - Paket {paket}")]
        p += [soru_xml(kimlik[i], beklenen[i], pt, f" [Paket {paket}]") for i, pt in sorular.items()]
        xml_yaz(f"final_paket_{paket}.xml", p)
    # öğretmen cevap anahtarı
    md = ["# Cevap Anahtarı (yalnızca hoca)\n", "Referans çözümler ve test case'ler. Beklenen çıktılar çözümlerden otomatik üretilmiştir.\n"]
    for a, baslik in ASAMALAR.items():
        md.append(f"\n## Aşama {a} — {baslik}\n")
        for s in S:
            if s["asama"] != a: continue
            md.append(f"### {s['id']} — {s['baslik']} ({s['tur']}, {s['puan']} puan)\n")
            md.append(s["metin"] + "\n")
            md.append("```python\n" + s["cozum"] + "```\n")
            md.append("| # | Girdi / çağrı | Beklenen | Görünür |\n|---|---|---|---|")
            for i, (t, e) in enumerate(zip(s["testler"], beklenen[s["id"]])):
                f = lambda x: "`" + x.replace("\n", "⏎").replace("|", "\\|") + "`" if x else "_(boş)_"
                md.append(f"| {i+1} | {f(t)} | {f(e)} | {'evet' if i < (2 if len(s['testler']) > 3 else 1) else 'gizli'} |")
            md.append("")
    md.append("\n## Sınav paketleri\n")
    for paket, sorular in SINAVLAR.items():
        md.append(f"* **Paket {paket}**: " + ", ".join(f"{i} ({pt})" for i, pt in sorular.items()))
    (KOK / "CEVAP_ANAHTARI.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nÜretildi: {CIKTI}/ (asama1-6.xml, tum_havuz.xml, final_paket_A-D.xml) ve CEVAP_ANAHTARI.md")


if __name__ == "__main__":
    print("Doğrulama:")
    h = dogrula()
    print(f"\n{len(S)} soru, {sum(len(s['testler']) for s in S)} test case, uyarı/hata: {h}")
    if h:
        sys.exit(1)
    if "--sadece-dogrula" not in sys.argv:
        uret()
