# Metadata

command: shell:riak admin search
versions: 3.4.0, 3.4.1

# Summary

Inspect the unavailable legacy search command.

# Description

The discovered entry is not an available search-management API in these releases. Do not use it to configure a search index.

# Arguments

# Examples

## reference-example-1

title: Check available administration commands

### Invocation

```sh
riak admin
```

### Description

Use the current administration command list instead of relying on this legacy entry.

### Expected output

Usage listing the supported command groups.

# Errors

## reference-error-1

### Condition

The legacy search entry is invoked.

### Description

The launcher cannot execute a supported search operation.

### Remedy

Use only search functionality explicitly supported by the selected release.

# Results

## reference-result-1

### Description

No supported search operation is available through this entry.

# Reviewed against

3.4.0: 8ca4a38a746d4851887f99494a9e38fde81b9b6c48d8d1846aa4937bfec71224
3.4.1: 8ca4a38a746d4851887f99494a9e38fde81b9b6c48d8d1846aa4937bfec71224
