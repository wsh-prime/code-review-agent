param(
    [string]$Repo = ".",
    [string]$Out = "",
    [string]$Summary = ""
)

$ErrorActionPreference = "Stop"

# Edit these values before running or pass parameters.
if (-not $Out) {
    $Out = "outputs/runs/$(Get-Date -Format 'yyyyMMdd-HHmmss')/hygiene"
}

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-hygiene-llm"
$srcPath = Join-Path $ProjectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

$argsList = @(
    "-m", "code_review_agent.cli",
    "hygiene",
    "--repo", $Repo,
    "--out", $Out,
    "--classifier", "hybrid"
)

if ($Summary) {
    $argsList += @("--summary", $Summary)
}

Push-Location $ProjectRoot
try {
    Write-Host "Code Review Agent - hygiene hybrid"
    Write-Host "Repo:       $Repo"
    Write-Host "Out:        $Out"
    Write-Host "Classifier: hybrid"
    Write-Host ""

    & python @argsList
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
