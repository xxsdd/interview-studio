$ErrorActionPreference = 'Stop'
$pidFile = Join-Path $PSScriptRoot 'data\server.pid'
if (Test-Path -LiteralPath $pidFile) {
    $serverId = [int](Get-Content -LiteralPath $pidFile)
    $processInfo = Get-CimInstance Win32_Process -Filter "ProcessId=$serverId"
    if ($processInfo -and $processInfo.CommandLine -match 'uvicorn' -and $processInfo.CommandLine -match '--port 8766') {
        Stop-Process -Id $serverId
        Write-Output 'Interview studio stopped.'
    }
}
