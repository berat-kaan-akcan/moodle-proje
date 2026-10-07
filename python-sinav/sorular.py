"""Python sınav soru havuzu.

Her soru:
  id, asama, baslik, metin, tur ('program' = stdin/stdout, 'fonksiyon' = testcode),
  cozum (referans çözüm), testler, puan, yanlislar (bilerek hatalı çözümler; test seti bunları yakalamalı)

'program'  testleri: stdin metni listesi
'fonksiyon' testleri: testcode metni listesi (print(...) dahil)
Beklenen çıktılar referans çözüm çalıştırılarak otomatik üretilir.
"""

ASAMALAR = {
    1: "Temeller: girdi, çıktı, aritmetik",
    2: "Koşullar (if-elif-else)",
    3: "Döngüler (for-while)",
    4: "Fonksiyonlar ve string işlemleri",
    5: "Liste, sözlük, küme, matris",
    6: "Özyineleme, istisna, OOP, algoritmalar",
}

S = []


def q(**k):
    k.setdefault("yanlislar", [])
    k.setdefault("puan", 10)
    S.append(k)


# ---------------------------------------------------------------- AŞAMA 1
q(id="s1_topla", asama=1, baslik="İki sayının toplamı", tur="program",
  metin="Klavyeden iki tam sayı (her biri ayrı satırda) okuyun ve toplamlarını yazdırın.",
  cozum="a = int(input())\nb = int(input())\nprint(a + b)\n",
  testler=["3\n4\n", "-5\n5\n", "0\n0\n", "1000000\n2345678\n", "-7\n-8\n"],
  yanlislar=["a=int(input())\nb=int(input())\nprint(a-b)\n"])

q(id="s1_ortalama", asama=1, baslik="Not ortalaması", tur="program",
  metin="Üç vize notunu (ayrı satırlarda, tam sayı) okuyun. Ortalamalarını **iki ondalık basamakla** yazdırın.\n\nÖrnek: 70, 80, 85 → `78.33`",
  cozum="a = int(input())\nb = int(input())\nc = int(input())\nprint(f'{(a + b + c) / 3:.2f}')\n",
  testler=["70\n80\n85\n", "100\n100\n100\n", "0\n0\n1\n", "55\n60\n65\n", "99\n98\n97\n"],
  yanlislar=["a=int(input())\nb=int(input())\nc=int(input())\nprint((a+b+c)//3)\n"])

q(id="s1_daire", asama=1, baslik="Dairenin alanı", tur="program",
  metin="Yarıçapı (ondalık sayı olabilir) okuyun. Dairenin alanını `math.pi` kullanarak **iki ondalık basamakla** yazdırın.",
  cozum="import math\nr = float(input())\nprint(f'{math.pi * r * r:.2f}')\n",
  testler=["1\n", "2.5\n", "0\n", "10\n", "0.1\n"],
  yanlislar=["r=float(input())\nprint(f'{3.14*r*r:.2f}')\n"])

q(id="s1_saniye", asama=1, baslik="Saniyeyi çevir", tur="program",
  metin="Saniye cinsinden bir süre okuyun. Bunu `S saat M dakika N saniye` biçiminde yazdırın.\n\nÖrnek: `3725` → `1 saat 2 dakika 5 saniye`",
  cozum="t = int(input())\nprint(f'{t // 3600} saat {t % 3600 // 60} dakika {t % 60} saniye')\n",
  testler=["3725\n", "0\n", "59\n", "3600\n", "86399\n", "7322\n"],
  yanlislar=["t=int(input())\nprint(f'{t//3600} saat {t//60} dakika {t%60} saniye')\n"])

q(id="s1_bolme", asama=1, baslik="Bölüm ve kalan", tur="program",
  metin="İki pozitif tam sayı `a` ve `b` okuyun (ayrı satırlarda). Tek satırda `a // b` ve `a % b` değerlerini boşlukla ayırarak yazdırın.",
  cozum="a = int(input())\nb = int(input())\nprint(a // b, a % b)\n",
  testler=["17\n5\n", "10\n2\n", "3\n7\n", "100\n9\n", "1\n1\n"],
  yanlislar=["a=int(input())\nb=int(input())\nprint(a/b, a%b)\n"])

