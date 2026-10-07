# Cevap Anahtarı (yalnızca hoca)

Referans çözümler ve test case'ler. Beklenen çıktılar çözümlerden otomatik üretilmiştir.


## Aşama 1 — Temeller: girdi, çıktı, aritmetik

### s1_topla — İki sayının toplamı (program, 10 puan)

Klavyeden iki tam sayı (her biri ayrı satırda) okuyun ve toplamlarını yazdırın.

```python
a = int(input())
b = int(input())
print(a + b)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `3⏎4⏎` | `7` | evet |
| 2 | `-5⏎5⏎` | `0` | evet |
| 3 | `0⏎0⏎` | `0` | gizli |
| 4 | `1000000⏎2345678⏎` | `3345678` | gizli |
| 5 | `-7⏎-8⏎` | `-15` | gizli |

### s1_ortalama — Not ortalaması (program, 10 puan)

Üç vize notunu (ayrı satırlarda, tam sayı) okuyun. Ortalamalarını **iki ondalık basamakla** yazdırın.

Örnek: 70, 80, 85 → `78.33`

```python
a = int(input())
b = int(input())
c = int(input())
print(f'{(a + b + c) / 3:.2f}')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `70⏎80⏎85⏎` | `78.33` | evet |
| 2 | `100⏎100⏎100⏎` | `100.00` | evet |
| 3 | `0⏎0⏎1⏎` | `0.33` | gizli |
| 4 | `55⏎60⏎65⏎` | `60.00` | gizli |
| 5 | `99⏎98⏎97⏎` | `98.00` | gizli |

### s1_daire — Dairenin alanı (program, 10 puan)

Yarıçapı (ondalık sayı olabilir) okuyun. Dairenin alanını `math.pi` kullanarak **iki ondalık basamakla** yazdırın.

```python
import math
r = float(input())
print(f'{math.pi * r * r:.2f}')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `1⏎` | `3.14` | evet |
| 2 | `2.5⏎` | `19.63` | evet |
| 3 | `0⏎` | `0.00` | gizli |
| 4 | `10⏎` | `314.16` | gizli |
| 5 | `0.1⏎` | `0.03` | gizli |

### s1_saniye — Saniyeyi çevir (program, 10 puan)

Saniye cinsinden bir süre okuyun. Bunu `S saat M dakika N saniye` biçiminde yazdırın.

Örnek: `3725` → `1 saat 2 dakika 5 saniye`

```python
t = int(input())
print(f'{t // 3600} saat {t % 3600 // 60} dakika {t % 60} saniye')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `3725⏎` | `1 saat 2 dakika 5 saniye` | evet |
| 2 | `0⏎` | `0 saat 0 dakika 0 saniye` | evet |
| 3 | `59⏎` | `0 saat 0 dakika 59 saniye` | gizli |
| 4 | `3600⏎` | `1 saat 0 dakika 0 saniye` | gizli |
| 5 | `86399⏎` | `23 saat 59 dakika 59 saniye` | gizli |
| 6 | `7322⏎` | `2 saat 2 dakika 2 saniye` | gizli |

### s1_bolme — Bölüm ve kalan (program, 10 puan)

İki pozitif tam sayı `a` ve `b` okuyun (ayrı satırlarda). Tek satırda `a // b` ve `a % b` değerlerini boşlukla ayırarak yazdırın.

```python
a = int(input())
b = int(input())
print(a // b, a % b)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `17⏎5⏎` | `3 2` | evet |
| 2 | `10⏎2⏎` | `5 0` | evet |
| 3 | `3⏎7⏎` | `0 3` | gizli |
| 4 | `100⏎9⏎` | `11 1` | gizli |
| 5 | `1⏎1⏎` | `1 0` | gizli |


## Aşama 2 — Koşullar (if-elif-else)

### s2_ciftmi — Çift mi tek mi? (program, 10 puan)

Bir tam sayı okuyun. Çift ise `cift`, tek ise `tek` yazdırın. (Negatif sayılar ve sıfır dahil.)

```python
n = int(input())
print('cift' if n % 2 == 0 else 'tek')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `4⏎` | `cift` | evet |
| 2 | `7⏎` | `tek` | evet |
| 3 | `0⏎` | `cift` | gizli |
| 4 | `-3⏎` | `tek` | gizli |
| 5 | `-8⏎` | `cift` | gizli |
| 6 | `1⏎` | `tek` | gizli |

### s2_artikyil — Artık yıl (fonksiyon, 10 puan)

`artik_mi(yil)` fonksiyonunu yazın. Yıl artık ise `True`, değilse `False` döndürsün.

Kural: 4'e bölünür **ama** 100'e bölünmez, **ya da** 400'e bölünür.

