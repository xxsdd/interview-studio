param([Parameter(Mandatory=$true)][string]$InputPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$payload = [System.IO.File]::ReadAllText($InputPath, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $prefix = [string]$payload.language
    $voice = $speaker.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name.StartsWith($prefix) } | Select-Object -First 1
    if (-not $voice) { throw 'No matching voice installed.' }
    $speaker.SelectVoice($voice.VoiceInfo.Name)
    $speaker.Rate = -1
    $speaker.SetOutputToWaveFile([string]$payload.output)
    $speaker.Speak([string]$payload.text)
} finally {
    $speaker.Dispose()
}
