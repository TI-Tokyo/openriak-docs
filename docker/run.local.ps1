param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $ComposeArguments
)

$ErrorActionPreference = 'Stop'
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Split-Path -Parent $scriptDirectory
$composeFile = Join-Path $scriptDirectory 'docker-compose.localhost-preview.yaml'
$previewURL = if ($env:HUGO_BASEURL) { $env:HUGO_BASEURL } else { 'http://localhost:1314/docs/' }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker is required but was not found on PATH.'
}

& docker compose version | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Docker Compose v2 is required (the 'docker compose' command)."
}

Write-Host 'Starting OpenRiak docs with Hugo 0.165.0'
Write-Host "HTTP preview: $previewURL"
& docker compose --project-directory $siteRoot -f $composeFile up --remove-orphans @ComposeArguments
exit $LASTEXITCODE