# ---------------------------------------------------------------- AŞAMA 2
q(id="s2_ciftmi", asama=2, baslik="Çift mi tek mi?", tur="program",
  metin="Bir tam sayı okuyun. Çift ise `cift`, tek ise `tek` yazdırın. (Negatif sayılar ve sıfır dahil.)",
  cozum="n = int(input())\nprint('cift' if n % 2 == 0 else 'tek')\n",
  testler=["4\n", "7\n", "0\n", "-3\n", "-8\n", "1\n"],
  yanlislar=["n=int(input())\nprint('cift' if n%2==0 and n>0 else 'tek')\n"])

q(id="s2_artikyil", asama=2, baslik="Artık yıl", tur="fonksiyon",
  metin="`artik_mi(yil)` fonksiyonunu yazın. Yıl artık ise `True`, değilse `False` döndürsün.\n\nKural: 4'e bölünür **ama** 100'e bölünmez, **ya da** 400'e bölünür.",
  cozum="def artik_mi(yil):\n    return (yil % 4 == 0 and yil % 100 != 0) or yil % 400 == 0\n",
  testler=[f"print(artik_mi({y}))" for y in (2024, 2023, 1900, 2000, 2100, 1996, 1)],
  yanlislar=["def artik_mi(yil):\n    return yil % 4 == 0\n"])

q(id="s2_harf", asama=2, baslik="Harf notu", tur="fonksiyon",
  metin="`harf(not_)` fonksiyonunu yazın:\n\n* 90–100 → `AA`\n* 80–89 → `BA`\n* 70–79 → `BB`\n* 60–69 → `CB`\n* 50–59 → `CC`\n* 0–49 → `FF`\n* 0'dan küçük veya 100'den büyük → `Gecersiz`",
  cozum=("def harf(not_):\n    if not_ < 0 or not_ > 100:\n        return 'Gecersiz'\n    if not_ >= 90:\n        return 'AA'\n"
         "    if not_ >= 80:\n        return 'BA'\n    if not_ >= 70:\n        return 'BB'\n    if not_ >= 60:\n        return 'CB'\n"
         "    if not_ >= 50:\n        return 'CC'\n    return 'FF'\n"),
  testler=[f"print(harf({n}))" for n in (95, 90, 89, 80, 79, 70, 69, 60, 59, 50, 49, 0, -1, 101, 100)],
  yanlislar=["def harf(not_):\n    if not_>90: return 'AA'\n    if not_>80: return 'BA'\n    if not_>70: return 'BB'\n    if not_>60: return 'CB'\n    if not_>50: return 'CC'\n    return 'FF'\n"])

q(id="s2_ucgen", asama=2, baslik="Üçgen türü", tur="fonksiyon",
  metin="`ucgen_turu(a, b, c)` fonksiyonunu yazın. Kenar uzunluklarına göre döndürün:\n\n* Üçgen oluşmuyorsa (herhangi bir kenar ≤ 0 ya da en uzun kenar ≥ diğer ikisinin toplamı) → `Gecersiz`\n* üç kenar eşitse → `Eskenar`\n* iki kenar eşitse → `Ikizkenar`\n* hiçbiri eşit değilse → `Caliskenar`",
  cozum=("def ucgen_turu(a, b, c):\n    if min(a, b, c) <= 0 or max(a, b, c) >= a + b + c - max(a, b, c):\n        return 'Gecersiz'\n"
         "    if a == b == c:\n        return 'Eskenar'\n    if a == b or b == c or a == c:\n        return 'Ikizkenar'\n    return 'Caliskenar'\n"),
  testler=["print(ucgen_turu(3, 3, 3))", "print(ucgen_turu(3, 3, 4))", "print(ucgen_turu(3, 4, 5))", "print(ucgen_turu(1, 2, 3))",
           "print(ucgen_turu(0, 4, 4))", "print(ucgen_turu(5, 5, 10))", "print(ucgen_turu(4, 5, 4))", "print(ucgen_turu(10, 1, 1))",
           "print(ucgen_turu(-1, 2, 2))"],
  yanlislar=["def ucgen_turu(a,b,c):\n    if a==b==c: return 'Eskenar'\n    if a==b or b==c or a==c: return 'Ikizkenar'\n    return 'Caliskenar'\n"])

q(id="s2_enbuyuk", asama=2, baslik="En büyük, en küçük", tur="program",
  metin="Üç tam sayıyı ayrı satırlarda okuyun. `max()` ve `min()` kullanmadan, tek satırda `en_buyuk en_kucuk` biçiminde yazdırın.",
  cozum=("a = int(input())\nb = int(input())\nc = int(input())\nbuyuk = a\nkucuk = a\nfor x in (b, c):\n    if x > buyuk:\n        buyuk = x\n    if x < kucuk:\n        kucuk = x\nprint(buyuk, kucuk)\n"),
  testler=["1\n2\n3\n", "3\n2\n1\n", "5\n5\n5\n", "-1\n-5\n-3\n", "2\n9\n4\n", "0\n-1\n1\n"],
  yanlislar=["a=int(input())\nb=int(input())\nc=int(input())\nprint(a, c)\n"])

