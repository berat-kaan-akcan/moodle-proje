# Istemci (Windows lab PC'si) kontrolleri; test/istemci_kontrol.sh betiginin Windows karsiligi.
# Kullanim:  powershell -ExecutionPolicy Bypass -File istemci_kontrol.ps1 http://SUNUCU_IP:8080
# Not: Windows PowerShell 5.1 BOM'suz dosyalari ANSI okudugu icin metinler bilerek Turkce karaktersiz yazildi.
param([Parameter(Mandatory = $true)][string]$Url)

$ProgressPreference = 'SilentlyContinue'
$Url = $Url.TrimEnd('/')
$u = [Uri]$Url
$script:gec = 0; $script:kal = 0

function Sonuc([string]$ad, [bool]$tamam) {
    if ($tamam) { Write-Host "  [GECTI] $ad" -ForegroundColor Green; $script:gec++ }
    else        { Write-Host "  [KALDI] $ad" -ForegroundColor Red;   $script:kal++ }
}

function Aciliyor([string]$adres) {
    try { Invoke-WebRequest -Uri $adres -UseBasicParsing -TimeoutSec 5 | Out-Null; return $true }
    catch { return $false }
}

Write-Host "== Kanit A: istemcide internet YOK olmali =="
Sonuc "8.8.8.8'e ping gitmiyor"        (-not (Test-Connection 8.8.8.8 -Count 2 -Quiet))
$dns = $false
try { [void][System.Net.Dns]::GetHostAddresses('google.com'); $dns = $true } catch {}
Sonuc "DNS cozumlenmiyor (google.com)" (-not $dns)
Sonuc "google.com'a HTTPS acilmiyor"   (-not (Aciliyor 'https://www.google.com'))
Sonuc "1.1.1.1'e HTTPS acilmiyor"      (-not (Aciliyor 'https://1.1.1.1'))

Write-Host "== Kanit B: sunucuya erisim VAR olmali =="
$tcp = $false
try {
    $c = New-Object System.Net.Sockets.TcpClient
    $tcp = $c.ConnectAsync($u.Host, $u.Port).Wait(5000) -and $c.Connected
    $c.Close()
} catch {}
Sonuc "sunucu portu acik ($($u.Host):$($u.Port))" $tcp

$sayfa = $null
try { $sayfa = Invoke-WebRequest -Uri "$Url/login/index.php" -UseBasicParsing -TimeoutSec 15 } catch {}
Sonuc "giris sayfasi yanit veriyor" ($null -ne $sayfa -and $sayfa.StatusCode -eq 200)
# Son adres: Windows PowerShell 5.1'de ResponseUri, PowerShell 7'de RequestMessage.RequestUri
$son = $null
if ($sayfa) {
    $son = $sayfa.BaseResponse.ResponseUri
    if (-not $son) { $son = $sayfa.BaseResponse.RequestMessage.RequestUri }
}
Sonuc "yonlendirme sunucu adresinde kaliyor ($son)" ($null -ne $son -and $son.Host -eq $u.Host)

Write-Host "== Dis kaynak =="
if ($sayfa) {
    $dis = [regex]::Matches($sayfa.Content, '(?:src|href)="(https?://[^"]+)"') |
        ForEach-Object { $_.Groups[1].Value } | Where-Object { $_ -notlike "*$($u.Authority)*" } | Sort-Object -Unique
    Sonuc "giris sayfasinda dis baglanti yok" (-not $dis)
    $dis | ForEach-Object { Write-Host "      $_" }
} else {
    Sonuc "dis kaynak taramasi yapilamadi (sayfa acilmadi)" $false
}

Write-Host "== Bilgi =="
$proxy = (Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction SilentlyContinue)
if ($proxy.ProxyEnable -eq 1) { Write-Host "  [UYARI] Sistem proxy'si acik: $($proxy.ProxyServer) - yerel adres acilmayabilir" -ForegroundColor Yellow }
else { Write-Host "  Sistem proxy'si kapali" }
Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -ne '127.0.0.1' } |
    ForEach-Object { Write-Host "  IP: $($_.IPAddress)/$($_.PrefixLength) ($($_.InterfaceAlias))" }

Write-Host ""
Write-Host "Ozet: $script:gec gecti, $script:kal kaldi"
if ($script:kal -gt 0) { exit 1 }
