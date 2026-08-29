param(
    [Parameter(Mandatory = $true)]
    [string] $SourceRoot,
    [string] $DestinationRoot = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$siteRoot = Split-Path -Parent $PSScriptRoot
if (-not $DestinationRoot) {
    $DestinationRoot = Join-Path $siteRoot 'content\kv\3.2.5'
}

$SourceRoot = [IO.Path]::GetFullPath($SourceRoot)
$DestinationRoot = [IO.Path]::GetFullPath($DestinationRoot)

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw "Source directory does not exist: $SourceRoot"
}
if (Test-Path -LiteralPath $DestinationRoot) {
    throw "Destination already exists; refusing to overwrite it: $DestinationRoot"
}

$referencePath = Join-Path $SourceRoot '_reference-links.md'
$landingPath = Join-Path $SourceRoot 'index.md'
if (-not (Test-Path -LiteralPath $referencePath -PathType Leaf)) {
    throw "Shared reference-link file does not exist: $referencePath"
}
if (-not (Test-Path -LiteralPath $landingPath -PathType Leaf)) {
    throw "Version landing page does not exist: $landingPath"
}

function Convert-LegacyLinks {
    param([string] $Text)

    $result = [regex]::Replace(
        $Text,
        '\{\{<\s*baseurl\s*>\}\}riak/kv/3\.2\.5',
        '{{< baseurl >}}kv/3.2.5',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\{\{<\s*baseurl\s*>\}\}riak/kv/latest',
        '{{< baseurl >}}kv/3.2.5',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\{\{<\s*baseurl\s*>\}\}riak/kv/learn',
        '{{< baseurl >}}kv/3.2.5/learn',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\{\{<\s*baseurl\s*>\}\}community(?:/projects|/reporting-bugs|/taishi)?/?',
        'https://github.com/orgs/OpenRiak/discussions',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\{\{<\s*baseurl\s*>\}\}(riak/(?:cs/(?:latest|2\.1\.1)|kv/(?:2\.9\.10|3\.2\.4))[^\s\)\]"''<>]*)',
        'https://www.tiot.jp/riak-docs/$1',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\{\{<\s*baseurl\s*>\}\}',
        '{{< baseurl >}}',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = $result.Replace('./get-started-with-rra/', './using-rra/')
    $result = $result.Replace(
        '../../using/tictac-aae-fold/',
        '../../using/cluster-operations/tictac-aae-fold/'
    )
    $result = $result.Replace(
        '../../using/admin/riak admin',
        '../../using/admin/riak-admin'
    )
    $result = $result.Replace(
        '&#123;&#123;<baseurl>&#125;&#125;riak/kv/3.2.5',
        '{{< baseurl >}}kv/3.2.5'
    )
    $result = $result.Replace(
        '{{< baseurl >}}kv/3.2.5/configuring/planning/v3-multi-datacenter',
        '{{< baseurl >}}kv/3.2.5/configuring/v3-multi-datacenter'
    )
    $result = $result.Replace(
        '[causal context][[concept causal context]]',
        '[causal context][concept causal context]'
    )
    $result = $result.Replace(
        '[reconfigure][redis add-on setup]',
        '[reconfigure][addon redis setup]'
    )
    $result = $result.Replace(
        '[`riak admin ensemble-status`][admin riak admin#ensemble]',
        '[`riak admin ensemble-status`][use admin riak admin#ensemble]'
    )
    $result = $result.Replace(
        '[tombstones][cluster ops obj deletion]',
        '[tombstones][cluster ops obj del]'
    )
    $result = $result.Replace(
        '[status output][cluster ops v2 mdc#status]',
        '[status output]({{< baseurl >}}kv/3.2.5/using/cluster-operations/v2-multi-datacenter/#status)'
    )
    $result = $result.Replace(
        '[search indexes][usage search]',
        '[search indexes]({{< baseurl >}}kv/3.2.5/deprecated/riak-search/)'
    )
    $result = [regex]::Replace(
        $result,
        '\{\{< baseurl >\}\}kv/3\.2\.5/(?:developing/api/http/(?:delete-search-index|fetch-search-index|fetch-search-schema|search-index-info|search-query|store-search-index|store-search-schema)|developing/api/protocol-buffers/search|developing/usage/(?:search|search-schemas|searching-data-types|custom-extractors|document-store)|using/reference/search)/?',
        '{{< baseurl >}}kv/3.2.5/deprecated/riak-search/',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    $result = [regex]::Replace(
        $result,
        '\(\./(?:search|search-schemas|searching-data-types|custom-extractors|document-store)/?\)',
        '({{< baseurl >}}kv/3.2.5/deprecated/riak-search/)',
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    return $result
}

$globalDefinitions = [ordered]@{}
$globalText = Convert-LegacyLinks ([IO.File]::ReadAllText($referencePath))
foreach ($match in [regex]::Matches($globalText, '(?m)^\[([^\]\r\n]+)\]:\s*(.+)$')) {
    $label = $match.Groups[1].Value.Trim().ToLowerInvariant()
    if (-not $globalDefinitions.Contains($label)) {
        $globalDefinitions[$label] = $match.Value
    }
}

function Add-SharedReferenceDefinitions {
    param([string] $Text)

    $localDefinitions = [System.Collections.Generic.HashSet[string]]::new(
        [StringComparer]::OrdinalIgnoreCase
    )
    foreach ($match in [regex]::Matches($Text, '(?m)^\[([^\]\r\n]+)\]:')) {
        [void] $localDefinitions.Add($match.Groups[1].Value.Trim())
    }

    $neededLabels = [System.Collections.Generic.HashSet[string]]::new(
        [StringComparer]::OrdinalIgnoreCase
    )
    foreach ($match in [regex]::Matches($Text, '(?<!\!)\[([^\]\r\n]+)\]\[([^\]\r\n]*)\]')) {
        $label = if ($match.Groups[2].Value) {
            $match.Groups[2].Value.Trim()
        } else {
            $match.Groups[1].Value.Trim()
        }
        [void] $neededLabels.Add($label)
    }
    foreach ($match in [regex]::Matches($Text, '(?<!\!)\[([^\]\r\n]+)\](?![\(\[:])')) {
        [void] $neededLabels.Add($match.Groups[1].Value.Trim())
    }

    $required = [System.Collections.Generic.List[string]]::new()
    foreach ($label in $neededLabels) {
        $normalizedLabel = $label.ToLowerInvariant()
        if (
            -not $localDefinitions.Contains($label) -and
            $globalDefinitions.Contains($normalizedLabel)
        ) {
            $required.Add([string] $globalDefinitions[$normalizedLabel])
        }
    }

    if ($required.Count -eq 0) {
        return $Text
    }

    return $Text.TrimEnd() + "`n`n" + ($required -join "`n") + "`n"
}

function Write-MigratedFile {
    param(
        [string] $RelativePath,
        [string] $Text
    )

    $targetPath = Join-Path $DestinationRoot $RelativePath
    $targetDirectory = Split-Path -Parent $targetPath
    [void] (New-Item -ItemType Directory -Force -Path $targetDirectory)
    $converted = Add-SharedReferenceDefinitions (Convert-LegacyLinks $Text)
    $frontMatter = [regex]::Match($converted, '(?s)\A---\r?\n(.*?)\r?\n---')
    if (
        $frontMatter.Success -and
        $frontMatter.Groups[1].Value -notmatch '(?m)^weight:\s*' -and
        $frontMatter.Groups[1].Value -match '(?m)^    weight:\s*(\d+)\s*$'
    ) {
        $legacyMenuWeight = $Matches[1]
        $frontMatterStart = [regex]::new('\A---\r?\n')
        $converted = $frontMatterStart.Replace(
            $converted,
            {
                param($match)
                return $match.Value + "weight: $legacyMenuWeight`n"
            },
            1
        )
    }
    if ([IO.Path]::GetFileName($RelativePath) -ne '_index.md' -and $converted -notmatch '(?m)^slug:\s*') {
        $slug = [IO.Path]::GetFileNameWithoutExtension($RelativePath)
        $frontMatterStart = [regex]::new('\A---\r?\n')
        $converted = $frontMatterStart.Replace(
            $converted,
            {
                param($match)
                return $match.Value + "slug: '$slug'`n"
            },
            1
        )
    }
    [IO.File]::WriteAllText($targetPath, $converted, [Text.UTF8Encoding]::new($false))
}

$landing = Convert-LegacyLinks ([IO.File]::ReadAllText($landingPath))
$landing = [regex]::Replace(
    $landing,
    '(?m)^project_version:\s*["'']?3\.2\.5["'']?\s*$',
    {
        param($match)
        return $match.Value + "`nproduct: 'Riak KV'`nproduct_version: '3.2.5'`nstatus: 'historical'`ndraft: false`nweight: 30`nurl: '/kv/3.2.5/'`ncascade:`n  product: 'Riak KV'`n  product_version: '3.2.5'`n  status: 'historical'"
    },
    1
)
$landing = [regex]::Replace(
    $landing,
    '(?s)\A(---\r?\n.*?\r?\n---\r?\n)',
    {
        param($match)
        return $match.Groups[1].Value + "`n> [!NOTE]`n> These historical docs describe Riak KV 3.2.5. Use the documentation version that matches every node in your cluster.`n"
    },
    1
)
Write-MigratedFile -RelativePath '_index.md' -Text $landing

$sourceFiles = Get-ChildItem -LiteralPath $SourceRoot -Recurse -File -Filter '*.md'
$excludedRootFiles = [System.Collections.Generic.HashSet[string]]::new(
    [StringComparer]::OrdinalIgnoreCase
)
foreach ($name in @('_index.md', 'index.md', '_reference-links.md')) {
    [void] $excludedRootFiles.Add($name)
}
$movedSections = 0
$copiedPages = 0

foreach ($sourceFile in $sourceFiles) {
    $relativePath = [IO.Path]::GetRelativePath($SourceRoot, $sourceFile.FullName)
    if (
        -not $relativePath.Contains([IO.Path]::DirectorySeparatorChar) -and
        $excludedRootFiles.Contains($relativePath)
    ) {
        continue
    }

    $withoutExtension = [IO.Path]::ChangeExtension($sourceFile.FullName, $null)
    if (Test-Path -LiteralPath $withoutExtension -PathType Container) {
        $relativeSection = [IO.Path]::GetRelativePath($SourceRoot, $withoutExtension)
        $relativePath = Join-Path $relativeSection '_index.md'
        $movedSections++
    }

    Write-MigratedFile -RelativePath $relativePath -Text ([IO.File]::ReadAllText($sourceFile.FullName))
    $copiedPages++
}

$deprecatedIndex = @'
---
title: 'Deprecated features'
description: 'Historical documentation for features deprecated in Riak KV 3.2.5.'
weight: 900
---

This section preserves documentation for features that were deprecated in Riak KV 3.2.5.
'@
Write-MigratedFile -RelativePath 'deprecated\_index.md' -Text $deprecatedIndex

$freeBsdStub = @'
---
title: 'Install Riak KV 3.2.5 on FreeBSD'
description: 'Describe the historical source-build procedure required to install Riak KV 3.2.5 on FreeBSD.'
weight: 80
draft: true
---

> [!WARNING]
> The source documentation referenced a FreeBSD installation page, but that page was not present in the preserved 3.2.5 source tree.

## Installing from source

Use the [Riak KV 3.2.5 source installation guide]({{< baseurl >}}kv/3.2.5/setup/installing/source/) as the general build procedure.

Before this page is considered complete, verify the supported FreeBSD release, Erlang/OTP version, required packages, GCC configuration, service integration, filesystem paths, and post-installation checks against a working FreeBSD system.
'@
Write-MigratedFile -RelativePath 'setup\installing\freebsd.md' -Text $freeBsdStub

$macOsStub = @'
---
title: 'Install Riak KV 3.2.5 on macOS'
description: 'Describe the historical source-build procedure required to install Riak KV 3.2.5 on macOS.'
weight: 90
draft: true
---

> [!WARNING]
> The source documentation referenced a macOS installation page, but that page was not present in the preserved 3.2.5 source tree.

## Installing from source

Use the [Riak KV 3.2.5 source installation guide]({{< baseurl >}}kv/3.2.5/setup/installing/source/) as the general build procedure.

Before this page is considered complete, verify the supported macOS release, Erlang/OTP version, compiler and package-manager prerequisites, launch-service integration, filesystem paths, and post-installation checks against a working macOS system.
'@
Write-MigratedFile -RelativePath 'setup\installing\mac-osx.md' -Text $macOsStub

$result = [pscustomobject]@{
    source_markdown_files = $sourceFiles.Count
    migrated_content_files = $copiedPages + 4
    section_pages_moved_to_indexes = $movedSections
    generated_section_indexes = 1
    generated_missing_source_stubs = 2
    destination = $DestinationRoot
}
$result | ConvertTo-Json
