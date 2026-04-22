param(
    [ValidateSet("smoke", "full")]
    [string]$Mode = "smoke",
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
} else {
    $ProjectRoot = (Resolve-Path $ProjectRoot).Path
}

Set-Location $ProjectRoot

$tmpRoot = Join-Path $ProjectRoot ".tmp\\pytest"
New-Item -ItemType Directory -Path $tmpRoot -Force | Out-Null

$env:TMP = $tmpRoot
$env:TEMP = $tmpRoot
$env:PYTHONPATH = ".claude/scripts"

# Avoid Windows basetemp directory permission/residual lock causing rm_rf failure (would cause all test cases to error directly at setup stage).
$runId = Get-Date -Format "yyyyMMdd_HHmmssfff"
$baseTemp = Join-Path $tmpRoot ("run-" + $Mode + "-" + $runId)

Write-Host "ProjectRoot: $ProjectRoot"
Write-Host "TMP/TEMP: $tmpRoot"
Write-Host "Mode: $Mode"

# Pre-check: Some Windows Python distributions (especially WindowsApps shim) create “inaccessible directories” when tempfile.mkdtemp is called,
# which causes pytest to directly WinError 5 during temporary directory creation/cleanup stage.
@'
import tempfile
from pathlib import Path
import sys

try:
    d = Path(tempfile.mkdtemp(prefix=”wordsmith_writer_pytest_”))
    # Must be able to list directories and write files; otherwise pytest will fail.
    list(d.iterdir())
    (d / “probe.txt”).write_text(“ok”, encoding=”utf-8”)
except Exception as exc:
    print(f”PYTEST_TMPDIR_PRECHECK_FAILED: {type(exc).__name__}: {exc}”, file=sys.stderr)
    raise
'@ | python - 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host “”
    Write-Host “❌ Python temporary directory pre-check failed (common cause: WindowsApps python.exe shim / permission issue)”
    Write-Host “Suggestion: Use standard Python (python.org installer) or use Python provided by uv/uvx to run tests.”
    exit 1
}

if ($Mode -eq "smoke") {
    python -m pytest -q `
        .claude/scripts/data_modules/tests/test_extract_chapter_context.py `
        .claude/scripts/data_modules/tests/test_rag_adapter.py `
        --basetemp $baseTemp `
        --no-cov `
        -p no:cacheprovider
    exit $LASTEXITCODE
}

python -m pytest -q `
    .claude/scripts/data_modules/tests `
    --basetemp $baseTemp `
    -p no:cacheprovider
exit $LASTEXITCODE