```python
def artik_mi(yil):
    return (yil % 4 == 0 and yil % 100 != 0) or yil % 400 == 0
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(artik_mi(2024))` | `True` | evet |
| 2 | `print(artik_mi(2023))` | `False` | evet |
| 3 | `print(artik_mi(1900))` | `False` | gizli |
| 4 | `print(artik_mi(2000))` | `True` | gizli |
| 5 | `print(artik_mi(2100))` | `False` | gizli |
| 6 | `print(artik_mi(1996))` | `True` | gizli |
| 7 | `print(artik_mi(1))` | `False` | gizli |

### s2_harf — Harf notu (fonksiyon, 10 puan)

`harf(not_)` fonksiyonunu yazın:

* 90–100 → `AA`
* 80–89 → `BA`
* 70–79 → `BB`
* 60–69 → `CB`
* 50–59 → `CC`
* 0–49 → `FF`
* 0'dan küçük veya 100'den büyük → `Gecersiz`

```python
def harf(not_):
    if not_ < 0 or not_ > 100:
        return 'Gecersiz'
    if not_ >= 90:
        return 'AA'
    if not_ >= 80:
        return 'BA'
    if not_ >= 70:
        return 'BB'
    if not_ >= 60:
        return 'CB'
    if not_ >= 50:
        return 'CC'
    return 'FF'
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(harf(95))` | `AA` | evet |
| 2 | `print(harf(90))` | `AA` | evet |
| 3 | `print(harf(89))` | `BA` | gizli |
| 4 | `print(harf(80))` | `BA` | gizli |
| 5 | `print(harf(79))` | `BB` | gizli |
| 6 | `print(harf(70))` | `BB` | gizli |
| 7 | `print(harf(69))` | `CB` | gizli |
| 8 | `print(harf(60))` | `CB` | gizli |
| 9 | `print(harf(59))` | `CC` | gizli |
| 10 | `print(harf(50))` | `CC` | gizli |
| 11 | `print(harf(49))` | `FF` | gizli |
| 12 | `print(harf(0))` | `FF` | gizli |
| 13 | `print(harf(-1))` | `Gecersiz` | gizli |
| 14 | `print(harf(101))` | `Gecersiz` | gizli |
| 15 | `print(harf(100))` | `AA` | gizli |

### s2_ucgen — Üçgen türü (fonksiyon, 10 puan)

`ucgen_turu(a, b, c)` fonksiyonunu yazın. Kenar uzunluklarına göre döndürün:

* Üçgen oluşmuyorsa (herhangi bir kenar ≤ 0 ya da en uzun kenar ≥ diğer ikisinin toplamı) → `Gecersiz`
* üç kenar eşitse → `Eskenar`
* iki kenar eşitse → `Ikizkenar`
* hiçbiri eşit değilse → `Caliskenar`

```python
def ucgen_turu(a, b, c):
    if min(a, b, c) <= 0 or max(a, b, c) >= a + b + c - max(a, b, c):
        return 'Gecersiz'
    if a == b == c:
        return 'Eskenar'
    if a == b or b == c or a == c:
        return 'Ikizkenar'
    return 'Caliskenar'
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(ucgen_turu(3, 3, 3))` | `Eskenar` | evet |
| 2 | `print(ucgen_turu(3, 3, 4))` | `Ikizkenar` | evet |
| 3 | `print(ucgen_turu(3, 4, 5))` | `Caliskenar` | gizli |
| 4 | `print(ucgen_turu(1, 2, 3))` | `Gecersiz` | gizli |
| 5 | `print(ucgen_turu(0, 4, 4))` | `Gecersiz` | gizli |
| 6 | `print(ucgen_turu(5, 5, 10))` | `Gecersiz` | gizli |
| 7 | `print(ucgen_turu(4, 5, 4))` | `Ikizkenar` | gizli |
| 8 | `print(ucgen_turu(10, 1, 1))` | `Gecersiz` | gizli |
| 9 | `print(ucgen_turu(-1, 2, 2))` | `Gecersiz` | gizli |

### s2_enbuyuk — En büyük, en küçük (program, 10 puan)

Üç tam sayıyı ayrı satırlarda okuyun. `max()` ve `min()` kullanmadan, tek satırda `en_buyuk en_kucuk` biçiminde yazdırın.

