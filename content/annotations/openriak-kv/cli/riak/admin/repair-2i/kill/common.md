# Metadata

command: shell:riak admin repair-2i kill
versions: 3.4.0, 3.4.1

# Summary

Stop a running secondary-index repair.

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

## shell-riak-admin-repair-2i-kill:inspect-repair-state

### Description

Inspect the result of cancelling an inactive repair. When no repair is running, expect a not-running status.

# Reviewed against

3.4.0: e66e8f7f45df6e602ac9ece64713df8350e612104ad47176f26227c9321f9179
3.4.1: e66e8f7f45df6e602ac9ece64713df8350e612104ad47176f26227c9321f9179

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_console
concept: replica-repair
