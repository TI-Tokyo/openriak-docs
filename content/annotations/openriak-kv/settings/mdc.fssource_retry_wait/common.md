# Description

Minimum delay before retrying a partition that encounters a soft full-sync failure. Used with the soft-retry limit to avoid exhausting retries while a remote AAE tree or other temporary prerequisite is unavailable.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator
concept: cross-cluster-replication, scheduling

# Reviewed against

3.4.0: 9f74d2a28ee79f8bf4208dd42e626c1544697c9558306c841c9cb8354f2d8560
3.4.1: 9f74d2a28ee79f8bf4208dd42e626c1544697c9558306c841c9cb8354f2d8560
