param(
    [bool] $IncludeDrafts = $true,
    [string] $Destination = 'public',
    [string] $BaseURL = ''
)

$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path -Parent $PSScriptRoot
$requiredVersion = (Get-Content -Raw -LiteralPath (Join-Path $siteRoot '.hugo-version')).Trim()
$installedVersion = (& hugo version) -join "`n"

if ($installedVersion -notmatch "hugo v$([regex]::Escape($requiredVersion))([+-]|\s)") {
    throw "This site requires Hugo $requiredVersion; found: $installedVersion"
}

$arguments = @(
    '--source', $siteRoot,
    '--destination', (Join-Path $siteRoot $Destination),
    '--gc',
    '--minify',
    '--panicOnWarning'
)

if ($IncludeDrafts) {
    $arguments += '--buildDrafts'
}

if ($BaseURL) {
    $arguments += @('--baseURL', $BaseURL)
}

& hugo @arguments
exit $LASTEXITCODE
