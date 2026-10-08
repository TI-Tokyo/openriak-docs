# Metadata

command: shell:riak repl pause-fullsync
versions: 3.4.0, 3.4.1

# Summary

Pause fullsync for legacy replication.

# Description

This is a deprecated replication-v2 control. For current named-cluster full-sync, use the repl fullsync subcommands.

# Arguments

# Results

## outcome

### Description

When a legacy replication listener exists, this requests its full-sync pause operation. The disposable node has no legacy listener, so the tested call raises an RPC error; it does not establish that a remote transfer changed state.

# Examples

## shell-riak-repl-pause-fullsync:legacy-control

### Description

Request pause for the configured legacy listener. With no connected legacy replication clients, an acknowledgement confirms the control request; it does not indicate that any objects have been transferred.

# Reviewed against

3.4.0: 35b466b440f10c735beef046eafd07f0529e6af249e4c36d1ca3177c64377885
3.4.1: 35b466b440f10c735beef046eafd07f0529e6af249e4c36d1ca3177c64377885

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
