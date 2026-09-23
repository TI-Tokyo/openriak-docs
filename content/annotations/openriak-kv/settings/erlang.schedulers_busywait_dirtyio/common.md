# Description

Busy-wait threshold for dirty I/O schedulers. Lower values let idle threads sleep sooner, reducing CPU overhead between native I/O tasks.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime, scheduling

# Reviewed against

3.4.0: 68c898e0e907af5f68adabf4b8d83cfb49fccc9f45f60347b02b17b062e13113
3.4.1: 68c898e0e907af5f68adabf4b8d83cfb49fccc9f45f60347b02b17b062e13113
