param(
    [ValidateSet('development', 'beta-test', 'release')]
    [string] $Profile = 'release',
    [bool] $IncludeDrafts = $true,
    [string] $Destination = 'public',
    [string] $BaseURL = 'https://www.openriak.org/docs/',
    [string] $RiakKVVersion = '3.2.5'
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
$coreDestination = Join-Path $siteRoot "build/core-$Profile"
$archiveDestination = Join-Path $siteRoot 'build/archives'
$generatedConfig = if ($Profile -eq 'development') {
    Join-Path $siteRoot 'build/generated-development/hugo.yaml'
} else {
    Join-Path $siteRoot 'tools/generated/hugo.yaml'
}
$developmentDataRoot = Join-Path $siteRoot 'build/generated-development'

$mountArguments = @('--base-config', (Join-Path $siteRoot 'content/hugo.yaml'), '--output', $generatedConfig)
if ($Profile -eq 'development') {
    $mountArguments += @(
        '--version-data-root', "openriak-kv=$((Join-Path $developmentDataRoot 'openriak-kv/data/versions'))",
        '--version-data-root', "openriak-cs=$((Join-Path $developmentDataRoot 'openriak-cs/data/versions'))",
        '--version-data-root', "openriak-ts=$((Join-Path $developmentDataRoot 'openriak-ts/data/versions'))",
        '--include-version', "riak-kv=$RiakKVVersion",
        '--include-latest', 'riak-cs',
        '--include-latest', 'riak-ts'
    )
}
& node (Join-Path $PSScriptRoot 'generate-version-mounts.js') @mountArguments
if ($LASTEXITCODE -ne 0) { throw 'Version mount generation failed' }
$metadataArguments = @()
if ($Profile -eq 'development') {
    $metadataArguments += @(
        '--output-root', $developmentDataRoot,
        '--include-version', "riak-kv=$RiakKVVersion",
        '--include-latest', 'riak-cs',
        '--include-latest', 'riak-ts'
    )
}
& node (Join-Path $PSScriptRoot 'sync-product-metadata.js') @metadataArguments
if ($LASTEXITCODE -ne 0) { throw 'Metadata synchronization failed' }

function Invoke-HugoBuild([string] $Config, [string] $Output) {
    $arguments = @('--source', (Join-Path $siteRoot 'content'), '--config', $Config, '--destination', $Output, '--baseURL', $BaseURL, '--gc', '--minify', '--panicOnWarning', '--noBuildLock', '--cleanDestinationDir')
    if ($IncludeDrafts) { $arguments += '--buildDrafts' }
    & hugo @arguments
    if ($LASTEXITCODE -ne 0) { throw "Hugo build failed for $Config" }
}

Invoke-HugoBuild $generatedConfig $coreDestination
if ($Profile -eq 'release') {
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
}

if (Test-Path -LiteralPath $destinationRoot) { Remove-Item -LiteralPath $destinationRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null
Copy-Item -Path (Join-Path $coreDestination '*') -Destination $destinationRoot -Recurse -Force
if ($Profile -eq 'release') {
    Copy-Item -Path (Join-Path $archiveDestination '*') -Destination $destinationRoot -Recurse -Force
}
Write-Host "Built the $Profile static site in $destinationRoot"
