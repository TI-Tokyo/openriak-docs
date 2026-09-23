# Metadata

command: shell:riak repl resume-fullsync
versions: 3.4.0, 3.4.1

# Summary

Resume fullsync for legacy replication.

# Description

This is a deprecated replication-v2 control. For current named-cluster full-sync, use the repl fullsync subcommands.

# Arguments

# Results

## outcome

### Description

When a legacy replication listener exists, this requests its full-sync resume operation. The disposable node has no legacy listener, so the tested call raises an RPC error; it does not establish that a remote transfer changed state.

# Examples

## shell-riak-repl-resume-fullsync:legacy-control

### Description

Request resume for the configured legacy listener. With no connected legacy replication clients, an acknowledgement confirms the control request; it does not indicate that any objects have been transferred.

# Reviewed against

3.4.0: 1d84abfe7e3ec958305aa6e0f98c23ccefe4d970eed575a8e5ebd8c720a52f15
3.4.1: 1d84abfe7e3ec958305aa6e0f98c23ccefe4d970eed575a8e5ebd8c720a52f15

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
