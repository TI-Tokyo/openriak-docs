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
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Node.js is required to generate version mounts' }
if (-not $BaseURL.EndsWith('/')) { $BaseURL += '/' }

$destinationRoot = if ([IO.Path]::IsPathRooted($Destination)) { $Destination } else { Join-Path $siteRoot $Destination }
$coreDestination = Join-Path $siteRoot 'build/core'
$archiveDestination = Join-Path $siteRoot 'build/archives'
$generatedConfig = Join-Path $siteRoot 'tools/generated/hugo.yaml'

& node (Join-Path $PSScriptRoot 'generate-version-mounts.js') --base-config (Join-Path $siteRoot 'content/hugo.yaml') --output $generatedConfig
if ($LASTEXITCODE -ne 0) { throw 'Version mount generation failed' }
& node (Join-Path $PSScriptRoot 'sync-product-metadata.js')
if ($LASTEXITCODE -ne 0) { throw 'Metadata synchronization failed' }

function Invoke-HugoBuild([string] $Config, [string] $Output) {
    $arguments = @('--source', (Join-Path $siteRoot 'content'), '--config', $Config, '--destination', $Output, '--baseURL', $BaseURL, '--gc', '--minify', '--panicOnWarning', '--noBuildLock', '--cleanDestinationDir')
    if ($IncludeDrafts) { $arguments += '--buildDrafts' }
    & hugo @arguments
    if ($LASTEXITCODE -ne 0) { throw "Hugo build failed for $Config" }
}

Invoke-HugoBuild $generatedConfig $coreDestination
Invoke-HugoBuild (Join-Path $siteRoot 'content/hugo-archives.yaml') $archiveDestination

$archiveFiles = @(Get-ChildItem -LiteralPath $archiveDestination -Recurse -File)
foreach ($file in $archiveFiles) {
    $relative = [IO.Path]::GetRelativePath($archiveDestination, $file.FullName)
    if ($relative -notmatch '^(archived-technical-blog|archived-mailing-list)[\\/]') {
        throw "Archive build produced an unexpected path: $relative"
    }
    if (Test-Path -LiteralPath (Join-Path $coreDestination $relative)) {
        throw "Core and archive builds both own: $relative"
    }
}

if (Test-Path -LiteralPath $destinationRoot) { Remove-Item -LiteralPath $destinationRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null
Copy-Item -Path (Join-Path $coreDestination '*') -Destination $destinationRoot -Recurse -Force
Copy-Item -Path (Join-Path $archiveDestination '*') -Destination $destinationRoot -Recurse -Force
Write-Host "Assembled the complete static site in $destinationRoot"
