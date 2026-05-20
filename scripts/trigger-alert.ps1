$ErrorActionPreference = "Stop"

$baseUrl = $env:METRIC_APP_URL
if ([string]::IsNullOrWhiteSpace($baseUrl)) {
    $baseUrl = "http://localhost:5000"
}

Write-Host "Alert senaryosu etkinlestiriliyor: $baseUrl/scenario"
Invoke-RestMethod -Method Post -Uri "$baseUrl/scenario" -ContentType "application/json" -Body '{"mode":"alert"}'

Write-Host ""
Write-Host "15-30 saniye icinde Prometheus alertleri firing durumuna gececektir."
Write-Host "Prometheus Alerts: http://localhost:9090/alerts"
Write-Host "Alertmanager:      http://localhost:9093"
