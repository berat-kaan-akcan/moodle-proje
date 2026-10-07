# Soru Yazım Kılavuzu (CodeRunner + Python)

Bu kılavuz, bir Python sorusunun **nasıl yazılacağını**, hangi araçla hangi alanın doldurulacağını ve XML dosyasındaki her alanın ne işe yaradığını anlatır. Üç yol var:

| Yol | Ne zaman |
|---|---|
| **A. `sorular.py` ile (önerilen)** | Çok soru, otomatik doğrulama, toplu XML. Beklenen çıktıyı elle yazmazsınız. |
| **B. Moodle arayüzü ile elle** | Tek bir soruyu hızlıca eklemek |
| **C. XML'i doğrudan yazmak** | Başka bir araçtan üretmek, ince ayar |

---

## 1. Önce karar: Hangi soru türü?

Moodle'da soru türü olarak **CodeRunner** kullanılır, dil olarak **`python3`** seçilir. Python 3 sorusunun iki biçimi var:

| | **Program** (`stdin → stdout`) | **Fonksiyon / sınıf** |
|---|---|---|
| Öğrenci ne yazar? | `input()` ile okuyup `print()` eden tam program | Yalnızca `def f(...)` veya `class ...` |
| Test girdisi nerede? | **Stdin** (Input) alanında | **Test code** alanında (`print(f(3))` gibi) |
| Ne zaman? | Girdi/çıktı, döngü, formatlama (Aşama 1–3) | Fonksiyon, koleksiyonlar, OOP (Aşama 2–6) |
| Beklenen çıktı | Programın `print` ettikleri | Test kodunun `print` ettikleri |

**Seçim kuralı:** "Klavyeden oku" diyorsanız → program. "`f(x)` fonksiyonunu yazın" diyorsanız → fonksiyon. Bunun dışında **soru türü her ikisinde de `python3`**'tür. Fark yalnızca testlerin nerede yazıldığıdır.

### Moodle bu testi nasıl çalıştırır?

```
[öğrencinin kodu]
[test code]          ← fonksiyon sorularında; program sorularında boş
```
Bu dosya Jobe'ta `python3` ile çalıştırılır; stdin varsa verilir. **stdout, beklenen çıktıyla satır satır karşılaştırılır** (satır sonu boşlukları yok sayılır). Eşit değilse test kırmızıdır.

---

## 2. Bir sorunun parçaları

| Parça | Anlamı | Örnek |
|---|---|---|
| **Ad** | Soru bankasında görünen isim | `s3_asal - Asal mı?` |
| **Soru metni** | Öğrenciye görünür, HTML | "`asal_mi(n)` fonksiyonunu yazın…" |
| **Soru türü** | CodeRunner → `python3` | |
| **Örnek çözüm** | Doğru referans çözüm (öğrenciye görünmez) | `def asal_mi(n): …` |
| **Test case'ler** | Girdi + beklenen çıktı + görünürlük | aşağıda |
| **Puan** | Soru notu | 15 |
| **Ceza rejimi** | Her yanlış denemede puan kesintisi | `10, 20, ...` (%10, %20 …) |
| **Cevap kutusu satırı** | Editör yüksekliği | 18 |

### Test case'in alanları

| Alan | Anlamı |
|---|---|
| **Test code** | Fonksiyon sorularında çağrı: `print(asal_mi(7))`. Program sorularında boş. |
| **Stdin** | Program sorularında klavye girdisi. Satırlar `\n` ile ayrılır. |
| **Expected** | Tam olarak beklenen çıktı (birden çok satır olabilir) |
| **Display** | `SHOW` (öğrenci görür) / `HIDE` (gizli test) |
| **Use as example** | Soru sayfasında örnek olarak da göster |
| **Mark** | Test ağırlığı (varsayılan 1) |

> **Altın kural:** Her sorunun **ilk 1–2 testi görünür** (öğrenci neyin beklendiğini anlasın), geri kalan **gizli** olmalıdır. Aksi halde `if n == 7: return True` gibi hileler geçer.

---

## 3. Yol A — `sorular.py` ile yazmak (önerilen)

