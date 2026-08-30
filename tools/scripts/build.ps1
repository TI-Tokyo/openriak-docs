param(
    [bool] $IncludeDrafts = $true,
    [string] $Destination = 'public',
    [string] $BaseURL = 'https://www.openriak.org/docs/'
)

$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$requiredVersion = (Get-Content -Raw -LiteralPath (Join-Path $siteRoot '.hugo-version')).Trim()
$installedVersion = (& hugo version) -join "`n"
if ($installedVersion -notmatch "hugo v$([regex]::Escape($requiredVersion))([+-]|\s)") {
    throw "This site requires Hugo $requiredVersion; found: $installedVersion"
}

if (-not $BaseURL.EndsWith('/')) { $BaseURL += '/' }
$destinationRoot = if ([IO.Path]::IsPathRooted($Destination)) { $Destination } else { Join-Path $siteRoot $Destination }

if (Get-Command node -ErrorAction SilentlyContinue) {
    & node (Join-Path $PSScriptRoot 'sync-product-metadata.js')
    if ($LASTEXITCODE -ne 0) { throw 'Metadata synchronization failed' }
}

$arguments = @('--source', (Join-Path $siteRoot 'content'), '--destination', $destinationRoot, '--baseURL', $BaseURL, '--gc', '--minify', '--panicOnWarning', '--noBuildLock', '--cleanDestinationDir')
if ($IncludeDrafts) { $arguments += '--buildDrafts' }
& hugo @arguments
if ($LASTEXITCODE -ne 0) { throw 'Hugo build failed' }
