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

3.4.0: be06d91c05a938b64160a8fdec3cf7357d6c1671f0690cc2773c2b2239684cc9
3.4.1: be06d91c05a938b64160a8fdec3cf7357d6c1671f0690cc2773c2b2239684cc9

# Tags

feature: observability
repository: riak_kv
module: riak_kv_console
concept: diagnostics
