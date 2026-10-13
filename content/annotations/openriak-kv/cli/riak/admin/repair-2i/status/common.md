# Metadata

command: shell:riak admin repair-2i status
versions: 3.4.0, 3.4.1

# Summary

Inspect secondary-index repair progress.

# Description

Secondary-index repair is a backend maintenance operation. Read status before starting or cancelling work.

# Arguments

# Options

## --speed

omit: true

# Results

## reference-result-1

### Description

The start command launches maintenance work; status reports its progress and kill requests cancellation.

# Examples

## shell-riak-admin-repair-2i-status:inspect-repair-state

### Description

Inspect the repair state. When no repair is running, expect a not-running status.

# Reviewed against

3.4.0: 2a0db930b60b5e31903fb806469ff54b75d0a5c5913b9d745e2a9954cb4b2c7b
3.4.1: 2a0db930b60b5e31903fb806469ff54b75d0a5c5913b9d745e2a9954cb4b2c7b

# Tags

feature: observability
repository: riak_kv
module: riak_kv_console
concept: diagnostics