# ---------------------------------------------------------------- AŞAMA 3
q(id="s3_toplam", asama=3, baslik="1'den n'e toplam", tur="fonksiyon",
  metin="`toplam(n)` fonksiyonu, **döngü kullanarak** 1'den `n`'e kadar (n dahil) olan sayıların toplamını döndürsün. `n < 1` ise `0` döndürsün.",
  cozum="def toplam(n):\n    t = 0\n    for i in range(1, n + 1):\n        t += i\n    return t\n",
  testler=[f"print(toplam({n}))" for n in (1, 5, 10, 100, 0, -3, 1000)],
  yanlislar=["def toplam(n):\n    t=0\n    for i in range(1,n):\n        t+=i\n    return t\n"])

q(id="s3_faktoriyel", asama=3, baslik="Faktöriyel", tur="fonksiyon",
  metin="`faktoriyel(n)` fonksiyonunu **döngü ile** yazın (`math.factorial` yasak). `0! = 1`. `n` negatifse `-1` döndürün.",
  cozum="def faktoriyel(n):\n    if n < 0:\n        return -1\n    s = 1\n    for i in range(2, n + 1):\n        s *= i\n    return s\n",
  testler=[f"print(faktoriyel({n}))" for n in (0, 1, 5, 10, -2, 15, 20)],
  yanlislar=["def faktoriyel(n):\n    s=1\n    for i in range(1,n):\n        s*=i\n    return s\n"])

q(id="s3_asal", asama=3, baslik="Asal mı?", tur="fonksiyon",
  metin="`asal_mi(n)` fonksiyonu `n` asal ise `True`, değilse `False` döndürsün. (0, 1 ve negatifler asal değildir.)",
  cozum="def asal_mi(n):\n    if n < 2:\n        return False\n    i = 2\n    while i * i <= n:\n        if n % i == 0:\n            return False\n        i += 1\n    return True\n",
  testler=[f"print(asal_mi({n}))" for n in (2, 3, 4, 1, 0, -7, 17, 25, 97, 100, 7919)],
  yanlislar=["def asal_mi(n):\n    if n<2: return False\n    for i in range(2,n//2):\n        if n%i==0: return False\n    return True\n"])

q(id="s3_fizzbuzz", asama=3, baslik="FizzBuzz", tur="program",
  metin="`n` okuyun. 1'den `n`'e kadar her sayıyı ayrı satıra yazdırın; ancak 3'ün katı ise `Fizz`, 5'in katı ise `Buzz`, ikisinin de katı ise `FizzBuzz` yazdırın.",
  cozum="n = int(input())\nfor i in range(1, n + 1):\n    if i % 15 == 0:\n        print('FizzBuzz')\n    elif i % 3 == 0:\n        print('Fizz')\n    elif i % 5 == 0:\n        print('Buzz')\n    else:\n        print(i)\n",
  testler=["1\n", "5\n", "15\n", "20\n", "0\n", "30\n"],
  yanlislar=["n=int(input())\nfor i in range(1,n+1):\n    if i%3==0: print('Fizz')\n    elif i%5==0: print('Buzz')\n    elif i%15==0: print('FizzBuzz')\n    else: print(i)\n"])

q(id="s3_basamak", asama=3, baslik="Basamaklar toplamı", tur="fonksiyon",
  metin="`basamak_toplami(n)` fonksiyonu bir tam sayının basamaklarının toplamını döndürsün. **String'e çevirmeden** (`%` ve `//` ile) yazın. Negatif sayılarda işareti yok sayın.",
  cozum="def basamak_toplami(n):\n    n = abs(n)\n    t = 0\n    while n > 0:\n        t += n % 10\n        n //= 10\n    return t\n",
  testler=[f"print(basamak_toplami({n}))" for n in (123, 0, 9, 1000, -456, 99999, 1234567890)],
  yanlislar=["def basamak_toplami(n):\n    t=0\n    while n>0:\n        t+=n%10\n        n//=10\n    return t\n"])

