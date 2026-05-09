param(
    [string]$Repo = ".",
    [string]$BaseRef = "origin/main",
    [string]$RunRoot = "",
    [switch]$Resume
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-all-llm"

Push-Location $ProjectRoot
try {
    if (-not $RunRoot) {
        $RunRoot = "outputs/runs/$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    }

    $MapOut = Join-Path $RunRoot "map"
    $HygieneOut = Join-Path $RunRoot "hygiene"
    $ReviewOut = Join-Path $RunRoot "review"
    $Diff = Join-Path $RunRoot "changes.patch"
    $RepoMap = Join-Path $MapOut "repo_map.json"
    $Hygiene = Join-Path $HygieneOut "project_hygiene.json"

    Write-Host "Code Review Agent - full LLM run"
    Write-Host "Repo:    $Repo"
    Write-Host "BaseRef: $BaseRef"
    Write-Host "RunRoot: $RunRoot"
    Write-Host "Diff:    $Diff"
    Write-Host ""

    & powershell -ExecutionPolicy Bypass -File "scripts/run-map.ps1" `
        -Repo $Repo `
        -Out $MapOut
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    & powershell -ExecutionPolicy Bypass -File "scripts/run-hygiene-llm.ps1" `
        -Repo $Repo `
        -Out $HygieneOut
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    $reviewArgs = @(
        "-ExecutionPolicy", "Bypass",
        "-File", "scripts/run-review-llm.ps1",
        "-Repo", $Repo,
        "-BaseRef", $BaseRef,
        "-Diff", $Diff,
        "-Out", $ReviewOut,
        "-RepoMap", $RepoMap,
        "-Hygiene", $Hygiene,
        "-ExportPrompts"
    )
    if ($Resume) {
        $reviewArgs += "-Resume"
    }

    & powershell @reviewArgs
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
