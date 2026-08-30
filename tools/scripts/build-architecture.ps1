$ErrorActionPreference = 'Stop'
$repositoryRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$image = 'ghcr.io/gohugoio/hugo:v0.165.0'
$validationRoot = Join-Path $repositoryRoot 'public/.architecture-validation'

node (Join-Path $PSScriptRoot 'generate-version-mounts.js')
if ($LASTEXITCODE -ne 0) { throw 'Version mount generation failed' }
node (Join-Path $PSScriptRoot 'sync-product-metadata.js')
if ($LASTEXITCODE -ne 0) { throw 'Metadata synchronization failed' }

Write-Host 'Building unified site...'
docker run --rm --volume "${repositoryRoot}:/workspace" --workdir /workspace/content $image `
    --config /workspace/tools/generated/hugo.yaml `
    --destination /workspace/public/.architecture-validation `
    --baseURL http://localhost:1410/docs/ `
    --cacheDir /tmp/hugo-cache `
    --cleanDestinationDir --gc --minify --panicOnWarning --buildDrafts
if ($LASTEXITCODE -ne 0) { throw 'Unified Hugo build failed' }

function Assert-MissingValueBuildFails {
    param([string]$Name, [string]$Shortcode, [string]$ExpectedOs)

    $fixtureDirectory = Join-Path $validationRoot "missing-value-fixture-$Name"
    New-Item -ItemType Directory -Force -Path $fixtureDirectory | Out-Null
    $fixturePath = Join-Path $fixtureDirectory 'missing-value-test.md'
    $fixtureContent = "---`ntitle: Missing value validation`n---`n`n$Shortcode`n"
    [IO.File]::WriteAllText($fixturePath, $fixtureContent, [Text.UTF8Encoding]::new($false))
    $output = docker run --rm --volume "${repositoryRoot}:/workspace" `
        --volume "${fixtureDirectory}:/workspace/content/openriak-kv/3.4.1:ro" `
        --workdir /workspace/content $image `
        --config /workspace/tools/generated/hugo.yaml `
        --destination "/workspace/public/.architecture-validation/missing-value-output-$Name" `
        --baseURL http://localhost:1410/docs/ `
        --cacheDir /tmp/hugo-cache --cleanDestinationDir --gc --minify --panicOnWarning 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) { throw "Hugo unexpectedly accepted missing value fixture $Name" }
    $expected = "missing value: product=openriak-kv version=3.4.1 os=$ExpectedOs key=banana"
    if (($output -join "`n") -notmatch [regex]::Escape($expected)) {
        throw "Missing value fixture $Name failed without the expected diagnostic: $($output -join ' ')"
    }
}

Assert-MissingValueBuildFails 'default-os' '{{< load-value key="banana" >}}' 'ubuntu-noble-amd64'
Assert-MissingValueBuildFails 'explicit-os' '{{< load-value key="banana" os="alpine-3.21-aarch64" >}}' 'alpine-3.21-aarch64'
Write-Host 'Missing value generation failure tests passed.'

node (Join-Path $PSScriptRoot 'architecture.test.js')
if ($LASTEXITCODE -ne 0) { throw 'Architecture validation failed' }
docker run --rm --volume "${repositoryRoot}:/workspace" --entrypoint /bin/sh $image `
    -c 'rm -rf /workspace/public/.architecture-validation'
if ($LASTEXITCODE -ne 0) { throw 'Architecture validation cleanup failed' }