Tüm sorular [sorular.py](sorular.py) içinde tek formatta tanımlıdır. Beklenen çıktıları **siz yazmazsınız**: referans çözüm çalıştırılarak üretilir, böylece elle hata yapılmaz.

### A1. Fonksiyon sorusu şablonu

```python
q(id="s3_toplam", asama=3, baslik="1'den n'e toplam", tur="fonksiyon",
  metin="`toplam(n)` fonksiyonu 1'den n'e kadar olan sayıların toplamını döndürsün. `n < 1` ise `0`.",
  cozum="def toplam(n):\n    t = 0\n    for i in range(1, n + 1):\n        t += i\n    return t\n",
  testler=[f"print(toplam({n}))" for n in (1, 5, 10, 100, 0, -3, 1000)],
  yanlislar=["def toplam(n):\n    t=0\n    for i in range(1,n):\n        t+=i\n    return t\n"])
```

* `tur="fonksiyon"`
* `testler`: her eleman bir **test kodu** (`print(...)` ile bitmeli)
* `cozum`: doğru referans çözüm
* `yanlislar`: **bilerek hatalı** çözümler. Test seti bunları yakalamak zorundadır. (Bu, "testlerim yeterince sıkı mı?" kontrolüdür.)

### A2. Program (stdin) sorusu şablonu

```python
q(id="s1_topla", asama=1, baslik="İki sayının toplamı", tur="program",
  metin="Klavyeden iki tam sayı (ayrı satırlarda) okuyun ve toplamlarını yazdırın.",
  cozum="a = int(input())\nb = int(input())\nprint(a + b)\n",
  testler=["3\n4\n", "-5\n5\n", "0\n0\n", "1000000\n2345678\n"],
  yanlislar=["a=int(input())\nb=int(input())\nprint(a-b)\n"])
```

* `tur="program"`
* `testler`: her eleman **stdin metni** (satır sonları `\n`)

### A3. Çok satırlı test (nesne kullanımı)

Fonksiyon sorularında `testler` elemanı çok satırlı olabilir:

```python
testler=["h = Hesap('ali', 100)\nh.cek(30)\nprint(h)",
         "h = Hesap('x', 10)\ntry:\n    h.cek(50)\nexcept ValueError as e:\n    print(e)\nprint(h)"]
```

### A4. Özel durumlar

| İstek | Nasıl |
|---|---|
| Girdiyi değiştirmeme kontrolü | Test: `l=[1,1,2]\ntekrarsiz(l)\nprint(l)` |
| Performans (naif çözüm zaman aşımına düşsün) | Büyük girdi: `print(fib(80))` |
| Yasak yöntemi yakalamak (`in`, `index`) | Erişimi sayan sarmalayıcı nesne (`SAYAC`, bkz. `s6_ikili_arama`) |
| Puan | `puan=15` (varsayılan 10) |

### A5. Üret ve doğrula

```bash
cd python-sinav
python3 uret.py                 # doğrula + XML üret
python3 uret.py --sadece-dogrula
```

Doğrulayıcı kontrolleri:
1. Referans çözüm her testte çalışıyor mu (hata/zaman aşımı yok)?
2. En az **5 test**, çıktılarda en az **2 farklı değer** var mı?
3. **Her hatalı çözüm en az bir testte yakalanıyor mu?** Yakalanmıyorsa test seti zayıftır.
4. Final paketleri tam **100 puan** mı?