q(id="s3_ucgen_yildiz", asama=3, baslik="Yıldız üçgeni", tur="program",
  metin="`n` okuyun. Sağa dayalı yıldız üçgeni çizin: `i`. satırda önce `n-i` boşluk, sonra `i` tane `*` olsun.\n\n`n=3` için:\n```\n  *\n **\n***\n```",
  cozum="n = int(input())\nfor i in range(1, n + 1):\n    print(' ' * (n - i) + '*' * i)\n",
  testler=["3\n", "1\n", "5\n", "0\n", "7\n"],
  yanlislar=["n=int(input())\nfor i in range(1,n+1):\n    print('*'*i)\n"])

# ---------------------------------------------------------------- AŞAMA 4
q(id="s4_palindrom", asama=4, baslik="Palindrom", tur="fonksiyon",
  metin="`palindrom_mu(s)` fonksiyonu; büyük/küçük harf ve **boşlukları yok sayarak** metin palindrom ise `True`, değilse `False` döndürsün.\n\nÖrnek: `\"Kay ak\"` → `True`.",
  cozum="def palindrom_mu(s):\n    t = s.replace(' ', '').lower()\n    return t == t[::-1]\n",
  testler=['print(palindrom_mu("kayak"))', 'print(palindrom_mu("Kay ak"))', 'print(palindrom_mu("python"))', 'print(palindrom_mu(""))',
           'print(palindrom_mu("A man a plan a canal Panama"))', 'print(palindrom_mu("ab"))', 'print(palindrom_mu("Aa"))'],
  yanlislar=["def palindrom_mu(s):\n    return s==s[::-1]\n"])

q(id="s4_sesli", asama=4, baslik="Sesli harf sayısı", tur="fonksiyon",
  metin="`sesli_say(s)` fonksiyonu, metindeki sesli harf (`aeıioöuü`, büyük/küçük fark etmez) sayısını döndürsün.",
  cozum="def sesli_say(s):\n    return sum(1 for c in s.lower() if c in 'aeıioöuü')\n",
  testler=['print(sesli_say("merhaba"))', 'print(sesli_say("PYTHON"))', 'print(sesli_say(""))', 'print(sesli_say("ÜÖİ"))',
           'print(sesli_say("kıvırcık"))', 'print(sesli_say("bcdfg"))', 'print(sesli_say("AEIOU"))'],
  yanlislar=["def sesli_say(s):\n    return sum(1 for c in s if c in 'aeiou')\n"])

q(id="s4_kelime", asama=4, baslik="En uzun kelime", tur="program",
  metin="Bir satır metin okuyun (kelimeler boşlukla ayrılmış). Önce kelime sayısını, sonra **en uzun kelimeyi** ayrı satırlarda yazdırın. Eşitlik varsa **ilk** geçen kelime seçilir. Satırda en az bir kelime olacaktır.",
  cozum="kelimeler = input().split()\nprint(len(kelimeler))\nen = ''\nfor k in kelimeler:\n    if len(k) > len(en):\n        en = k\nprint(en)\n",
  testler=["bugun hava cok guzel\n", "a bb ccc dd\n", "tek\n", "bir iki uc dort bes\n", "ab cd ef\n", "  cok   bosluk   var  \n"],
  yanlislar=["k=input().split()\nprint(len(k))\nprint(max(k,key=len) if k else '')\nprint('x')\n"])

q(id="s4_sezar", asama=4, baslik="Sezar şifresi", tur="fonksiyon",
  metin="`sifrele(metin, kaydir)` fonksiyonunu yazın. Yalnızca `a-z` ve `A-Z` harfleri alfabede `kaydir` kadar ileri kaydırılır (z'den sonra a'ya dönülür, büyük/küçük harf korunur). Diğer karakterler **aynen** kalır. `kaydir` negatif olabilir.",
  cozum=("def sifrele(metin, kaydir):\n    sonuc = ''\n    for c in metin:\n        if 'a' <= c <= 'z':\n            sonuc += chr((ord(c) - 97 + kaydir) % 26 + 97)\n"
         "        elif 'A' <= c <= 'Z':\n            sonuc += chr((ord(c) - 65 + kaydir) % 26 + 65)\n        else:\n            sonuc += c\n    return sonuc\n"),
  testler=['print(sifrele("abc", 1))', 'print(sifrele("xyz", 3))', 'print(sifrele("Hello, World!", 5))', 'print(sifrele("abc", 0))',
           'print(sifrele("def", -3))', 'print(sifrele("Python 3.12", 13))', 'print(sifrele("abc", 27))'],
  yanlislar=["def sifrele(metin, kaydir):\n    return ''.join(chr(ord(c)+kaydir) for c in metin)\n"])

