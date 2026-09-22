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

3.4.0: 8546c2ad2a9c2b437d541fba4a20b9ce9b6a52ecdca5030a77e0fff9c926c9a1
3.4.1: 8546c2ad2a9c2b437d541fba4a20b9ce9b6a52ecdca5030a77e0fff9c926c9a1
