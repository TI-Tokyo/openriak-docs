param(
    [string] $BuildDirectory = 'public',
    [string] $ReportPath = '',
    [string] $BasePath = '/docs/'
)

$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$buildRoot = if ([IO.Path]::IsPathRooted($BuildDirectory)) {
    [IO.Path]::GetFullPath($BuildDirectory)
} else {
    [IO.Path]::GetFullPath((Join-Path $siteRoot $BuildDirectory))
}

if (-not (Test-Path -LiteralPath $buildRoot -PathType Container)) {
    throw "Build directory does not exist: $buildRoot"
}

$missing = [System.Collections.Generic.List[object]]::new()
$checked = 0
$attributePattern = [regex]::new('(?:href|src)\s*=\s*(?:"([^"]+)"|''([^'']+)''|([^\s>]+))', [Text.RegularExpressions.RegexOptions]'IgnoreCase, Compiled')
$published = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$seenAbsoluteUrls = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$seenCandidates = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($file in Get-ChildItem -LiteralPath $buildRoot -Recurse -File) {
    [void] $published.Add([IO.Path]::GetFullPath($file.FullName))
}

foreach ($htmlFile in Get-ChildItem -LiteralPath $buildRoot -Recurse -File -Filter '*.html') {
    $html = [IO.File]::ReadAllText($htmlFile.FullName)
    # Literal HTML and configuration examples can contain href= or src= text.
    # They are escaped inside code blocks and are not navigable document links.
    $htmlToValidate = [regex]::Replace(
        $html,
        '(?is)<pre\b.*?</pre>|<code\b.*?</code>',
        ''
    )
    foreach ($match in $attributePattern.Matches($htmlToValidate)) {
        $url = if ($match.Groups[1].Success) { $match.Groups[1].Value } elseif ($match.Groups[2].Success) { $match.Groups[2].Value } else { $match.Groups[3].Value }
        if ($url -match '^(?:[a-z][a-z0-9+.-]*:|//|#)') { continue }

        $path = ($url -split '[?#]', 2)[0]
        if (-not $path) { continue }
        if ($path.StartsWith('/') -and -not $seenAbsoluteUrls.Add($path)) { continue }
        $siteRelativePath = $path
        if ($path.StartsWith('/') -and $BasePath) {
            $normalizedBasePath = '/' + $BasePath.Trim('/') + '/'
            if ($path.StartsWith($normalizedBasePath, [StringComparison]::OrdinalIgnoreCase)) {
                $siteRelativePath = '/' + $path.Substring($normalizedBasePath.Length)
            }
        }
        $decoded = [Uri]::UnescapeDataString($siteRelativePath).Replace('/', [IO.Path]::DirectorySeparatorChar)
        if ($path.StartsWith('/')) {
            $candidate = Join-Path $buildRoot $decoded.TrimStart([char[]]@('/', '\'))
        } else {
            $candidate = Join-Path $htmlFile.DirectoryName $decoded
        }

        if ($path.EndsWith('/')) {
            $candidate = Join-Path $candidate 'index.html'
        } elseif (-not [IO.Path]::GetExtension($candidate)) {
            $directoryIndex = Join-Path $candidate 'index.html'
            if ($published.Contains([IO.Path]::GetFullPath($directoryIndex))) { $candidate = $directoryIndex }
        }

        $candidate = [IO.Path]::GetFullPath($candidate)
        if (-not $seenCandidates.Add($candidate)) { continue }
        $checked++
        if (-not $published.Contains($candidate)) {
            $missing.Add([pscustomobject]@{
                Source = [IO.Path]::GetRelativePath($buildRoot, $htmlFile.FullName)
                URL = $url
            })
        }
    }
}

if ($missing.Count) {
    $uniqueMissing = @($missing | Sort-Object Source, URL -Unique)
    if ($ReportPath) {
        $report = [pscustomobject]@{
            generated_at = [DateTimeOffset]::Now.ToString('o')
            build_directory = $buildRoot
            checked_targets = $checked
            unresolved_count = $uniqueMissing.Count
            unresolved = $uniqueMissing
        }
        [IO.File]::WriteAllText([IO.Path]::GetFullPath($ReportPath), ($report | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    }
    $uniqueMissing | Select-Object -First 25 | Format-Table -AutoSize
    throw "$($uniqueMissing.Count) unresolved local asset or page references were found."
}

Write-Output "Validated $checked local links and assets across the generated HTML."

