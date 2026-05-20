# Proje Raporu

## Cloud-Native Network Monitoring Sistemi

**Ders:** Akıllı Ağlar - SDN, Network Programlama ve Yapay Zekâ Uygulamaları  
**Proje konusu:** Cloud-native araçlarla network izleme, görselleştirme ve alarm mekanizması  
**Proje türü:** Uygulamalı yazılım ve sistem entegrasyonu  
**Hazırlanan çıktı:** Çalışan demo ortamı, proje raporu, sunum/demo akışı ve kaynak dosyalar

---

## 1. Ders Kapsamı ve Proje Bağlamı

“Akıllı Ağlar - SDN, Network Programlama ve Yapay Zekâ Uygulamaları” dersi kapsamında öğrencilerden modern ağ teknolojileriyle ilişkili bir konuda uygulama, proje raporu ve sunum hazırlamaları beklenmektedir. Bu proje, cloud-native gözlemlenebilirlik yaklaşımını ağ izleme alanına uygulamaktadır.

Proje değerlendirmesinde aşağıdaki kriterler dikkate alınmaktadır:

| Değerlendirme kriteri | Ağırlık | Bu projedeki karşılığı |
| --- | ---: | --- |
| Teknik doğruluk | %30 | Prometheus scrape modeli, PromQL sorguları, alert kuralları, Grafana datasource ve dashboard yapısı doğru şekilde kurulmuştur. |
| Uygulama başarısı | %30 | Docker Compose ile çalışan çok servisli bir monitoring ortamı oluşturulmuş, canlı metrik üretimi ve alert tetikleme başarıyla gösterilmiştir. |
| Sunum ve demo | %20 | 15 dakikayı aşmayacak canlı demo akışı hazırlanmıştır. Normal trafik, metrik izleme ve alert tetikleme senaryosu gösterilebilir durumdadır. |
| Dokümantasyon | %20 | Mimari, kurulum, çalışma mantığı, dosya yapısı, metrikler, alertler, demo adımları ve değerlendirme eşleştirmesi ayrıntılı olarak belgelenmiştir. |

Bu rapor, final haftasında yapılacak sunum ve proje teslimi için hazırlanmıştır. Proje maksimum 3 kişilik grup çalışmasına uygun olmakla birlikte tek kişi tarafından da sunulabilecek şekilde bağımsız ve çalıştırılabilir olarak tasarlanmıştır.

---

## 2. Projenin Amacı

Bu projenin amacı, modern cloud-native araçlar kullanarak canlı network telemetry verilerini izleyen, bu verileri grafiksel dashboard ile görselleştiren ve belirli eşik değerleri aşıldığında alarm üreten bir network monitoring sistemi kurmaktır.

Proje kapsamında hedeflenen ana çıktılar şunlardır:

- Prometheus ile canlı telemetry verilerinin toplanması.
- Grafana ile network dashboard oluşturulması.
- Alertmanager ile alarm yönetiminin gösterilmesi.
- Belirli bir senaryoda alert tetiklenmesinin canlı olarak kanıtlanması.
- Sistemin Docker Compose ile kolay çalıştırılabilir hale getirilmesi.

---

## 3. Problem Tanımı

Modern ağ altyapılarında trafik hacmi, bağlantı sayısı, gecikme ve paket kaybı gibi metrikler sürekli değişmektedir. Bu metriklerin manuel olarak takip edilmesi hem zor hem de hataya açıktır. Özellikle servis kalitesi, ağ performansı ve güvenlik açısından kritik eşiklerin aşılması hızlı şekilde fark edilmelidir.

Bu proje, aşağıdaki temel probleme çözüm üretmektedir:

> Bir ağ sistemindeki canlı metrikleri merkezi olarak nasıl toplayabilir, görselleştirebilir ve kritik durumlarda otomatik alarm üretebiliriz?

Bu soruya cevap olarak Prometheus, Grafana ve Alertmanager tabanlı bir cloud-native monitoring mimarisi kurulmuştur.

---

## 4. Kullanılan Teknolojiler

### 4.1 Docker Compose

Docker Compose, birden fazla servisi tek bir `docker-compose.yml` dosyası ile birlikte çalıştırmak için kullanılmıştır. Projede Prometheus, Grafana, Alertmanager, metric-app ve node-exporter servisleri aynı Docker network üzerinde çalışır.

### 4.2 Prometheus

Prometheus, sistemdeki ana telemetry toplama bileşenidir. Metric app tarafından yayınlanan `/metrics` endpointini belirli aralıklarla scrape eder. Toplanan verileri zaman serisi olarak saklar ve PromQL ile sorgulanabilir hale getirir.

