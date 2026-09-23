# Metadata

command: shell:riak repl start-fullsync
versions: 3.4.0, 3.4.1

# Summary

Start fullsync for legacy replication.

# Description

This is a deprecated replication-v2 control. For current named-cluster full-sync, use the repl fullsync subcommands.

# Arguments

# Results

## outcome

### Description

When a legacy replication listener exists, this requests its full-sync start operation. The disposable node has no legacy listener, so the tested call raises an RPC error; it does not establish that a remote transfer started.

# Examples

## shell-riak-repl-start-fullsync:legacy-control

### Description

Request start for the configured legacy listener. With no connected legacy replication clients, an acknowledgement confirms the control request; it does not indicate that any objects have been transferred.

# Reviewed against

3.4.0: ce6684d5e4238ac94738900c7633ac22c0ba4c9beb902835fe6d9937174dc192
3.4.1: ce6684d5e4238ac94738900c7633ac22c0ba4c9beb902835fe6d9937174dc192

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
