param()

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-all-llm"

Push-Location $ProjectRoot
try {
    & powershell -ExecutionPolicy Bypass -File "scripts/run-map.ps1"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & powershell -ExecutionPolicy Bypass -File "scripts/run-hygiene-llm.ps1"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & powershell -ExecutionPolicy Bypass -File "scripts/run-review-llm.ps1"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
