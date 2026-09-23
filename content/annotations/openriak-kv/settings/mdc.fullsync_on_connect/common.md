# Description

Start legacy full-sync when a connection to the remote cluster is first established. This helps reconcile existing differences in addition to changes subsequently delivered by real-time replication.

# Tags

feature: full-sync, legacy-replication
repository: riak_repl
module: riak_repl2_fscoordinator, riak_repl_tcp_server
concept: replica-repair

# Reviewed against

3.4.0: 7a930e045f4f7bbb0a68601930e93212de557109e3b50211612abb85cdd0600d
3.4.1: 7a930e045f4f7bbb0a68601930e93212de557109e3b50211612abb85cdd0600d
