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

$generatedConfig = Join-Path $siteRoot 'tools/generated/hugo.yaml'
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Node.js is required to generate version mounts' }
& node (Join-Path $PSScriptRoot 'generate-version-mounts.js') --output $generatedConfig
if ($LASTEXITCODE -ne 0) { throw 'Version mount generation failed' }
& node (Join-Path $PSScriptRoot 'sync-product-metadata.js')
if ($LASTEXITCODE -ne 0) { throw 'Metadata synchronization failed' }

$arguments = @('--source', (Join-Path $siteRoot 'content'), '--config', $generatedConfig, '--destination', $destinationRoot, '--baseURL', $BaseURL, '--gc', '--minify', '--panicOnWarning', '--noBuildLock', '--cleanDestinationDir')
if ($IncludeDrafts) { $arguments += '--buildDrafts' }
& hugo @arguments
if ($LASTEXITCODE -ne 0) { throw 'Hugo build failed' }
