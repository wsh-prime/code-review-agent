function Start-RunTranscript {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $logDir = Join-Path $ProjectRoot "outputs/logs"
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $logPath = Join-Path $logDir "$Name-$timestamp.log"
    try {
        Start-Transcript -Path $logPath -Force | Out-Null
        return @{
            Started = $true
            Path = $logPath
        }
    } catch {
        Write-Warning "Could not start transcript logging: $($_.Exception.Message)"
        return @{
            Started = $false
            Path = $logPath
        }
    }
}

function Stop-RunTranscript {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Transcript
    )

    if (-not $Transcript.Started) {
        return
    }

    try {
        Stop-Transcript | Out-Null
        Write-Host "Log: $($Transcript.Path)"
    } catch {
        Write-Warning "Could not stop transcript logging: $($_.Exception.Message)"
    }
}