Çıktılar: `cikti/*.xml` (Moodle'a yüklenecek) ve `CEVAP_ANAHTARI.md` (hoca için).

---

## 4. Yol B — Moodle arayüzünde elle oluşturma

1. Kurs → **Daha fazla → Soru bankası** → kategoriyi seçin → **Yeni soru oluştur**.
2. Listeden **CodeRunner** → **Ekle**.
3. Alanları doldurun:

| Alan | Ne yazılır |
|---|---|
| **Question type** | `python3` (program ve fonksiyon sorularının ikisi için de) |
| **Question name** | `s3_asal - Asal mı?` |
| **Question text** | Soru açıklaması (HTML/Markdown düz metin) |
| **Default mark** | 15 |
| **Penalty regime** | `10, 20, ...` |
| **Answer box lines** | 18 |

4. **Customisation** başlığı **kapalı** kalsın (şablonu değiştirmeyin).
5. **Test cases** bölümü:
   * **Fonksiyon sorusu:** `Test` sütununa `print(asal_mi(7))`, `Expected` sütununa `True`.
   * **Program sorusu:** `Test` boş, **Standard input** sütununa `3\n4`, `Expected` sütununa `7`.
   * `Show` sütunu: `Show` ya da `Hide`. **Use as example** ✔: öğrenciye örnek olarak da gösterir.
   * Daha fazla test için **Add another test case**.
6. **Sample answer** kutusuna doğru çözümü yazın.
7. **Kaydet**. Sonra **Önizle** ile önce doğru, sonra yanlış çözümü deneyin.

> Test sütunları görünmüyorsa Moodle "Advanced customisation"u açın: *Show test case column "Standard input"*. Program sorularında Stdin sütunu kullanılır.

---

## 5. Yol C — XML'i doğrudan yazmak

### Dosyanın iskeleti

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <!-- 1) Kategori satırı: sonraki sorular bu kategoriye girer -->
  <question type="category">
    <category><text>$course$/top/Python Sinav/Asama 3 - Döngüler</text></category>
  </question>

  <!-- 2) Sorular -->
  <question type="coderunner"> ... </question>
  <question type="coderunner"> ... </question>
</quiz>
```

> Kategori adında `/` kullanmayın (alt kategoriye bölünür). Ağaç ayırıcısı yalnızca `top/Python Sinav/...` içindeki `/`'lardır.

### Tek bir fonksiyon sorusu (özet alanlarla)

```xml
<question type="coderunner">
  <name><text>s3_asal - Asal mı?</text></name>
  <questiontext format="html"><text><![CDATA[<p><code>asal_mi(n)</code> fonksiyonunu yazın.</p>]]></text></questiontext>
  <defaultgrade>15</defaultgrade>
  <penalty>0.1</penalty>
  <coderunnertype>python3</coderunnertype>     <!-- soru türü -->
  <prototypetype>0</prototypetype>             <!-- 0 = normal soru -->
  <allornothing>0</allornothing>               <!-- 0 = testlere oransal puan -->
  <penaltyregime>10, 20, ...</penaltyregime>
  <precheck>0</precheck>
  <showsource>0</showsource>
  <answerboxlines>18</answerboxlines>
  <useace>1</useace>                           <!-- kod editörü -->
  <answer><![CDATA[def asal_mi(n):
    ...
]]></answer>                                   <!-- örnek çözüm -->
  <validateonsave>1</validateonsave>           <!-- kaydederken örnek çözümü test et -->
  <testcases>
    <testcase testtype="0" useasexample="1" hiderestiffail="0" mark="1.0">
      <testcode><text><![CDATA[print(asal_mi(7))]]></text></testcode>
      <stdin><text></text></stdin>
      <expected><text>True</text></expected>
      <extra><text></text></extra>
      <display><text>SHOW</text></display>
    </testcase>
    <testcase testtype="0" useasexample="0" hiderestiffail="0" mark="1.0">
      <testcode><text><![CDATA[print(asal_mi(1))]]></text></testcode>
      <stdin><text></text></stdin>
      <expected><text>False</text></expected>
      <extra><text></text></extra>
      <display><text>HIDE</text></display>
    </testcase>
  </testcases>
</question>
```

### Program (stdin) sorusunda fark

Yalnızca testcase içinde: `testcode` boş, `stdin` dolu.

```xml
<testcase testtype="0" useasexample="1" hiderestiffail="0" mark="1.0">
  <testcode><text></text></testcode>
  <stdin><text><![CDATA[3
4
]]></text></stdin>
  <expected><text>7</text></expected>
  <extra><text></text></extra>
  <display><text>SHOW</text></display>
