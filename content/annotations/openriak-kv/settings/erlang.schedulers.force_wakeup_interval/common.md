# Description

Interval in milliseconds for scanning run queues and waking sleeping schedulers with pending work. Zero disables forced wakeups. This is a workaround for native code that prevents normal scheduling progress.

# Tags

feature: erlang-runtime
repository: cuttlefish, riak
module: erlang_vm.schema, riak.schema
concept: concurrency, runtime, scheduling

# Reviewed against

3.4.0: c1d81af9b54806e927c6b124bd9606dfa7192ee71a6794de40e8354b74e10bf7
3.4.1: c1d81af9b54806e927c6b124bd9606dfa7192ee71a6794de40e8354b74e10bf7
