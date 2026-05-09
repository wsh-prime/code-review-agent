param(
    [string]$Repo = ".",
    [string]$BaseRef = "origin/main",
    [string]$Diff = ".tmp/changes.patch",
    [string]$Out = "",
    [string]$EnvFile = "scripts/review-live.env.local",
    [string]$RepoMap = "outputs/my-map/repo_map.json",
    [string]$Hygiene = "outputs/my-hygiene/project_hygiene.json",
    [switch]$ExportPrompts,
    [switch]$Resume,
    [bool]$FetchBaseRef = $true,
    [bool]$GenerateDiff = $true,
    [int]$ContextBudget = 24000,
    [int]$MaxFilesPerAgentCall = 8,
    [int]$MaxEvidencePerFile = 80,
    [int]$MaxContextRefillRounds = 1,
    [int]$MaxContextRequests = 8
)

$ErrorActionPreference = "Stop"

# Edit these values before running or pass parameters.
if (-not $Out) {
    $Out = "outputs/runs/$(Get-Date -Format 'yyyyMMdd-HHmmss')/review"
}

function Import-EnvFile {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    Get-Content -LiteralPath $Path | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) {
            return
        }

        $key, $value = $line -split "=", 2
        if (-not $key -or $null -eq $value) {
            return
        }

        $cleanValue = $value.Trim().Trim('"').Trim("'")
        Set-Item -Path "Env:$($key.Trim())" -Value $cleanValue
    }
}

function Require-LiveConfig {
    if (-not $env:SILICONFLOW_API_KEY -and -not $env:OPENAI_COMPATIBLE_API_KEY) {
        throw @"
hybrid-live requires an API key.

Fill scripts/review-live.env.local or set:
  `$env:SILICONFLOW_API_KEY = "sk-..."
"@
    }

    if (-not $env:SILICONFLOW_BASE_URL -and -not $env:OPENAI_COMPATIBLE_BASE_URL) {
        $env:SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
    }
    if (-not $env:SILICONFLOW_MODEL -and -not $env:OPENAI_COMPATIBLE_MODEL) {
        $env:SILICONFLOW_MODEL = "deepseek-ai/DeepSeek-V4-Flash"
    }
}

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-review-llm"
$srcPath = Join-Path $ProjectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

Push-Location $ProjectRoot
try {
    Import-EnvFile -Path $EnvFile
    Require-LiveConfig

    if ($FetchBaseRef) {
        & git fetch origin
        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }
    }

    if ($GenerateDiff) {
        & git add -N .
        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }

        $diffDir = Split-Path -Parent $Diff
        if ($diffDir -and -not (Test-Path -LiteralPath $diffDir)) {
            New-Item -ItemType Directory -Path $diffDir | Out-Null
        }

        $diffPathspec = $Diff -replace "\\", "/"
        & git diff --binary $BaseRef -- . ":(exclude)$diffPathspec" ":(exclude)changes.patch" |
            Out-File -LiteralPath $Diff -Encoding utf8
    }

    $argsList = @(
        "-m", "code_review_agent.cli",
        "review",
        "--repo", $Repo,
        "--diff", $Diff,
        "--out", $Out,
        "--mode", "hybrid-live",
        "--context-budget", "$ContextBudget",
        "--max-files-per-agent-call", "$MaxFilesPerAgentCall",
        "--max-evidence-per-file", "$MaxEvidencePerFile",
        "--max-context-refill-rounds", "$MaxContextRefillRounds",
        "--max-context-requests", "$MaxContextRequests"
    )

    if ($RepoMap -and (Test-Path -LiteralPath $RepoMap)) {
        $argsList += @("--repo-map", $RepoMap)
    }
    if ($Hygiene -and (Test-Path -LiteralPath $Hygiene)) {
        $argsList += @("--hygiene", $Hygiene)
    }
    if ($ExportPrompts) {
        $argsList += "--export-prompts"
    }
    if ($Resume) {
        $argsList += "--resume"
    }

    $model = if ($env:SILICONFLOW_MODEL) { $env:SILICONFLOW_MODEL } else { $env:OPENAI_COMPATIBLE_MODEL }
    $baseUrl = if ($env:SILICONFLOW_BASE_URL) { $env:SILICONFLOW_BASE_URL } else { $env:OPENAI_COMPATIBLE_BASE_URL }

    Write-Host "Code Review Agent - review hybrid-live"
    Write-Host "Repo:     $Repo"
    Write-Host "BaseRef:  $BaseRef"
    Write-Host "Diff:     $Diff"
    Write-Host "Out:      $Out"
    Write-Host "Model:    $model"
    Write-Host "Base URL: $baseUrl"
    Write-Host ""

    & python @argsList
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
