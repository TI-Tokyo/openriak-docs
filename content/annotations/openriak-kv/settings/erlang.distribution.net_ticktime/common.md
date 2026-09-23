# Description

Distributed Erlang heartbeat interval used to detect unresponsive peer nodes. Coordinate this across the cluster: a larger value tolerates longer communication stalls but delays node-failure detection.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: runtime, scheduling

# Reviewed against

3.4.0: 24d91ab3b012a79166c2254289d47ead6b38a48e10e9ff854b370c749c8b993c
3.4.1: 24d91ab3b012a79166c2254289d47ead6b38a48e10e9ff854b370c749c8b993c
