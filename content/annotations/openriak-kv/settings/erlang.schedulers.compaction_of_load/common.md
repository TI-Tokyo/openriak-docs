# Description

Concentrate runnable work onto fewer scheduler threads when load is low. Disabling load compaction changes balancing behaviour rather than reducing the configured scheduler count.

# Tags

feature: erlang-runtime
repository: cuttlefish, riak
module: erlang_vm.schema, riak.schema
concept: compaction, concurrency, runtime

# Reviewed against

3.4.0: 0483c4c30b28bb7b9ac73c750096c00275d6e2ee1e66967b19b468e9f6723f85
3.4.1: 0483c4c30b28bb7b9ac73c750096c00275d6e2ee1e66967b19b468e9f6723f85