Prometheus ayrıca alert rule dosyasında tanımlanan kuralları değerlendirir. Eşik değerleri belirli süre boyunca aşılırsa alert üretir.

### 4.3 Grafana

Grafana, Prometheus’tan alınan metrikleri görselleştirmek için kullanılmıştır. Dashboard otomatik provision edilmiştir. Kullanıcı Grafana arayüzünü açtığında hazır dashboard üzerinden latency, packet loss, bandwidth, packet rate, active connections ve firing alerts panellerini görebilir.

### 4.4 Alertmanager

Alertmanager, Prometheus tarafından üretilen alertleri merkezi olarak yönetir. Bu projede alertlerin gruplanması ve web arayüzünde görüntülenmesi için kullanılmıştır.

### 4.5 Metric App

Metric app, Python Flask ile yazılmıştır. Gerçek bir ağ ortamına ihtiyaç duymadan canlı network telemetry davranışı üretir. Normal, degraded ve alert olmak üzere üç farklı senaryo destekler.

### 4.6 Node Exporter

Node Exporter, sistem seviyesindeki temel metriklerin toplanabileceğini göstermek için projeye eklenmiştir. Bu bileşen, cloud-native monitoring sistemlerinde sık kullanılan exporter mantığını temsil eder.

---

## 5. Sistem Mimarisi

Sistemin genel akışı aşağıdaki gibidir:

```text
               +----------------+
               |   Metric App   |
               |  /metrics API  |
               +--------+-------+
                        |
                        | scrape
                        v
               +----------------+
               |   Prometheus   |
               | metrics + rules|
               +---+--------+---+
                   |        |
        datasource |        | alert
                   v        v
          +----------+   +--------------+
          | Grafana  |   | Alertmanager |
          | Dashboard|   | Alert UI     |
          +----------+   +--------------+
```

Sistem içindeki veri akışı:

1. Metric app, canlı network metriklerini üretir.
2. Prometheus, metric app üzerindeki `/metrics` endpointinden verileri toplar.
3. Prometheus, alert kurallarını düzenli olarak değerlendirir.
4. Grafana, Prometheus datasource üzerinden metrikleri görselleştirir.
5. Alert koşulları sağlanırsa Prometheus alert üretir.
6. Alertmanager, üretilen alertleri merkezi arayüzde gösterir.

---

## 6. Proje Dosya Yapısı

```text
cloud-native-network-monitoring/
├── docker-compose.yml
├── README.md
├── PROJECT_REPORT.md
├── DEMO_SCRIPT.md
├── PRESENTATION_PLAN.md
├── EVALUATION_CHECKLIST.md
├── metric-app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── prometheus/
│   ├── prometheus.yml
│   └── alerts.yml
├── alertmanager/
│   └── alertmanager.yml
├── grafana/
│   ├── dashboards/
│   │   └── network-monitoring-dashboard.json
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml
│       └── datasources/
│           └── prometheus.yml
├── scripts/
│   ├── trigger-alert.ps1
│   ├── normal-traffic.ps1
│   └── degraded-traffic.ps1
└── k8s/
    └── README.md
```

---

## 7. Metric App Tasarımı

Metric app, Python Flask kullanılarak geliştirilmiştir. Uygulama iki temel amaç taşır:

- Prometheus formatında metrik yayınlamak.
- Demo sırasında farklı trafik senaryoları üretmek.

Uygulamanın önemli endpointleri:

| Endpoint | Açıklama |
| --- | --- |
| `/` | Servis bilgisi ve mevcut senaryo bilgisini döndürür. |
| `/health` | Servisin çalışıp çalışmadığını kontrol eder. |
| `/status` | Mevcut senaryo ve anlık metrik durumlarını JSON olarak gösterir. |
| `/scenario` | Normal, degraded veya alert moduna geçiş sağlar. |
| `/metrics` | Prometheus formatında metrikleri yayınlar. |

Desteklenen senaryolar:

| Senaryo | Açıklama |
| --- | --- |
| `normal` | Gecikme, paket kaybı, bant genişliği ve bağlantı sayısı normal değerlerdedir. |
| `degraded` | Ağ performansı bozulmaya başlar, fakat her zaman kritik alert oluşmayabilir. |
| `alert` | Metrikler bilinçli olarak eşik üstüne çıkarılır ve alert tetiklenir. |

---

## 8. Toplanan Network Metrikleri

Projede aşağıdaki metrikler kullanılmıştır:

