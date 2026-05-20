# Uygulamali Gosterim Konusma Akisi

## 1. Sistemi Baslatma

```powershell
cd "C:\Users\mut46\Documents\ULAK FİNAL\cloud-native-network-monitoring"
docker compose up -d --build
```

Anlatim:

Bu komut ile metric app, Prometheus, Grafana, Alertmanager ve node-exporter servisleri ayni Docker networku icinde baslatilir.

## 2. Prometheus Target Kontrolu

Adres:

```text
http://localhost:9090/targets
```

Anlatim:

Prometheus target ekraninda `network-metric-app`, `prometheus` ve `node-exporter` servislerinin UP durumda oldugunu gosteriyorum. Bu, telemetry toplama kisminin calistigini kanitlar.

## 3. Grafana Dashboard

Adres:

```text
http://localhost:3000
```

Giris:

```text
admin / admin
```

Anlatim:

Grafana dashboardunda latency, packet loss, bandwidth, packet rate ve active connection metriklerini canli olarak izliyorum. Dashboard Prometheus datasource ile otomatik provision edildi.

## 4. Alert Tetikleme

```powershell
.\scripts\trigger-alert.ps1
```

Anlatim:

Bu komut uygulamayi alert senaryosuna alir. Sistem yuksek trafik, yuksek gecikme, paket kaybi ve fazla aktif baglanti uretmeye baslar.

## 5. Alertleri Gosterme

Prometheus:

```text
http://localhost:9090/alerts
```

Alertmanager:

```text
http://localhost:9093
```

Anlatim:

Prometheus alert kurallari 15 saniye boyunca esiklerin asildigini gorunce alertleri firing durumuna alir. Alertmanager bu alertleri alir, gruplar ve merkezi bir alert yonetim ekrani sunar.

## 6. Sistemi Normale Dondurme

```powershell
.\scripts\normal-traffic.ps1
```

Anlatim:

Normal trafik moduna donuldugunde metrikler dusmeye baslar ve alertler kisa sure sonra resolved olur.
