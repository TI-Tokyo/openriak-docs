# Metadata

command: shell:riak repl cancel-fullsync
versions: 3.4.0, 3.4.1

# Summary

Cancel fullsync for legacy replication.

# Description

This is a deprecated replication-v2 control. For current named-cluster full-sync, use the repl fullsync subcommands.

# Arguments

# Results

## outcome

### Description

When a legacy replication listener exists, this requests its full-sync cancel operation. The disposable node has no legacy listener, so the tested call raises an RPC error; it does not establish that a remote transfer changed state.

# Examples

## shell-riak-repl-cancel-fullsync:legacy-control

### Description

Request cancel for the configured legacy listener. With no connected legacy replication clients, an acknowledgement confirms the control request; it does not indicate that any objects have been transferred.

# Reviewed against

3.4.0: 2a54b26ad11c0f4a69e6b5d089b8643b48e65db17b2772f89caa49b67c1af637
3.4.1: 2a54b26ad11c0f4a69e6b5d089b8643b48e65db17b2772f89caa49b67c1af637

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