| Metrik adı | Tür | Açıklama |
| --- | --- | --- |
| `network_latency_ms` | Gauge | Anlık ağ gecikmesini milisaniye cinsinden gösterir. |
| `network_packet_loss_percent` | Gauge | Paket kaybı yüzdesini gösterir. |
| `network_active_connections` | Gauge | Aktif bağlantı sayısını gösterir. |
| `network_bandwidth_mbps` | Gauge | Bant genişliği kullanımını Mbps cinsinden gösterir. |
| `network_packets_total` | Counter | Direction ve protocol etiketleriyle toplam paket sayısını tutar. |
| `network_traffic_bytes_total` | Counter | Direction ve protocol etiketleriyle toplam trafik miktarını byte olarak tutar. |
| `network_alert_scenario_enabled` | Gauge | Alert senaryosunun aktif olup olmadığını gösterir. |

Bu metriklerin bir kısmı anlık değerleri, bir kısmı ise zaman içinde artan sayaçları temsil eder. Grafana dashboardunda hem gauge hem time series panelleri kullanılmıştır.

---

## 9. Prometheus Yapılandırması

Prometheus yapılandırması `prometheus/prometheus.yml` dosyasında tanımlanmıştır.

Temel ayarlar:

- `scrape_interval: 5s`
- `evaluation_interval: 5s`
- Metric app target: `metric-app:5000`
- Node exporter target: `node-exporter:9100`
- Prometheus self-monitoring target: `prometheus:9090`

Bu yapılandırma sayesinde Prometheus her 5 saniyede bir metrikleri toplar. Demo ortamında hızlı geri bildirim alınabilmesi için kısa scrape interval tercih edilmiştir.

---

## 10. Alert Kuralları

Alert kuralları `prometheus/alerts.yml` dosyasında yer alır.

| Alert adı | PromQL koşulu | Süre | Seviye | Anlamı |
| --- | --- | --- | --- | --- |
| `HighNetworkLatency` | `network_latency_ms > 150` | 15s | warning | Ağ gecikmesi kabul edilebilir seviyenin üstüne çıkmıştır. |
| `HighPacketLoss` | `network_packet_loss_percent > 5` | 15s | critical | Paket kaybı kritik seviyeye ulaşmıştır. |
| `HighBandwidthUsage` | `network_bandwidth_mbps > 800` | 15s | critical | Bant genişliği kullanımı aşırı yükselmiştir. |
| `TooManyActiveConnections` | `network_active_connections > 600` | 15s | warning | Aktif bağlantı sayısı olağan dışı artmıştır. |

Kurallarda `for: 15s` kullanılması, metrik değeri eşik üstüne kısa süreli çıktığında hemen alarm üretmemeyi sağlar. Bu, gerçek sistemlerde yanlış pozitif alertleri azaltmak için kullanılan önemli bir yaklaşımdır.

---

## 11. Grafana Dashboard

Grafana dashboardu `grafana/dashboards/network-monitoring-dashboard.json` dosyasında tanımlanmıştır. Datasource otomatik olarak `grafana/provisioning/datasources/prometheus.yml` ile eklenir.

Dashboard panelleri:

| Panel | Açıklama |
| --- | --- |
| Network Latency | Anlık gecikmeyi gauge panelinde gösterir. |
| Packet Loss | Paket kaybı yüzdesini gauge panelinde gösterir. |
| Bandwidth Usage | Bant genişliği kullanımını zaman serisi olarak gösterir. |
| Packet Rate | Protokol ve yön bazlı paket akış hızını gösterir. |
| Active Connections | Aktif bağlantı sayısının zaman içindeki değişimini gösterir. |
| Alert Scenario Enabled | Demo alert senaryosunun aktif olup olmadığını gösterir. |
| Firing Alerts | Prometheus içinde firing durumunda olan alertleri tablo olarak gösterir. |

Dashboard 5 saniyede bir otomatik yenilenecek şekilde ayarlanmıştır.

---

## 12. Alertmanager Yapılandırması

Alertmanager yapılandırması `alertmanager/alertmanager.yml` dosyasında bulunur.

Bu projede Alertmanager:

- Alertleri `demo-console` receiver altında toplar.
- Alertleri `alertname` ve `severity` alanlarına göre gruplar.
- Critical alert varsa aynı component için warning alertleri inhibit edebilir.
- Web arayüzü üzerinden alertlerin gözlemlenmesini sağlar.

Gerçek bir production ortamında Alertmanager e-posta, Slack, Microsoft Teams, webhook veya PagerDuty gibi sistemlere bağlanabilir. Bu projede ders demosu için web arayüzü yeterli tutulmuştur.

---

## 13. Kurulum ve Çalıştırma

### 13.1 Gereksinimler

