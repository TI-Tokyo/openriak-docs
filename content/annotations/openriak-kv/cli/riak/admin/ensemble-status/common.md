# Metadata

command: shell:riak admin ensemble-status
versions: 3.4.0, 3.4.1

# Summary

Inspect the strong-consistency ensemble subsystem.

# Description

Without an ensemble selector, show the consensus-system summary. `root` selects the root ensemble. A cluster that has not enabled strong consistency reports the subsystem as disabled.

# Arguments

## ensemble

datatype: ensemble selector
required: false
repeatable: false

### Description

Select a particular ensemble, for example `root`. Omit to show the overall consensus-system summary.

# Reviewed against

3.4.0: aa8da6035a6fbdda5be5d2877674db331bf9b1602689c4a10454db44ac48a172
3.4.1: aa8da6035a6fbdda5be5d2877674db331bf9b1602689c4a10454db44ac48a172

# Tags

feature: observability
repository: riak_kv
module: riak_kv_console
concept: diagnostics
