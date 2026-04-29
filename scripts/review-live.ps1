param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,

    [Parameter(Mandatory = $true)]
    [string]$Diff,

    [string]$Out = "outputs/live-review",

    [ValidateSet("rules", "hybrid-fake", "hybrid-live")]
    [string]$Mode = "hybrid-live",

    [string]$EnvFile = "",

    [switch]$ExportPrompts
)

$ErrorActionPreference = "Stop"

# Resolve EnvFile default here, after $PSScriptRoot is guaranteed to be set
if (-not $EnvFile) {
    $EnvFile = Join-Path $PSScriptRoot "review-live.env.local"
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
    if ($Mode -ne "hybrid-live") {
        return
    }

    if (-not $env:SILICONFLOW_API_KEY -and -not $env:OPENAI_COMPATIBLE_API_KEY) {
        throw @"
hybrid-live requires an API key.

Either set it in the current shell:
  `$env:SILICONFLOW_API_KEY = "sk-..."

Or copy scripts/review-live.env.example to scripts/review-live.env.local and fill:
  SILICONFLOW_API_KEY=sk-...
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
Import-EnvFile -Path $EnvFile
Require-LiveConfig

$srcPath = Join-Path $ProjectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

$argsList = @(
    "-m", "code_review_agent.cli",
    "review",
    "--repo", $Repo,
    "--diff", $Diff,
    "--out", $Out,
    "--mode", $Mode
)

if ($ExportPrompts) {
    $argsList += "--export-prompts"
}

Write-Host "Code Review Agent live runner"
Write-Host "Repo:  $Repo"
Write-Host "Diff:  $Diff"
Write-Host "Out:   $Out"
Write-Host "Mode:  $Mode"
if ($Mode -eq "hybrid-live") {
    $model = if ($env:SILICONFLOW_MODEL) { $env:SILICONFLOW_MODEL } else { $env:OPENAI_COMPATIBLE_MODEL }
    $baseUrl = if ($env:SILICONFLOW_BASE_URL) { $env:SILICONFLOW_BASE_URL } else { $env:OPENAI_COMPATIBLE_BASE_URL }
    Write-Host "Model: $model"
    Write-Host "Base:  $baseUrl"
}
Write-Host ""

Push-Location $ProjectRoot
try {
    & python @argsList
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
}
