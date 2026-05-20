$ErrorActionPreference = "Stop"

$baseUrl = $env:METRIC_APP_URL
if ([string]::IsNullOrWhiteSpace($baseUrl)) {
    $baseUrl = "http://localhost:5000"
}

Write-Host "Normal trafik senaryosu etkinlestiriliyor: $baseUrl/scenario"
Invoke-RestMethod -Method Post -Uri "$baseUrl/scenario" -ContentType "application/json" -Body '{"mode":"normal"}'

Write-Host ""
Write-Host "Alertler kisa sure sonra resolved durumuna donecektir."