- Windows işletim sistemi
- Docker Desktop
- Docker Compose
- Web tarayıcısı

### 13.2 Projeyi Başlatma

```powershell
cd "C:\Users\mut46\Documents\ULAK FİNAL\cloud-native-network-monitoring"
docker compose up -d --build
```

### 13.3 Servis Adresleri

| Servis | Adres |
| --- | --- |
| Grafana | `http://localhost:3000` |
| Prometheus | `http://localhost:9090` |
| Alertmanager | `http://localhost:9093` |
| Metric App | `http://localhost:5000` |

Grafana kullanıcı bilgileri:

```text
Kullanıcı adı: admin
Şifre: admin
```

### 13.4 Servisleri Durdurma

```powershell
docker compose down
```

Verileri de temizlemek için:

```powershell
docker compose down -v
```

---

## 14. Uygulamalı Demo Senaryosu

Demo senaryosu ders sunumunda canlı olarak gösterilecek şekilde tasarlanmıştır.

### 14.1 Normal Durum

Sistem ilk açıldığında metric app normal trafik üretir. Bu durumda:

- Latency düşük seviyededir.
- Packet loss düşük seviyededir.
- Bandwidth kullanımı normal aralıktadır.
- Active connection sayısı olağan seviyededir.
- Prometheus targets ekranında servisler `UP` görünür.

Kontrol adresi:

```text
http://localhost:9090/targets
```

### 14.2 Dashboard İzleme

Grafana dashboard açılır:

```text
http://localhost:3000
```

Dashboard yolu:

```text
Dashboards > Cloud Native Monitoring > Cloud-Native Network Monitoring
```

Burada canlı network metrikleri grafikler üzerinden izlenir.

### 14.3 Alert Senaryosunu Tetikleme

Proje klasöründe şu komut çalıştırılır:

```powershell
.\scripts\trigger-alert.ps1
```

Bu komut metric app üzerinde `alert` modunu etkinleştirir. Alert modunda metrikler bilinçli olarak yüksek değerlere çıkar:

- Latency 150 ms üstüne çıkar.
- Packet loss %5 üstüne çıkar.
- Bandwidth 800 Mbps üstüne çıkar.
- Active connection sayısı 600 üstüne çıkar.

### 14.4 Alertlerin Gözlemlenmesi

Prometheus alert ekranı:

```text
http://localhost:9090/alerts
```

Alertmanager ekranı:

```text
http://localhost:9093/#/alerts
```

Beklenen alertler:

- `HighNetworkLatency`
- `HighPacketLoss`
- `HighBandwidthUsage`
- `TooManyActiveConnections`

### 14.5 Normal Duruma Dönüş

Demo bittikten sonra sistem normal moda alınır:

```powershell
.\scripts\normal-traffic.ps1
```

Kısa süre sonra metrikler düşer ve alertler resolved durumuna döner.

---

## 15. Test ve Doğrulama

Projenin çalıştığı aşağıdaki ekranlarla doğrulanmıştır:

- Grafana dashboard ekranında canlı metriklerin görünmesi.
- Prometheus `/targets` ekranında targetların `UP` olması.
- Prometheus `/graph` ekranında PromQL sorgularının değer döndürmesi.
- Prometheus `/alerts` ekranında alertlerin `firing` durumuna geçmesi.
- Alertmanager `/alerts` ekranında alertlerin gruplanmış olarak görünmesi.
- Metric app ana sayfasında senaryonun `alert` olarak görünmesi.

Örnek PromQL sorguları:

```promql
network_latency_ms
network_packet_loss_percent
network_bandwidth_mbps
network_active_connections
ALERTS{alertstate="firing"}
```

Bu doğrulamalar projenin hem telemetry toplama hem görselleştirme hem de alert üretme gereksinimlerini karşıladığını göstermektedir.

---

## 16. Değerlendirme Kriterlerine Göre Proje Analizi

### 16.1 Teknik Doğruluk (%30)

Proje teknik olarak doğru bir observability mimarisi kullanmaktadır. Prometheus pull-based scrape modeliyle çalışır. Metric app Prometheus formatında metrik yayınlar. Grafana, Prometheus datasource üzerinden veri çeker. Alert kuralları PromQL ifadeleriyle tanımlanmıştır. Alertmanager, Prometheus alert akışına doğru şekilde bağlanmıştır.

Teknik doğruluk açısından güçlü noktalar:

- Servisler aynı Docker network içinde çalışmaktadır.
- Prometheus targetları `UP` durumundadır.
- Metrikler PromQL ile sorgulanabilmektedir.
- Alert rule mantığı doğru şekilde kurulmuştur.
- Dashboard panelleri gerçek zamanlı veriye bağlıdır.

