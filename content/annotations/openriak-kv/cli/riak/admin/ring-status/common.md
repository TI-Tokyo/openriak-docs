# Metadata

command: shell:riak admin ring-status
versions: 3.4.0, 3.4.1

# Summary

Inspect the claimant, ring readiness and pending ownership changes.

# Description

Use the claimant and pending-change details to diagnose a stalled membership change. Ownership transfer is asynchronous.

# Arguments

# Reviewed against

3.4.0: f597420ba2cb31cac7a474416c3fd6d0f790259a44bf7a01c27c742956451e1f
3.4.1: f597420ba2cb31cac7a474416c3fd6d0f790259a44bf7a01c27c742956451e1f

# Tags

feature: observability
repository: riak_core
module: riak_core_console
concept: diagnostics