q(id="s4_anagram", asama=4, baslik="Anagram", tur="fonksiyon",
  metin="`anagram_mi(a, b)` fonksiyonu iki kelime birbirinin anagramı ise `True` döndürsün. Büyük/küçük harf ve boşluklar yok sayılır.",
  cozum="def anagram_mi(a, b):\n    f = lambda s: sorted(s.replace(' ', '').lower())\n    return f(a) == f(b)\n",
  testler=['print(anagram_mi("listen", "silent"))', 'print(anagram_mi("Dormitory", "dirty room"))', 'print(anagram_mi("abc", "abd"))',
           'print(anagram_mi("aab", "abb"))', 'print(anagram_mi("", ""))', 'print(anagram_mi("abc", "ab"))'],
  yanlislar=["def anagram_mi(a,b):\n    return set(a)==set(b)\n"])

# ---------------------------------------------------------------- AŞAMA 5
q(id="s5_ikinci", asama=5, baslik="İkinci en büyük", tur="fonksiyon",
  metin="`ikinci_buyuk(liste)` fonksiyonu listedeki **farklı** değerler arasında ikinci en büyüğünü döndürsün. Farklı iki değer yoksa `None` döndürsün.",
  cozum="def ikinci_buyuk(liste):\n    s = sorted(set(liste), reverse=True)\n    return s[1] if len(s) >= 2 else None\n",
  testler=["print(ikinci_buyuk([1, 2, 3]))", "print(ikinci_buyuk([5, 5, 5]))", "print(ikinci_buyuk([10, 9, 10, 8]))", "print(ikinci_buyuk([]))",
           "print(ikinci_buyuk([7]))", "print(ikinci_buyuk([-1, -2, -3]))", "print(ikinci_buyuk([2, 1]))"],
  yanlislar=["def ikinci_buyuk(liste):\n    s=sorted(liste,reverse=True)\n    return s[1] if len(s)>=2 else None\n"])

q(id="s5_tekrarsiz", asama=5, baslik="Tekrarları sil", tur="fonksiyon",
  metin="`tekrarsiz(liste)` fonksiyonu, tekrar eden elemanları silip **ilk geçişlerin sırasını koruyarak** yeni bir liste döndürsün. Girdi listesini değiştirmeyin.",
  cozum="def tekrarsiz(liste):\n    gorulen = set()\n    sonuc = []\n    for x in liste:\n        if x not in gorulen:\n            gorulen.add(x)\n            sonuc.append(x)\n    return sonuc\n",
  testler=["print(tekrarsiz([1, 2, 2, 3, 1]))", "print(tekrarsiz([]))", "print(tekrarsiz(['a', 'b', 'a']))", "print(tekrarsiz([3, 3, 3]))",
           "print(tekrarsiz([5, 4, 3]))", "l = [1, 1, 2]\ntekrarsiz(l)\nprint(l)"],
  yanlislar=["def tekrarsiz(liste):\n    return list(set(liste))\n"])

q(id="s5_frekans", asama=5, baslik="Harf frekansı", tur="program",
  metin="Bir satır metin okuyun. Harfleri (küçük harfe çevirerek, boşluk ve diğer karakterleri atlayarak) sayın. Her harfi `harf: adet` biçiminde, **önce adedi çok olan, eşitlikte alfabetik** sırayla ayrı satırlarda yazdırın.",
  cozum=("s = input().lower()\nsayac = {}\nfor c in s:\n    if c.isalpha():\n        sayac[c] = sayac.get(c, 0) + 1\n"
         "for harf, adet in sorted(sayac.items(), key=lambda x: (-x[1], x[0])):\n    print(f'{harf}: {adet}')\n"),
  testler=["banana\n", "Hello World\n", "aabbcc\n", "a\n", "x y z x\n", "123 !!\n", "Python ve Java\n"],
  yanlislar=["s=input().lower()\nd={}\nfor c in s:\n    if c.isalpha(): d[c]=d.get(c,0)+1\nfor k,v in sorted(d.items()):\n    print(f'{k}: {v}')\n"])

q(id="s5_matris", asama=5, baslik="Matris devriği", tur="fonksiyon",
  metin="`devrik(m)` fonksiyonu, iç içe liste ile verilen matrisin devriğini (transpose) yeni bir liste olarak döndürsün. Boş matris için `[]` döndürün.",
  cozum="def devrik(m):\n    if not m:\n        return []\n    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]\n",
  testler=["print(devrik([[1, 2], [3, 4]]))", "print(devrik([[1, 2, 3], [4, 5, 6]]))", "print(devrik([[1], [2], [3]]))", "print(devrik([]))",
           "print(devrik([[7]]))", "print(devrik([[1, 2, 3]]))"],
  yanlislar=["def devrik(m):\n    return m\n"])

