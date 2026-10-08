# Metadata

command: shell:riak repl del-site
versions: 3.4.0, 3.4.1

# Summary

Remove a legacy replication site.

# Deprecation

This operation belongs to the legacy replication protocol. There is no direct replacement within that protocol. Migrate to named-cluster replication using [`riak repl connect`](../connect/) and review [`riak repl fullsync start`](../fullsync/start/) and [`riak repl fullsync stop`](../fullsync/stop/) for full-sync control.

# Description

This configures the deprecated replication protocol. Use named-cluster connections for current replication deployments.

# Arguments

## sitename

datatype: site name
required: true
repeatable: false

### Description

Legacy site label, for example `cli_site`.

# Reviewed against

3.4.0: 1ef07b5dd86d6f47487694fc418b4bd7cb1d37a8be4ad94750800512951cf844
3.4.1: 1ef07b5dd86d6f47487694fc418b4bd7cb1d37a8be4ad94750800512951cf844

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