```python
a = int(input())
b = int(input())
c = int(input())
buyuk = a
kucuk = a
for x in (b, c):
    if x > buyuk:
        buyuk = x
    if x < kucuk:
        kucuk = x
print(buyuk, kucuk)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `1⏎2⏎3⏎` | `3 1` | evet |
| 2 | `3⏎2⏎1⏎` | `3 1` | evet |
| 3 | `5⏎5⏎5⏎` | `5 5` | gizli |
| 4 | `-1⏎-5⏎-3⏎` | `-1 -5` | gizli |
| 5 | `2⏎9⏎4⏎` | `9 2` | gizli |
| 6 | `0⏎-1⏎1⏎` | `1 -1` | gizli |


## Aşama 3 — Döngüler (for-while)

### s3_toplam — 1'den n'e toplam (fonksiyon, 10 puan)

`toplam(n)` fonksiyonu, **döngü kullanarak** 1'den `n`'e kadar (n dahil) olan sayıların toplamını döndürsün. `n < 1` ise `0` döndürsün.

```python
def toplam(n):
    t = 0
    for i in range(1, n + 1):
        t += i
    return t
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(toplam(1))` | `1` | evet |
| 2 | `print(toplam(5))` | `15` | evet |
| 3 | `print(toplam(10))` | `55` | gizli |
| 4 | `print(toplam(100))` | `5050` | gizli |
| 5 | `print(toplam(0))` | `0` | gizli |
| 6 | `print(toplam(-3))` | `0` | gizli |
| 7 | `print(toplam(1000))` | `500500` | gizli |

### s3_faktoriyel — Faktöriyel (fonksiyon, 10 puan)

`faktoriyel(n)` fonksiyonunu **döngü ile** yazın (`math.factorial` yasak). `0! = 1`. `n` negatifse `-1` döndürün.

```python
def faktoriyel(n):
    if n < 0:
        return -1
    s = 1
    for i in range(2, n + 1):
        s *= i
    return s
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(faktoriyel(0))` | `1` | evet |
| 2 | `print(faktoriyel(1))` | `1` | evet |
| 3 | `print(faktoriyel(5))` | `120` | gizli |
| 4 | `print(faktoriyel(10))` | `3628800` | gizli |
| 5 | `print(faktoriyel(-2))` | `-1` | gizli |
| 6 | `print(faktoriyel(15))` | `1307674368000` | gizli |
| 7 | `print(faktoriyel(20))` | `2432902008176640000` | gizli |

### s3_asal — Asal mı? (fonksiyon, 10 puan)

`asal_mi(n)` fonksiyonu `n` asal ise `True`, değilse `False` döndürsün. (0, 1 ve negatifler asal değildir.)

```python
def asal_mi(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(asal_mi(2))` | `True` | evet |
| 2 | `print(asal_mi(3))` | `True` | evet |
| 3 | `print(asal_mi(4))` | `False` | gizli |
| 4 | `print(asal_mi(1))` | `False` | gizli |
| 5 | `print(asal_mi(0))` | `False` | gizli |
| 6 | `print(asal_mi(-7))` | `False` | gizli |
| 7 | `print(asal_mi(17))` | `True` | gizli |
| 8 | `print(asal_mi(25))` | `False` | gizli |
| 9 | `print(asal_mi(97))` | `True` | gizli |
| 10 | `print(asal_mi(100))` | `False` | gizli |
| 11 | `print(asal_mi(7919))` | `True` | gizli |

### s3_fizzbuzz — FizzBuzz (program, 10 puan)

`n` okuyun. 1'den `n`'e kadar her sayıyı ayrı satıra yazdırın; ancak 3'ün katı ise `Fizz`, 5'in katı ise `Buzz`, ikisinin de katı ise `FizzBuzz` yazdırın.

```python
n = int(input())
for i in range(1, n + 1):
    if i % 15 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `1⏎` | `1` | evet |
| 2 | `5⏎` | `1⏎2⏎Fizz⏎4⏎Buzz` | evet |
| 3 | `15⏎` | `1⏎2⏎Fizz⏎4⏎Buzz⏎Fizz⏎7⏎8⏎Fizz⏎Buzz⏎11⏎Fizz⏎13⏎14⏎FizzBuzz` | gizli |
| 4 | `20⏎` | `1⏎2⏎Fizz⏎4⏎Buzz⏎Fizz⏎7⏎8⏎Fizz⏎Buzz⏎11⏎Fizz⏎13⏎14⏎FizzBuzz⏎16⏎17⏎Fizz⏎19⏎Buzz` | gizli |
| 5 | `0⏎` | _(boş)_ | gizli |
| 6 | `30⏎` | `1⏎2⏎Fizz⏎4⏎Buzz⏎Fizz⏎7⏎8⏎Fizz⏎Buzz⏎11⏎Fizz⏎13⏎14⏎FizzBuzz⏎16⏎17⏎Fizz⏎19⏎Buzz⏎Fizz⏎22⏎23⏎Fizz⏎Buzz⏎26⏎Fizz⏎28⏎29⏎FizzBuzz` | gizli |

### s3_basamak — Basamaklar toplamı (fonksiyon, 10 puan)

`basamak_toplami(n)` fonksiyonu bir tam sayının basamaklarının toplamını döndürsün. **String'e çevirmeden** (`%` ve `//` ile) yazın. Negatif sayılarda işareti yok sayın.

```python
def basamak_toplami(n):
    n = abs(n)
    t = 0
    while n > 0:
        t += n % 10
        n //= 10
    return t
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(basamak_toplami(123))` | `6` | evet |
| 2 | `print(basamak_toplami(0))` | `0` | evet |
| 3 | `print(basamak_toplami(9))` | `9` | gizli |
| 4 | `print(basamak_toplami(1000))` | `1` | gizli |
| 5 | `print(basamak_toplami(-456))` | `15` | gizli |
| 6 | `print(basamak_toplami(99999))` | `45` | gizli |
| 7 | `print(basamak_toplami(1234567890))` | `45` | gizli |

### s3_ucgen_yildiz — Yıldız üçgeni (program, 10 puan)

`n` okuyun. Sağa dayalı yıldız üçgeni çizin: `i`. satırda önce `n-i` boşluk, sonra `i` tane `*` olsun.

`n=3` için:
```
  *
 **
***
```

```python
n = int(input())
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * i)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `3⏎` | `  *⏎ **⏎***` | evet |
| 2 | `1⏎` | `*` | evet |
| 3 | `5⏎` | `    *⏎   **⏎  ***⏎ ****⏎*****` | gizli |
| 4 | `0⏎` | _(boş)_ | gizli |
| 5 | `7⏎` | `      *⏎     **⏎    ***⏎   ****⏎  *****⏎ ******⏎*******` | gizli |


## Aşama 4 — Fonksiyonlar ve string işlemleri

### s4_palindrom — Palindrom (fonksiyon, 10 puan)

`palindrom_mu(s)` fonksiyonu; büyük/küçük harf ve **boşlukları yok sayarak** metin palindrom ise `True`, değilse `False` döndürsün.

Örnek: `"Kay ak"` → `True`.

```python
def palindrom_mu(s):
    t = s.replace(' ', '').lower()
    return t == t[::-1]
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(palindrom_mu("kayak"))` | `True` | evet |
| 2 | `print(palindrom_mu("Kay ak"))` | `True` | evet |
| 3 | `print(palindrom_mu("python"))` | `False` | gizli |
| 4 | `print(palindrom_mu(""))` | `True` | gizli |
| 5 | `print(palindrom_mu("A man a plan a canal Panama"))` | `True` | gizli |
| 6 | `print(palindrom_mu("ab"))` | `False` | gizli |
| 7 | `print(palindrom_mu("Aa"))` | `True` | gizli |

### s4_sesli — Sesli harf sayısı (fonksiyon, 10 puan)

`sesli_say(s)` fonksiyonu, metindeki sesli harf (`aeıioöuü`, büyük/küçük fark etmez) sayısını döndürsün.

```python
def sesli_say(s):
    return sum(1 for c in s.lower() if c in 'aeıioöuü')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(sesli_say("merhaba"))` | `3` | evet |
| 2 | `print(sesli_say("PYTHON"))` | `1` | evet |
| 3 | `print(sesli_say(""))` | `0` | gizli |
| 4 | `print(sesli_say("ÜÖİ"))` | `3` | gizli |
| 5 | `print(sesli_say("kıvırcık"))` | `3` | gizli |
| 6 | `print(sesli_say("bcdfg"))` | `0` | gizli |
| 7 | `print(sesli_say("AEIOU"))` | `5` | gizli |

### s4_kelime — En uzun kelime (program, 10 puan)

Bir satır metin okuyun (kelimeler boşlukla ayrılmış). Önce kelime sayısını, sonra **en uzun kelimeyi** ayrı satırlarda yazdırın. Eşitlik varsa **ilk** geçen kelime seçilir. Satırda en az bir kelime olacaktır.

```python
kelimeler = input().split()
print(len(kelimeler))
en = ''
for k in kelimeler:
    if len(k) > len(en):
        en = k
print(en)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `bugun hava cok guzel⏎` | `4⏎bugun` | evet |
| 2 | `a bb ccc dd⏎` | `4⏎ccc` | evet |
| 3 | `tek⏎` | `1⏎tek` | gizli |
| 4 | `bir iki uc dort bes⏎` | `5⏎dort` | gizli |
| 5 | `ab cd ef⏎` | `3⏎ab` | gizli |
| 6 | `  cok   bosluk   var  ⏎` | `3⏎bosluk` | gizli |

### s4_sezar — Sezar şifresi (fonksiyon, 10 puan)

`sifrele(metin, kaydir)` fonksiyonunu yazın. Yalnızca `a-z` ve `A-Z` harfleri alfabede `kaydir` kadar ileri kaydırılır (z'den sonra a'ya dönülür, büyük/küçük harf korunur). Diğer karakterler **aynen** kalır. `kaydir` negatif olabilir.

```python
def sifrele(metin, kaydir):
    sonuc = ''
    for c in metin:
        if 'a' <= c <= 'z':
            sonuc += chr((ord(c) - 97 + kaydir) % 26 + 97)
        elif 'A' <= c <= 'Z':
            sonuc += chr((ord(c) - 65 + kaydir) % 26 + 65)
        else:
            sonuc += c
    return sonuc
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(sifrele("abc", 1))` | `bcd` | evet |
| 2 | `print(sifrele("xyz", 3))` | `abc` | evet |
| 3 | `print(sifrele("Hello, World!", 5))` | `Mjqqt, Btwqi!` | gizli |
| 4 | `print(sifrele("abc", 0))` | `abc` | gizli |
| 5 | `print(sifrele("def", -3))` | `abc` | gizli |
| 6 | `print(sifrele("Python 3.12", 13))` | `Clguba 3.12` | gizli |
| 7 | `print(sifrele("abc", 27))` | `bcd` | gizli |

### s4_anagram — Anagram (fonksiyon, 10 puan)

`anagram_mi(a, b)` fonksiyonu iki kelime birbirinin anagramı ise `True` döndürsün. Büyük/küçük harf ve boşluklar yok sayılır.

```python
def anagram_mi(a, b):
    f = lambda s: sorted(s.replace(' ', '').lower())
    return f(a) == f(b)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(anagram_mi("listen", "silent"))` | `True` | evet |
| 2 | `print(anagram_mi("Dormitory", "dirty room"))` | `True` | evet |
| 3 | `print(anagram_mi("abc", "abd"))` | `False` | gizli |
| 4 | `print(anagram_mi("aab", "abb"))` | `False` | gizli |
| 5 | `print(anagram_mi("", ""))` | `True` | gizli |
| 6 | `print(anagram_mi("abc", "ab"))` | `False` | gizli |


## Aşama 5 — Liste, sözlük, küme, matris

### s5_ikinci — İkinci en büyük (fonksiyon, 10 puan)

`ikinci_buyuk(liste)` fonksiyonu listedeki **farklı** değerler arasında ikinci en büyüğünü döndürsün. Farklı iki değer yoksa `None` döndürsün.

```python
def ikinci_buyuk(liste):
    s = sorted(set(liste), reverse=True)
    return s[1] if len(s) >= 2 else None
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(ikinci_buyuk([1, 2, 3]))` | `2` | evet |
| 2 | `print(ikinci_buyuk([5, 5, 5]))` | `None` | evet |
| 3 | `print(ikinci_buyuk([10, 9, 10, 8]))` | `9` | gizli |
| 4 | `print(ikinci_buyuk([]))` | `None` | gizli |
| 5 | `print(ikinci_buyuk([7]))` | `None` | gizli |
| 6 | `print(ikinci_buyuk([-1, -2, -3]))` | `-2` | gizli |
| 7 | `print(ikinci_buyuk([2, 1]))` | `1` | gizli |

### s5_tekrarsiz — Tekrarları sil (fonksiyon, 10 puan)

`tekrarsiz(liste)` fonksiyonu, tekrar eden elemanları silip **ilk geçişlerin sırasını koruyarak** yeni bir liste döndürsün. Girdi listesini değiştirmeyin.

```python
def tekrarsiz(liste):
    gorulen = set()
    sonuc = []
    for x in liste:
        if x not in gorulen:
            gorulen.add(x)
            sonuc.append(x)
    return sonuc
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(tekrarsiz([1, 2, 2, 3, 1]))` | `[1, 2, 3]` | evet |
| 2 | `print(tekrarsiz([]))` | `[]` | evet |
| 3 | `print(tekrarsiz(['a', 'b', 'a']))` | `['a', 'b']` | gizli |
| 4 | `print(tekrarsiz([3, 3, 3]))` | `[3]` | gizli |
| 5 | `print(tekrarsiz([5, 4, 3]))` | `[5, 4, 3]` | gizli |
| 6 | `l = [1, 1, 2]⏎tekrarsiz(l)⏎print(l)` | `[1, 1, 2]` | gizli |

### s5_frekans — Harf frekansı (program, 10 puan)

Bir satır metin okuyun. Harfleri (küçük harfe çevirerek, boşluk ve diğer karakterleri atlayarak) sayın. Her harfi `harf: adet` biçiminde, **önce adedi çok olan, eşitlikte alfabetik** sırayla ayrı satırlarda yazdırın.

```python
s = input().lower()
sayac = {}
for c in s:
    if c.isalpha():
        sayac[c] = sayac.get(c, 0) + 1
for harf, adet in sorted(sayac.items(), key=lambda x: (-x[1], x[0])):
    print(f'{harf}: {adet}')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `banana⏎` | `a: 3⏎n: 2⏎b: 1` | evet |
| 2 | `Hello World⏎` | `l: 3⏎o: 2⏎d: 1⏎e: 1⏎h: 1⏎r: 1⏎w: 1` | evet |
| 3 | `aabbcc⏎` | `a: 2⏎b: 2⏎c: 2` | gizli |
| 4 | `a⏎` | `a: 1` | gizli |
| 5 | `x y z x⏎` | `x: 2⏎y: 1⏎z: 1` | gizli |
| 6 | `123 !!⏎` | _(boş)_ | gizli |
| 7 | `Python ve Java⏎` | `a: 2⏎v: 2⏎e: 1⏎h: 1⏎j: 1⏎n: 1⏎o: 1⏎p: 1⏎t: 1⏎y: 1` | gizli |

### s5_matris — Matris devriği (fonksiyon, 10 puan)

`devrik(m)` fonksiyonu, iç içe liste ile verilen matrisin devriğini (transpose) yeni bir liste olarak döndürsün. Boş matris için `[]` döndürün.

```python
def devrik(m):
    if not m:
        return []
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(devrik([[1, 2], [3, 4]]))` | `[[1, 3], [2, 4]]` | evet |
| 2 | `print(devrik([[1, 2, 3], [4, 5, 6]]))` | `[[1, 4], [2, 5], [3, 6]]` | evet |
| 3 | `print(devrik([[1], [2], [3]]))` | `[[1, 2, 3]]` | gizli |
| 4 | `print(devrik([]))` | `[]` | gizli |
| 5 | `print(devrik([[7]]))` | `[[7]]` | gizli |
| 6 | `print(devrik([[1, 2, 3]]))` | `[[1], [2], [3]]` | gizli |

### s5_notlar — Öğrenci not sözlüğü (fonksiyon, 10 puan)

`en_basarili(notlar)` fonksiyonu `{isim: [not, not, ...]}` sözlüğü alır. Ortalaması en yüksek öğrencinin ismini döndürsün. Eşitlikte alfabetik olarak **ilk** isim seçilsin. Sözlük boşsa `None`. Notu olmayan öğrencinin ortalaması 0 sayılır.

```python
def en_basarili(notlar):
    en_iyi, en_ort = None, -1
    for isim in sorted(notlar):
        l = notlar[isim]
        ort = sum(l) / len(l) if l else 0
        if ort > en_ort:
            en_iyi, en_ort = isim, ort
    return en_iyi
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(en_basarili({'ali': [50, 60], 'veli': [90, 70], 'ayse': [100, 50]}))` | `veli` | evet |
| 2 | `print(en_basarili({}))` | `None` | evet |
| 3 | `print(en_basarili({'zeynep': [80], 'ali': [80]}))` | `ali` | gizli |
| 4 | `print(en_basarili({'a': [], 'b': [1]}))` | `b` | gizli |
| 5 | `print(en_basarili({'x': [100, 100, 100]}))` | `x` | gizli |
| 6 | `print(en_basarili({'a': [], 'b': []}))` | `a` | gizli |

### s5_toplam_ikili — İki sayı toplamı (Two Sum) (fonksiyon, 10 puan)

`iki_toplam(liste, hedef)` fonksiyonu, toplamı `hedef` eden iki **farklı indeksi** `(i, j)` (`i < j`) demeti olarak döndürsün. Birden çok çözüm varsa `i` en küçük, sonra `j` en küçük olan seçilir. Çözüm yoksa `None`.

```python
def iki_toplam(liste, hedef):
    for i in range(len(liste)):
        for j in range(i + 1, len(liste)):
            if liste[i] + liste[j] == hedef:
                return (i, j)
    return None
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(iki_toplam([2, 7, 11, 15], 9))` | `(0, 1)` | evet |
| 2 | `print(iki_toplam([3, 2, 4], 6))` | `(1, 2)` | evet |
| 3 | `print(iki_toplam([1, 2, 3], 10))` | `None` | gizli |
| 4 | `print(iki_toplam([3, 3], 6))` | `(0, 1)` | gizli |
| 5 | `print(iki_toplam([], 0))` | `None` | gizli |
| 6 | `print(iki_toplam([5], 10))` | `None` | gizli |
| 7 | `print(iki_toplam([1, 4, 5, 6, 4], 8))` | `(1, 4)` | gizli |
| 8 | `print(iki_toplam([0, 4, 3, 0], 0))` | `(0, 3)` | gizli |


## Aşama 6 — Özyineleme, istisna, OOP, algoritmalar

### s6_fibonacci — Fibonacci (özyineleme) (fonksiyon, 10 puan)

`fib(n)` fonksiyonunu **özyineleme (recursion)** ile yazın. `fib(0)=0`, `fib(1)=1`. Büyük `n` testleri de var: verimsiz çözüm zaman aşımına düşebilir (ipucu: önbellek/`functools.lru_cache`).

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(fib(0))` | `0` | evet |
| 2 | `print(fib(1))` | `1` | evet |
| 3 | `print(fib(2))` | `1` | gizli |
| 4 | `print(fib(10))` | `55` | gizli |
| 5 | `print(fib(20))` | `6765` | gizli |
| 6 | `print(fib(30))` | `832040` | gizli |
| 7 | `print(fib(80))` | `23416728348467685` | gizli |

### s6_guvenli_bol — Güvenli bölme (istisna) (program, 10 puan)

Her satırda `a b` biçiminde iki değer gelir; girdi `son` satırıyla biter. Her satır için `a / b` sonucunu **iki ondalık** yazdırın. Hata durumlarında şu mesajlar yazılır:

* `b` sıfır → `Sifira bolunemez`
* sayıya çevrilemeyen değer → `Gecersiz giris`

`try/except` kullanın.

```python
while True:
    satir = input()
    if satir == 'son':
        break
    try:
        a, b = satir.split()
        print(f'{float(a) / float(b):.2f}')
    except ZeroDivisionError:
        print('Sifira bolunemez')
    except ValueError:
        print('Gecersiz giris')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `10 4⏎son⏎` | `2.50` | evet |
| 2 | `5 0⏎son⏎` | `Sifira bolunemez` | evet |
| 3 | `abc 2⏎son⏎` | `Gecersiz giris` | gizli |
| 4 | `1 3⏎7 2⏎9 0⏎x y⏎son⏎` | `0.33⏎3.50⏎Sifira bolunemez⏎Gecersiz giris` | gizli |
| 5 | `son⏎` | _(boş)_ | gizli |
| 6 | `-6 4⏎0 5⏎son⏎` | `-1.50⏎0.00` | gizli |

### s6_banka — Banka hesabı (OOP) (fonksiyon, 10 puan)

`Hesap` sınıfını yazın:

* `Hesap(sahip, bakiye=0)` — kurucu
* `yatir(miktar)` — miktar pozitifse bakiyeye ekler; değilse `ValueError` fırlatır
* `cek(miktar)` — yetersiz bakiyede `ValueError("Yetersiz bakiye")` fırlatır; aksi halde düşer
* `__str__` → `Sahip: ali, Bakiye: 100.00`

```python
class Hesap:
    def __init__(self, sahip, bakiye=0):
        self.sahip = sahip
        self.bakiye = bakiye

    def yatir(self, miktar):
        if miktar <= 0:
            raise ValueError('Gecersiz miktar')
        self.bakiye += miktar

    def cek(self, miktar):
        if miktar > self.bakiye:
            raise ValueError('Yetersiz bakiye')
        self.bakiye -= miktar

    def __str__(self):
        return f'Sahip: {self.sahip}, Bakiye: {self.bakiye:.2f}'
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `h = Hesap('ali', 100)⏎print(h)` | `Sahip: ali, Bakiye: 100.00` | evet |
| 2 | `h = Hesap('veli')⏎h.yatir(50)⏎h.yatir(25.5)⏎print(h)` | `Sahip: veli, Bakiye: 75.50` | evet |
| 3 | `h = Hesap('ayse', 100)⏎h.cek(30)⏎print(h)` | `Sahip: ayse, Bakiye: 70.00` | gizli |
| 4 | `h = Hesap('x', 10)⏎try:⏎    h.cek(50)⏎except ValueError as e:⏎    print(e)⏎print(h)` | `Yetersiz bakiye⏎Sahip: x, Bakiye: 10.00` | gizli |
| 5 | `h = Hesap('y')⏎try:⏎    h.yatir(-5)⏎except ValueError:⏎    print('hata')⏎print(h.bakiye)` | `hata⏎0` | gizli |
| 6 | `h = Hesap('z', 20)⏎h.cek(20)⏎print(h)` | `Sahip: z, Bakiye: 0.00` | gizli |

### s6_satir_say — Metin istatistikleri (stdin) (program, 10 puan)

Girdi (`sys.stdin`) birden çok satırdır; bitene kadar okuyun. Üç satır yazdırın:

```
Satir: <boş olmayan satır sayısı>
Kelime: <toplam kelime>
Karakter: <boşluk ve satır sonu hariç toplam karakter>
```

```python
import sys
satir = kelime = karakter = 0
for s in sys.stdin:
    s = s.rstrip('\n')
    if s.strip() == '':
        continue
    satir += 1
    kelime += len(s.split())
    karakter += len(s.replace(' ', ''))
print(f'Satir: {satir}')
print(f'Kelime: {kelime}')
print(f'Karakter: {karakter}')
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `merhaba dunya⏎ikinci satir⏎` | `Satir: 2⏎Kelime: 4⏎Karakter: 23` | evet |
| 2 | `tek⏎` | `Satir: 1⏎Kelime: 1⏎Karakter: 3` | evet |
| 3 | `⏎⏎bos satirlar var⏎⏎` | `Satir: 1⏎Kelime: 3⏎Karakter: 14` | gizli |
| 4 | `a b c⏎d e⏎⏎f⏎` | `Satir: 3⏎Kelime: 6⏎Karakter: 6` | gizli |
| 5 | _(boş)_ | `Satir: 0⏎Kelime: 0⏎Karakter: 0` | gizli |
| 6 | `  bosluklu   satir  ⏎` | `Satir: 1⏎Kelime: 2⏎Karakter: 13` | gizli |

### s6_ikili_arama — İkili arama (fonksiyon, 10 puan)

`ikili_ara(liste, x)` fonksiyonu, **sıralı** listede `x`'in indeksini ikili arama ile döndürsün; yoksa `-1`. (`in`, `index`, doğrusal arama yasak: bazı testler en fazla ~25 eleman erişimine izin verir.) Testlerde elemanlar tekildir.

```python
def ikili_ara(liste, x):
    sol, sag = 0, len(liste) - 1
    while sol <= sag:
        orta = (sol + sag) // 2
        if liste[orta] == x:
            return orta
        if liste[orta] < x:
            sol = orta + 1
        else:
            sag = orta - 1
    return -1
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(ikili_ara([1, 3, 5, 7, 9], 7))` | `3` | evet |
| 2 | `print(ikili_ara([1, 3, 5, 7, 9], 1))` | `0` | evet |
| 3 | `print(ikili_ara([1, 3, 5, 7, 9], 9))` | `4` | gizli |
| 4 | `print(ikili_ara([1, 3, 5, 7, 9], 4))` | `-1` | gizli |
| 5 | `print(ikili_ara([], 1))` | `-1` | gizli |
| 6 | `print(ikili_ara([5], 5))` | `0` | gizli |
| 7 | `print(ikili_ara(list(range(0, 2000000, 2)), 1999998))` | `999999` | gizli |
| 8 | `print(ikili_ara(list(range(0, 2000000, 2)), 3))` | `-1` | gizli |
| 9 | `class Sayac:⏎    def __init__(self, it):⏎        self._l = list(it)⏎        self.erisim = 0⏎    def __len__(self):⏎        return len(self._l)⏎    def __getitem__(self, i):⏎        self.erisim += 1⏎        return self._l[i]⏎⏎s = Sayac(range(0, 2000000, 2))⏎print(ikili_ara(s, 1000000), s.erisim <= 25)` | `500000 False` | gizli |
| 10 | `class Sayac:⏎    def __init__(self, it):⏎        self._l = list(it)⏎        self.erisim = 0⏎    def __len__(self):⏎        return len(self._l)⏎    def __getitem__(self, i):⏎        self.erisim += 1⏎        return self._l[i]⏎⏎s = Sayac(range(0, 2000000, 2))⏎print(ikili_ara(s, 7), s.erisim <= 25)` | `-1 False` | gizli |

### s6_siralama — Kabarcık sıralaması (fonksiyon, 10 puan)

`sirala(liste)` fonksiyonu, `sorted()`/`.sort()` kullanmadan, kabarcık (bubble) ya da seçmeli sıralama ile **yeni** artan sıralı liste döndürsün. Girdi değişmemelidir.

```python
def sirala(liste):
    l = list(liste)
    n = len(l)
    for i in range(n):
        for j in range(n - 1 - i):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
    return l
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(sirala([3, 1, 2]))` | `[1, 2, 3]` | evet |
| 2 | `print(sirala([]))` | `[]` | evet |
| 3 | `print(sirala([5, 5, 1, 1]))` | `[1, 1, 5, 5]` | gizli |
| 4 | `print(sirala([9, 8, 7, 6, 5]))` | `[5, 6, 7, 8, 9]` | gizli |
| 5 | `print(sirala([1]))` | `[1]` | gizli |
| 6 | `g = [2, 1]⏎sirala(g)⏎print(g)` | `[2, 1]` | gizli |
| 7 | `print(sirala([-1, 3, -5, 0]))` | `[-5, -1, 0, 3]` | gizli |

### s6_parantez — Parantez dengesi (yığın) (fonksiyon, 10 puan)

`dengeli_mi(s)` fonksiyonu, metindeki `()[]{}` parantezleri doğru eşleşip iç içe kapanıyorsa `True` döndürsün. Diğer karakterler yok sayılır.

```python
def dengeli_mi(s):
    cift = {')': '(', ']': '[', '}': '{'}
    y = []
    for c in s:
        if c in '([{':
            y.append(c)
        elif c in cift:
            if not y or y.pop() != cift[c]:
                return False
    return not y
```

| # | Girdi / çağrı | Beklenen | Görünür |
|---|---|---|---|
| 1 | `print(dengeli_mi("()"))` | `True` | evet |
| 2 | `print(dengeli_mi("([{}])"))` | `True` | evet |
| 3 | `print(dengeli_mi("(]"))` | `False` | gizli |
| 4 | `print(dengeli_mi("(()"))` | `False` | gizli |
| 5 | `print(dengeli_mi(")("))` | `False` | gizli |
| 6 | `print(dengeli_mi(""))` | `True` | gizli |
| 7 | `print(dengeli_mi("a(b[c]d)e"))` | `True` | gizli |
| 8 | `print(dengeli_mi("([)]"))` | `False` | gizli |


## Sınav paketleri

* **Paket A**: s1_ortalama (10), s2_harf (15), s3_asal (15), s4_palindrom (15), s5_frekans (20), s6_banka (25)
* **Paket B**: s1_saniye (10), s2_ucgen (15), s3_fizzbuzz (15), s4_sezar (15), s5_tekrarsiz (20), s6_parantez (25)
* **Paket C**: s1_bolme (10), s2_artikyil (15), s3_basamak (15), s4_anagram (15), s5_toplam_ikili (20), s6_guvenli_bol (25)
* **Paket D**: s1_daire (10), s2_enbuyuk (15), s3_faktoriyel (15), s4_kelime (15), s5_notlar (20), s6_ikili_arama (25)