q(id="s5_notlar", asama=5, baslik="Öğrenci not sözlüğü", tur="fonksiyon",
  metin="`en_basarili(notlar)` fonksiyonu `{isim: [not, not, ...]}` sözlüğü alır. Ortalaması en yüksek öğrencinin ismini döndürsün. Eşitlikte alfabetik olarak **ilk** isim seçilsin. Sözlük boşsa `None`. Notu olmayan öğrencinin ortalaması 0 sayılır.",
  cozum=("def en_basarili(notlar):\n    en_iyi, en_ort = None, -1\n    for isim in sorted(notlar):\n        l = notlar[isim]\n        ort = sum(l) / len(l) if l else 0\n"
         "        if ort > en_ort:\n            en_iyi, en_ort = isim, ort\n    return en_iyi\n"),
  testler=["print(en_basarili({'ali': [50, 60], 'veli': [90, 70], 'ayse': [100, 50]}))", "print(en_basarili({}))", "print(en_basarili({'zeynep': [80], 'ali': [80]}))",
           "print(en_basarili({'a': [], 'b': [1]}))", "print(en_basarili({'x': [100, 100, 100]}))", "print(en_basarili({'a': [], 'b': []}))"],
  yanlislar=["def en_basarili(notlar):\n    if not notlar: return None\n    return max(notlar, key=lambda k: sum(notlar[k]))\n"])

q(id="s5_toplam_ikili", asama=5, baslik="İki sayı toplamı (Two Sum)", tur="fonksiyon",
  metin="`iki_toplam(liste, hedef)` fonksiyonu, toplamı `hedef` eden iki **farklı indeksi** `(i, j)` (`i < j`) demeti olarak döndürsün. Birden çok çözüm varsa `i` en küçük, sonra `j` en küçük olan seçilir. Çözüm yoksa `None`.",
  cozum="def iki_toplam(liste, hedef):\n    for i in range(len(liste)):\n        for j in range(i + 1, len(liste)):\n            if liste[i] + liste[j] == hedef:\n                return (i, j)\n    return None\n",
  testler=["print(iki_toplam([2, 7, 11, 15], 9))", "print(iki_toplam([3, 2, 4], 6))", "print(iki_toplam([1, 2, 3], 10))", "print(iki_toplam([3, 3], 6))",
           "print(iki_toplam([], 0))", "print(iki_toplam([5], 10))", "print(iki_toplam([1, 4, 5, 6, 4], 8))", "print(iki_toplam([0, 4, 3, 0], 0))"],
  yanlislar=["def iki_toplam(liste, hedef):\n    for i in range(len(liste)):\n        for j in range(len(liste)):\n            if liste[i]+liste[j]==hedef: return (i,j)\n    return None\n"])

# ---------------------------------------------------------------- AŞAMA 6
q(id="s6_fibonacci", asama=6, baslik="Fibonacci (özyineleme)", tur="fonksiyon",
  metin="`fib(n)` fonksiyonunu **özyineleme (recursion)** ile yazın. `fib(0)=0`, `fib(1)=1`. Büyük `n` testleri de var: verimsiz çözüm zaman aşımına düşebilir (ipucu: önbellek/`functools.lru_cache`).",
  cozum="from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n",
  testler=[f"print(fib({n}))" for n in (0, 1, 2, 10, 20, 30, 80)],
  yanlislar=["def fib(n):\n    if n<2: return n\n    return fib(n-1)+fib(n-2)\n"])

q(id="s6_guvenli_bol", asama=6, baslik="Güvenli bölme (istisna)", tur="program",
  metin="Her satırda `a b` biçiminde iki değer gelir; girdi `son` satırıyla biter. Her satır için `a / b` sonucunu **iki ondalık** yazdırın. Hata durumlarında şu mesajlar yazılır:\n\n* `b` sıfır → `Sifira bolunemez`\n* sayıya çevrilemeyen değer → `Gecersiz giris`\n\n`try/except` kullanın.",
  cozum=("while True:\n    satir = input()\n    if satir == 'son':\n        break\n    try:\n        a, b = satir.split()\n        print(f'{float(a) / float(b):.2f}')\n"
         "    except ZeroDivisionError:\n        print('Sifira bolunemez')\n    except ValueError:\n        print('Gecersiz giris')\n"),
  testler=["10 4\nson\n", "5 0\nson\n", "abc 2\nson\n", "1 3\n7 2\n9 0\nx y\nson\n", "son\n", "-6 4\n0 5\nson\n"],
  yanlislar=["while True:\n    s=input()\n    if s=='son': break\n    a,b=s.split()\n    print(f'{float(a)/float(b):.2f}')\n"])