### 16.2 Uygulama Başarısı (%30)

Uygulama başarıyla çalışmaktadır. Sistem tek komutla ayağa kalkar. Demo için ayrı scriptler hazırlanmıştır. Alert senaryosu canlı olarak tetiklenebilir ve sonuçlar hem Grafana hem Prometheus hem Alertmanager üzerinde görülebilir.

Uygulama başarısı açısından güçlü noktalar:

- Tek komutla kurulum: `docker compose up -d --build`
- Otomatik dashboard provisioning
- Otomatik datasource provisioning
- Hazır alert tetikleme scripti
- Normal moda dönüş scripti
- Canlı metrik üretimi

### 16.3 Sunum ve Demo (%20)

Sunum 15 dakikayı geçmeyecek şekilde planlanmıştır. Demo akışı nettir:

1. Mimari kısa anlatılır.
2. Servislerin ayakta olduğu gösterilir.
3. Grafana dashboard üzerinden canlı metrikler izlenir.
4. Alert senaryosu çalıştırılır.
5. Prometheus ve Alertmanager üzerinde alertlerin tetiklendiği gösterilir.
6. Sistem normal moda döndürülür.

Bu akış, uygulamanın çalıştığını canlı olarak göstermeye yeterlidir.

### 16.4 Dokümantasyon (%20)

Dokümantasyon; mimari, kurulum, çalışma mantığı, dosya yapısı, metrikler, alertler, demo komutları, doğrulama adımları ve değerlendirme kriterlerini içermektedir. Bu nedenle proje teslimi için gerekli açıklama seviyesi sağlanmıştır.

---

## 17. SDN ve Akıllı Ağlar ile İlişki

Bu proje doğrudan bir SDN controller uygulaması olmasa da akıllı ağların temel gereksinimlerinden biri olan gözlemlenebilirlik katmanını kurmaktadır. SDN tabanlı ağlarda controller kararlarının doğru verilebilmesi için ağdan sürekli telemetry verisi alınması gerekir.

Bu monitoring sistemi SDN ortamına şu şekilde genişletilebilir:

- Switch, router veya SDN controller metrikleri Prometheus exporter ile toplanabilir.
- Trafik yoğunluğu arttığında controller üzerinden route değişikliği yapılabilir.
- Paket kaybı arttığında alternatif path seçilebilir.
- Alertmanager webhook ile otomatik müdahale sistemi tetiklenebilir.
- Yapay zekâ modeli, toplanan metrikler üzerinden anomali tespiti yapabilir.

Bu açıdan proje, SDN ve yapay zekâ uygulamalarına temel oluşturabilecek telemetry ve monitoring altyapısını göstermektedir.

---

## 18. Gerçek Ortama Genişletme Önerileri

Bu demo proje aşağıdaki geliştirmelerle production benzeri bir sisteme dönüştürülebilir:

- Kubernetes üzerinde Prometheus Operator kullanımı.
- Gerçek router/switch exporter entegrasyonu.
- SNMP exporter ile ağ cihazlarından metrik toplama.
- Blackbox exporter ile endpoint erişilebilirlik testi.
- Alertmanager e-posta veya Teams bildirimi.
- Grafana kullanıcı yetkilendirme ve dashboard paylaşımı.
- Uzun süreli metrik saklama için Thanos veya Cortex kullanımı.
- Yapay zekâ tabanlı anomali tespit modülü eklenmesi.

---

## 19. Sonuç

Bu proje kapsamında cloud-native araçlar kullanılarak uçtan uca çalışan bir network monitoring sistemi kurulmuştur. Prometheus ile canlı telemetry verileri toplanmış, Grafana ile görselleştirilmiş ve Alertmanager ile alarm yönetimi sağlanmıştır. Demo senaryosu üzerinden belirli eşik değerleri aşıldığında alertlerin tetiklendiği canlı olarak gösterilmiştir.

Sonuç olarak proje, verilen konu gereksinimlerini karşılamaktadır:

- Canlı network telemetry verisi üretilmiştir.
- Prometheus ile metrik toplama yapılmıştır.
- Grafana dashboard oluşturulmuştur.
- Alert kuralları tanımlanmıştır.
- Alertmanager ile alarm mekanizması gösterilmiştir.
- Uygulamalı demo senaryosu başarıyla çalıştırılmıştır.

Bu çalışma, akıllı ağlarda gözlemlenebilirlik, otomasyon ve olay yönetimi kavramlarını uygulamalı olarak göstermektedir.
