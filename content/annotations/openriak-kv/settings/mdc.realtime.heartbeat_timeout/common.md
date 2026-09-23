# Description

How long the legacy replication source waits for a heartbeat response before closing and re-establishing the connection. A short timeout detects stalls quickly but is more sensitive to transient delays.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtsource_conn
concept: cross-cluster-replication, scheduling

# Reviewed against

3.4.0: ecaf9cedf06ced6b36ded25984dff9255e7c66d5304699d5042518005bf303a5
3.4.1: ecaf9cedf06ced6b36ded25984dff9255e7c66d5304699d5042518005bf303a5
