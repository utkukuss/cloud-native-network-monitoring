# Değerlendirme Kontrol Listesi

Bu dosya, ders yönergesindeki değerlendirme başlıklarına göre projenin hangi koşulları karşıladığını göstermek için hazırlanmıştır.

## 1. Teknik Doğruluk (%30)

| Kontrol | Durum | Kanıt |
| --- | --- | --- |
| Prometheus kullanıldı mı? | Sağlandı | `prometheus/prometheus.yml` ve `http://localhost:9090` |
| Telemetry verisi toplanıyor mu? | Sağlandı | `http://localhost:9090/targets` ekranında targetlar `UP` |
| PromQL ile metrik sorgulanabiliyor mu? | Sağlandı | `network_latency_ms`, `network_packet_loss_percent`, `network_bandwidth_mbps` |
| Alert kuralları doğru tanımlandı mı? | Sağlandı | `prometheus/alerts.yml` |
| Alertmanager bağlantısı kuruldu mu? | Sağlandı | `alerting.alertmanagers` yapılandırması ve `http://localhost:9093` |
| Grafana datasource doğru mu? | Sağlandı | `grafana/provisioning/datasources/prometheus.yml` |

## 2. Uygulama Başarısı (%30)

| Kontrol | Durum | Kanıt |
| --- | --- | --- |
| Sistem tek komutla çalışıyor mu? | Sağlandı | `docker compose up -d --build` |
| Metric app çalışıyor mu? | Sağlandı | `http://localhost:5000` |
| Dashboard otomatik geliyor mu? | Sağlandı | Grafana dashboard provisioning |
| Normal trafik senaryosu var mı? | Sağlandı | `scripts/normal-traffic.ps1` |
| Alert senaryosu var mı? | Sağlandı | `scripts/trigger-alert.ps1` |
| Alertler canlı tetikleniyor mu? | Sağlandı | Prometheus Alerts ve Alertmanager ekranları |

## 3. Sunum ve Demo (%20)

| Kontrol | Durum | Kanıt |
| --- | --- | --- |
| 15 dakikalık sunum planı hazır mı? | Sağlandı | `PRESENTATION_PLAN.md` |
| Canlı dashboard gösterimi var mı? | Sağlandı | Grafana dashboard |
| Canlı metrik sorgulama var mı? | Sağlandı | Prometheus Graph ekranı |
| Alert tetikleme gösterimi var mı? | Sağlandı | `trigger-alert.ps1` |
| Alertmanager gösterimi var mı? | Sağlandı | `http://localhost:9093/#/alerts` |

## 4. Dokümantasyon (%20)

| Kontrol | Durum | Kanıt |
| --- | --- | --- |
| Proje amacı açıklandı mı? | Sağlandı | `PROJECT_REPORT.md` |
| Mimari açıklandı mı? | Sağlandı | `PROJECT_REPORT.md` ve `README.md` |
| Kurulum adımları var mı? | Sağlandı | `README.md` |
| Dosya yapısı açıklandı mı? | Sağlandı | `PROJECT_REPORT.md` |
| Metrikler açıklandı mı? | Sağlandı | `PROJECT_REPORT.md` |
| Alert kuralları açıklandı mı? | Sağlandı | `PROJECT_REPORT.md` |
| Demo akışı açıklandı mı? | Sağlandı | `DEMO_SCRIPT.md` ve `PRESENTATION_PLAN.md` |

## Sonuç

Proje, verilen yönergede istenen uygulama, proje raporu, sunum ve demo gereksinimlerini karşılamaktadır. Canlı network metrikleri Prometheus ile toplanmakta, Grafana ile görselleştirilmekte ve belirlenen eşik değerlerinde alert mekanizması çalışmaktadır.