</testcase>
```

### Alan sözlüğü

| XML etiketi | Anlamı | Değerler |
|---|---|---|
| `<coderunnertype>` | Soru türü / dil | `python3` |
| `<defaultgrade>` | Soru puanı | sayı |
| `<penalty>` | Yanlış deneme başına ceza | `0.1` = %10 |
| `<penaltyregime>` | Ceza dizisi | `10, 20, ...` |
| `<allornothing>` | `1`: tüm testler geçmedikçe 0 puan · `0`: test başına oransal | `0` önerilir |
| `<precheck>` | `1` ise "Ön kontrol" düğmesi ek olarak çıkar | `0` |
| `<showsource>` | Gönderilen tam kodu geri bildirimde göster | `0` |
| `<answer>` | Örnek çözüm | kod |
| `<testcode>` | Fonksiyon sorularında test kodu | `print(f(2))` |
| `<stdin>` | Program girdisi | metin |
| `<expected>` | Beklenen stdout | metin |
| `<display>` | `SHOW` / `HIDE` | |
| `useasexample` | Soru sayfasında örnek olarak göster | `1`/`0` |
| `hiderestiffail` | Bu test başarısız olursa kalanları gizle | `0` |
| `mark` | Test ağırlığı | `1.0` |

> **CDATA:** Kod ve çok satırlı metinleri `<![CDATA[ ... ]]>` içine alın. `<`, `&` gibi karakterler bozulmaz.

---

## 6. İyi test seti nasıl yazılır?

Her soru için şu kategorilerden **en az 5 test**:

| Tür | Örnek (`asal_mi`) |
|---|---|
| **Tipik** | 7, 17, 100 |
| **En küçük/sınır** | 0, 1, 2 |
| **Negatif/geçersiz** | -7 |
| **Özel yapı** | Tam kare (25), büyük asal (7919) |
| **Hile engeli** | Ezberlemeyi önlemek için gizli, farklı değerler |

Hatalı çözüm yazma alışkanlığı kazanın: *"Öğrencilerin yapacağı tipik hata nedir?"* → onu `yanlislar=[...]` içine koyun. Test seti onu yakalamıyorsa **yeni test ekleyin**.

Tipik hata → test eşlemesi:

| Tipik hata | Yakalayan test |
|---|---|
| `range(1, n)` (son dahil değil) | küçük `n` (1, 5) |
| `>` yerine `>=` | sınır değer (89/90) |
| Büyük/küçük harf duyarlılığı | `"Aa"` gibi karışık harf |
| Girdi listesini değiştirmek | testte listeyi yazdırarak kontrol |
| Boş koleksiyonda çökme | `[]`, `""`, `{}` |
| `sorted()` yasağını çiğnemek | **kod incelemesi** gerekir (CodeRunner çıktıya bakar). Gerekirse erişim sayacı gibi hile testi |

---

## 7. Bilinen tuzaklar

1. **Boş stdin:** Yalnızca boşluk/satır sonundan oluşan girdi, boş girdiye dönüşür. `input()` EOF hatası verir. Program sorularında boş satır testi koymayın.
2. **Çıktı biçimi:** `print(f"{x:.2f}")` gibi biçimi sorunun metninde açık yazın ("iki ondalık"). Aksi halde öğrenci doğru yapsa da kırmızı alır.
3. **Sıralama belirsizliği:** Küme/sözlük çıktısı sırasızdır. Sıra gerekiyorsa soruda "alfabetik sırada yazdırın" deyin ya da testte `sorted(...)` kullanın.
4. **Kayan nokta:** `0.1+0.2` gibi eşitlik testlerinden kaçının; `round()` ya da `.2f` kullanın.
5. **Zaman aşımı:** Jobe varsayılan ~5 sn limitiyle çalışır. Performans testi koyuyorsanız referans çözümün bunun çok altında bitmesi gerekir.
6. **Aynı XML'i iki kez yüklemek** soruları çoğaltır.

---

## 8. Sık yapılan işler

| İş | Komut/yer |
|---|---|
| Yeni soru ekle | `sorular.py` sonuna `q(...)` ekle → `python3 uret.py` |
| Yeni soruyu sınav paketine koy | `sorular.py` → `SINAVLAR` içine id + puan; toplam 100 olmalı |
| Soruyu Moodle'a yükle | Soru bankası → Import → `cikti/tum_havuz.xml` (bkz. [YOL_HARITASI.md](YOL_HARITASI.md) Adım 1) |
| Cevap anahtarı | `CEVAP_ANAHTARI.md` (otomatik güncellenir) |