q(id="s6_banka", asama=6, baslik="Banka hesabı (OOP)", tur="fonksiyon",
  metin="`Hesap` sınıfını yazın:\n\n* `Hesap(sahip, bakiye=0)` — kurucu\n* `yatir(miktar)` — miktar pozitifse bakiyeye ekler; değilse `ValueError` fırlatır\n* `cek(miktar)` — yetersiz bakiyede `ValueError(\"Yetersiz bakiye\")` fırlatır; aksi halde düşer\n* `__str__` → `Sahip: ali, Bakiye: 100.00`",
  cozum=("class Hesap:\n    def __init__(self, sahip, bakiye=0):\n        self.sahip = sahip\n        self.bakiye = bakiye\n\n"
         "    def yatir(self, miktar):\n        if miktar <= 0:\n            raise ValueError('Gecersiz miktar')\n        self.bakiye += miktar\n\n"
         "    def cek(self, miktar):\n        if miktar > self.bakiye:\n            raise ValueError('Yetersiz bakiye')\n        self.bakiye -= miktar\n\n"
         "    def __str__(self):\n        return f'Sahip: {self.sahip}, Bakiye: {self.bakiye:.2f}'\n"),
  testler=["h = Hesap('ali', 100)\nprint(h)",
           "h = Hesap('veli')\nh.yatir(50)\nh.yatir(25.5)\nprint(h)",
           "h = Hesap('ayse', 100)\nh.cek(30)\nprint(h)",
           "h = Hesap('x', 10)\ntry:\n    h.cek(50)\nexcept ValueError as e:\n    print(e)\nprint(h)",
           "h = Hesap('y')\ntry:\n    h.yatir(-5)\nexcept ValueError:\n    print('hata')\nprint(h.bakiye)",
           "h = Hesap('z', 20)\nh.cek(20)\nprint(h)"],
  yanlislar=["class Hesap:\n    def __init__(self, sahip, bakiye=0):\n        self.sahip=sahip\n        self.bakiye=bakiye\n    def yatir(self, m):\n        self.bakiye+=m\n    def cek(self, m):\n        self.bakiye-=m\n    def __str__(self):\n        return f'Sahip: {self.sahip}, Bakiye: {self.bakiye:.2f}'\n"])

q(id="s6_satir_say", asama=6, baslik="Metin istatistikleri (stdin)", tur="program",
  metin="Girdi (`sys.stdin`) birden çok satırdır; bitene kadar okuyun. Üç satır yazdırın:\n\n```\nSatir: <boş olmayan satır sayısı>\nKelime: <toplam kelime>\nKarakter: <boşluk ve satır sonu hariç toplam karakter>\n```",
  cozum=("import sys\nsatir = kelime = karakter = 0\nfor s in sys.stdin:\n    s = s.rstrip('\\n')\n    if s.strip() == '':\n        continue\n    satir += 1\n    kelime += len(s.split())\n"
         "    karakter += len(s.replace(' ', ''))\nprint(f'Satir: {satir}')\nprint(f'Kelime: {kelime}')\nprint(f'Karakter: {karakter}')\n"),
  testler=["merhaba dunya\nikinci satir\n", "tek\n", "\n\nbos satirlar var\n\n", "a b c\nd e\n\nf\n", "", "  bosluklu   satir  \n"],
  yanlislar=["import sys\nm=sys.stdin.read()\nprint('Satir:',len(m.split('\\n')))\nprint('Kelime:',len(m.split()))\nprint('Karakter:',len(m))\n"])

SAYAC = ("class Sayac:\n    def __init__(self, it):\n        self._l = list(it)\n        self.erisim = 0\n"
         "    def __len__(self):\n        return len(self._l)\n    def __getitem__(self, i):\n        self.erisim += 1\n        return self._l[i]\n\n")

