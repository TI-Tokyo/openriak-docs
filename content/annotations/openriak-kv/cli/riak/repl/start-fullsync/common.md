# Metadata

command: shell:riak repl start-fullsync
versions: 3.4.0, 3.4.1

# Summary

Start fullsync for legacy replication.

# Deprecation

This operation belongs to the legacy replication protocol. There is no direct replacement within that protocol. Migrate to named-cluster replication using [`riak repl connect`](../connect/) and review [`riak repl fullsync start`](../fullsync/start/) and [`riak repl fullsync stop`](../fullsync/stop/) for full-sync control.

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

3.4.0: c07d96a638a8b051995a209c11e82eed76458bb24c7b2a42aec669a55e9ce0db
3.4.1: c07d96a638a8b051995a209c11e82eed76458bb24c7b2a42aec669a55e9ce0db

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
