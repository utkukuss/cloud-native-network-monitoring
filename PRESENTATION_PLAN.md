# 15 Dakikalık Sunum Planı

## Proje: Cloud-Native Network Monitoring Sistemi

Bu dosya final haftasında yapılacak sunum için hazırlanmıştır. Sunum süresi 15 dakikayı geçmeyecek şekilde planlanmıştır.

---

## 0:00 - 1:00 | Giriş

Söylenecek metin:

Bu projede modern cloud-native araçlar kullanarak bir network monitoring sistemi geliştirdim. Sistem Prometheus ile telemetry verisi topluyor, Grafana ile bu verileri dashboard üzerinde görselleştiriyor ve belirlenen eşik değerleri aşıldığında Alertmanager üzerinden alarm üretiyor.

Vurgulanacak noktalar:

- Proje konusu network monitoring.
- Amaç canlı metrik izleme ve alert tetikleme.
- Kullanılan temel araçlar Prometheus, Grafana ve Alertmanager.

---

## 1:00 - 3:00 | Problem ve Motivasyon

Söylenecek metin:

Modern ağlarda gecikme, paket kaybı, bant genişliği kullanımı ve bağlantı sayısı gibi metrikler sürekli değişmektedir. Bu metriklerin manuel takip edilmesi zor olduğu için merkezi bir gözlemlenebilirlik sistemi gerekir. Bu sistem sayesinde ağdaki sorunlar erken fark edilebilir ve kritik durumlarda otomatik alarm üretilebilir.

Vurgulanacak noktalar:

- Ağ metrikleri servis kalitesi için önemlidir.
- Monitoring olmadan sorunlar geç fark edilir.
- Alert mekanizması operasyonel farkındalık sağlar.

---

## 3:00 - 5:00 | Mimari

Söylenecek metin:

Sistemde metric app isimli bir uygulama Prometheus formatında canlı network metrikleri yayınlıyor. Prometheus bu metrikleri düzenli olarak scrape ediyor. Grafana, Prometheus datasource üzerinden dashboard oluşturuyor. Prometheus alert kuralları eşik değerlerini kontrol ediyor ve eşikler aşılınca Alertmanager'a alert gönderiyor.

Gösterilecek yer:

- `docker-compose.yml`
- Mimari anlatım:

```text
Metric App -> Prometheus -> Grafana
                  |
                  v
             Alertmanager
```

---

## 5:00 - 7:00 | Kullanılan Teknolojiler

Söylenecek metin:

Docker Compose çok servisli yapıyı ayağa kaldırmak için kullanıldı. Prometheus metrik toplama ve alert rule değerlendirme görevini üstleniyor. Grafana dashboard ve görselleştirme için kullanılıyor. Alertmanager alarm yönetimini sağlıyor. Flask tabanlı metric app ise canlı network metrikleri üretiyor.

Kısa açıklamalar:

- Docker Compose: Ortamı tek komutla çalıştırır.
- Prometheus: Telemetry toplar.
- Grafana: Verileri görselleştirir.
- Alertmanager: Alarmları yönetir.
- Flask metric app: Demo network metrikleri üretir.

---

## 7:00 - 10:00 | Canlı Dashboard Demo

Gösterilecek ekran:

```text
http://localhost:3000
```

Söylenecek metin:

Grafana dashboard üzerinde canlı network metrikleri izleniyor. Burada network latency, packet loss, bandwidth usage, packet rate ve active connections panelleri bulunuyor. Dashboard 5 saniyede bir yenileniyor ve Prometheus'tan gelen canlı verileri gösteriyor.

Gösterilecek paneller:

- Network Latency
- Packet Loss
- Bandwidth Usage
- Packet Rate
- Active Connections
- Firing Alerts

---

## 10:00 - 12:30 | Alert Tetikleme Demo

Çalıştırılacak komut:

```powershell
.\scripts\trigger-alert.ps1
```

Söylenecek metin:

Şimdi alert senaryosunu başlatıyorum. Bu senaryoda sistem yüksek gecikme, yüksek paket kaybı, yüksek bant genişliği kullanımı ve fazla aktif bağlantı üretiyor. Prometheus bu değerleri topluyor ve tanımlanan eşik değerleri 15 saniye boyunca aşıldığında alertleri firing durumuna geçiriyor.

Gösterilecek adresler:

```text
http://localhost:9090/alerts
http://localhost:9093/#/alerts
```

Beklenen alertler:

- HighNetworkLatency
- HighPacketLoss
- HighBandwidthUsage
- TooManyActiveConnections

---

## 12:30 - 14:00 | Doğrulama ve Sonuçlar

Söylenecek metin:

Prometheus targets ekranında servislerin UP olduğu görülüyor. Prometheus graph ekranında metrik sorguları değer döndürüyor. Grafana dashboard metrikleri görselleştiriyor. Prometheus alerts ekranında alertler firing durumunda. Alertmanager ekranında bu alertler gruplanmış olarak görüntüleniyor. Bu nedenle sistemin telemetry toplama, görselleştirme ve alert üretme fonksiyonları başarıyla çalışmaktadır.

Gösterilecek adresler:

```text
http://localhost:9090/targets
http://localhost:9090/graph
http://localhost:9090/alerts
http://localhost:9093/#/alerts
```

---

## 14:00 - 15:00 | Kapanış

Söylenecek metin:

Sonuç olarak bu proje, cloud-native monitoring zincirini uçtan uca göstermektedir. Network telemetry verileri canlı olarak üretilmiş, Prometheus ile toplanmış, Grafana ile görselleştirilmiş ve Alertmanager ile alarm mekanizması kurulmuştur. Bu yapı gerçek ağ cihazları, SDN controller metrikleri veya yapay zekâ tabanlı anomali tespit modülleriyle genişletilebilir.

Demo sonunda normal moda dönmek için:

```powershell
.\scripts\normal-traffic.ps1
```