q(id="s6_ikili_arama", asama=6, baslik="İkili arama", tur="fonksiyon",
  metin="`ikili_ara(liste, x)` fonksiyonu, **sıralı** listede `x`'in indeksini ikili arama ile döndürsün; yoksa `-1`. (`in`, `index`, doğrusal arama yasak: bazı testler en fazla ~25 eleman erişimine izin verir.) Testlerde elemanlar tekildir.",
  cozum=("def ikili_ara(liste, x):\n    sol, sag = 0, len(liste) - 1\n    while sol <= sag:\n        orta = (sol + sag) // 2\n        if liste[orta] == x:\n            return orta\n"
         "        if liste[orta] < x:\n            sol = orta + 1\n        else:\n            sag = orta - 1\n    return -1\n"),
  testler=["print(ikili_ara([1, 3, 5, 7, 9], 7))", "print(ikili_ara([1, 3, 5, 7, 9], 1))", "print(ikili_ara([1, 3, 5, 7, 9], 9))", "print(ikili_ara([1, 3, 5, 7, 9], 4))",
           "print(ikili_ara([], 1))", "print(ikili_ara([5], 5))", "print(ikili_ara(list(range(0, 2000000, 2)), 1999998))", "print(ikili_ara(list(range(0, 2000000, 2)), 3))",
           SAYAC + "s = Sayac(range(0, 2000000, 2))\nprint(ikili_ara(s, 1000000), s.erisim <= 25)",
           SAYAC + "s = Sayac(range(0, 2000000, 2))\nprint(ikili_ara(s, 7), s.erisim <= 25)"],
  yanlislar=["def ikili_ara(liste, x):\n    return liste.index(x) if x in liste else -1\n"])

q(id="s6_siralama", asama=6, baslik="Kabarcık sıralaması", tur="fonksiyon",
  metin="`sirala(liste)` fonksiyonu, `sorted()`/`.sort()` kullanmadan, kabarcık (bubble) ya da seçmeli sıralama ile **yeni** artan sıralı liste döndürsün. Girdi değişmemelidir.",
  cozum=("def sirala(liste):\n    l = list(liste)\n    n = len(l)\n    for i in range(n):\n        for j in range(n - 1 - i):\n            if l[j] > l[j + 1]:\n                l[j], l[j + 1] = l[j + 1], l[j]\n    return l\n"),
  testler=["print(sirala([3, 1, 2]))", "print(sirala([]))", "print(sirala([5, 5, 1, 1]))", "print(sirala([9, 8, 7, 6, 5]))", "print(sirala([1]))",
           "g = [2, 1]\nsirala(g)\nprint(g)", "print(sirala([-1, 3, -5, 0]))"],
  yanlislar=["def sirala(liste):\n    liste.sort()\n    return liste\n"])

q(id="s6_parantez", asama=6, baslik="Parantez dengesi (yığın)", tur="fonksiyon",
  metin="`dengeli_mi(s)` fonksiyonu, metindeki `()[]{}` parantezleri doğru eşleşip iç içe kapanıyorsa `True` döndürsün. Diğer karakterler yok sayılır.",
  cozum=("def dengeli_mi(s):\n    cift = {')': '(', ']': '[', '}': '{'}\n    y = []\n    for c in s:\n        if c in '([{':\n            y.append(c)\n"
         "        elif c in cift:\n            if not y or y.pop() != cift[c]:\n                return False\n    return not y\n"),
  testler=['print(dengeli_mi("()"))', 'print(dengeli_mi("([{}])"))', 'print(dengeli_mi("(]"))', 'print(dengeli_mi("(()"))', 'print(dengeli_mi(")("))',
           'print(dengeli_mi(""))', 'print(dengeli_mi("a(b[c]d)e"))', 'print(dengeli_mi("([)]"))'],
  yanlislar=["def dengeli_mi(s):\n    return s.count('(')==s.count(')') and s.count('[')==s.count(']') and s.count('{')==s.count('}')\n"])

# ---------------------------------------------------------------- SINAV PAKETLERİ
# Her paket 6 soru (aşama başına bir), toplam 100 puan; süre 90 dk.
SINAVLAR = {
    "A": {"s1_ortalama": 10, "s2_harf": 15, "s3_asal": 15, "s4_palindrom": 15, "s5_frekans": 20, "s6_banka": 25},
    "B": {"s1_saniye": 10, "s2_ucgen": 15, "s3_fizzbuzz": 15, "s4_sezar": 15, "s5_tekrarsiz": 20, "s6_parantez": 25},
    "C": {"s1_bolme": 10, "s2_artikyil": 15, "s3_basamak": 15, "s4_anagram": 15, "s5_toplam_ikili": 20, "s6_guvenli_bol": 25},
    "D": {"s1_daire": 10, "s2_enbuyuk": 15, "s3_faktoriyel": 15, "s4_kelime": 15, "s5_notlar": 20, "s6_ikili_arama": 25},
}
