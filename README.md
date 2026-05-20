# Cloud-Native Network Monitoring Sistemi

Bu proje Prometheus, Grafana ve Alertmanager kullanarak hazırlanmış uygulamalı bir network monitoring demosudur. Sistem canlı network telemetry metrikleri üretir, Prometheus bu metrikleri toplar, Grafana dashboard ile görselleştirir ve eşik değerleri aşılınca alert üretir.

## Mimari

```text
metric-app  --->  Prometheus  --->  Grafana Dashboard
    |                 |
    |                 +-------> Alertmanager
    |
    +-- /metrics endpoint ile network telemetry
```

## Bileşenler

- `metric-app`: Flask tabanlı canlı network metrik üreticisi.
- `prometheus`: Telemetry toplama ve alert rule değerlendirme servisi.
- `grafana`: Otomatik provision edilen network monitoring dashboard.
- `alertmanager`: Prometheus alertlerini gruplayan ve gösteren servis.
- `node-exporter`: Host/container seviyesinde temel sistem metrikleri.

## Toplanan Metrikler

- `network_latency_ms`: Anlık network gecikmesi.
- `network_packet_loss_percent`: Paket kaybı yüzdesi.
- `network_active_connections`: Aktif bağlantı sayısı.
- `network_bandwidth_mbps`: Bant genişliği kullanımı.
- `network_packets_total`: Direction ve protocol etiketli paket sayacı.
- `network_traffic_bytes_total`: Direction ve protocol etiketli trafik sayacı.

## Alert Kuralları

Prometheus alert kuralları `prometheus/alerts.yml` dosyasındadır.

- `HighNetworkLatency`: Gecikme 15 saniye boyunca 150 ms üstündeyse.
- `HighPacketLoss`: Paket kaybı 15 saniye boyunca %5 üstündeyse.
- `HighBandwidthUsage`: Bant genişliği 15 saniye boyunca 800 Mbps üstündeyse.
- `TooManyActiveConnections`: Aktif bağlantı 15 saniye boyunca 600 üstündeyse.

## Kurulum

Docker Desktop kurulu ve çalışır durumda olmalıdır.

```powershell
cd "C:\Users\mut46\Documents\ULAK FİNAL\cloud-native-network-monitoring"
docker compose up -d --build
```

## Docker Bulunamadı Hatası

Eğer PowerShell şu hatayı verirse:

```text
docker : The term 'docker' is not recognized
```

Bu, Docker Desktop'ın kurulu olmadığı veya PATH'e eklenmediği anlamına gelir. Windows için Docker Desktop kurulumu:

```powershell
winget install -e --id Docker.DockerDesktop
```

Kurulumdan sonra bilgisayarı yeniden başlat veya Docker Desktop'ı Start Menu'den aç. Docker çalışır duruma geldikten sonra yeni bir PowerShell penceresi açıp kontrol et:

```powershell
docker --version
docker compose version
```

Sonra projeyi başlat:

```powershell
cd "C:\Users\mut46\Documents\ULAK FİNAL\cloud-native-network-monitoring"
docker compose up -d --build
```

## Servisler

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Metric App: http://localhost:5000

Grafana giriş bilgileri:

- Kullanıcı adı: `admin`
- Şifre: `admin`

Dashboard yolu:

```text
Dashboards > Cloud Native Monitoring > Cloud-Native Network Monitoring
```

## Teslim ve Dokümantasyon Dosyaları

- `PROJECT_REPORT.md`: Ayrıntılı proje raporu. Ders kapsamı, teknik mimari, metrikler, alert kuralları, demo senaryosu ve sonuç bölümlerini içerir.
- `PRESENTATION_PLAN.md`: 15 dakikayı geçmeyecek sunum akışı ve konuşma metni.
- `DEMO_SCRIPT.md`: Uygulamalı gösterim sırasında izlenecek pratik adımlar.
- `EVALUATION_CHECKLIST.md`: Teknik doğruluk, uygulama başarısı, sunum-demo ve dokümantasyon kriterlerine göre kontrol listesi.

## Uygulamalı Demo Akışı

1. Sistemi başlat:

```powershell
docker compose up -d --build
```

2. Grafana dashboardunu aç:

```text
http://localhost:3000
```

3. Normal trafik metriklerini izle. Latency, packet loss, bandwidth ve active connection panelleri düşük/normal değerlerde olacaktır.

4. Alert senaryosunu başlat:

```powershell
.\scripts\trigger-alert.ps1
```

5. Yaklaşık 15-30 saniye bekle. Grafana dashboardunda değerlerin yükseldiğini, Prometheus Alerts sayfasında alertlerin `firing` durumuna geçtiğini göster:

```text
http://localhost:9090/alerts
```

6. Alertmanager ekranında alertlerin gruplanmış halde göründüğünü göster:

```text
http://localhost:9093/#/alerts
```

7. Normal duruma dön:

```powershell
.\scripts\normal-traffic.ps1
```

## Alternatif Senaryo

Alert seviyesine çıkmadan bozulmuş network davranışı göstermek için:

```powershell
.\scripts\degraded-traffic.ps1
```

Bu senaryoda gecikme ve paket kaybı artar, ancak her zaman critical alert tetiklenmeyebilir.

## Manuel API Kullanımı

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:5000/status"
Invoke-RestMethod -Method Post -Uri "http://localhost:5000/scenario" -ContentType "application/json" -Body '{"mode":"alert"}'
Invoke-RestMethod -Method Post -Uri "http://localhost:5000/scenario" -ContentType "application/json" -Body '{"mode":"normal"}'
```

## Durdurma

```powershell
docker compose down
```

Verileri de silmek istersen:

```powershell
docker compose down -v
```

## Sunumda Anlatılacak Kısa Özet

Bu sistem cloud-native observability yaklaşımını kullanır. Uygulama servisleri metriklerini `/metrics` endpointinden Prometheus formatında yayınlar. Prometheus belirli aralıklarla bu endpointleri scrape eder ve zaman serisi olarak saklar. Grafana, Prometheus datasource üzerinden bu metrikleri dashboarda dönüştürür. Prometheus alert kuralları belirlenen eşikler aşıldığında alert üretir ve Alertmanager bu alertleri gruplayıp yönetir. Demo sırasında alert senaryosu etkinleştirilerek latency, packet loss, bandwidth ve connection sayılarının arttığı, bunun sonucunda alert mekanizmasının çalıştığı canlı olarak gösterilir.
