$ErrorActionPreference = "Stop"

$baseUrl = $env:METRIC_APP_URL
if ([string]::IsNullOrWhiteSpace($baseUrl)) {
    $baseUrl = "http://localhost:5000"
}

Write-Host "Bozulmus trafik senaryosu etkinlestiriliyor: $baseUrl/scenario"
Invoke-RestMethod -Method Post -Uri "$baseUrl/scenario" -ContentType "application/json" -Body '{"mode":"degraded"}'

Write-Host ""
Write-Host "Dashboard uzerinde gecikme ve paket kaybi artislarini izleyebilirsin."
