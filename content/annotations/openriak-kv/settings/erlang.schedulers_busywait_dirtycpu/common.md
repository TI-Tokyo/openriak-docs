# Description

Busy-wait threshold for dirty CPU schedulers. These run CPU-bound dirty native work; lowering the threshold reduces time spent spinning when that work queue is empty.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime, scheduling

# Reviewed against

3.4.0: e405851fd97abe7cc7ef042385c79f679d4317672c8262cc17110f10ee5d3e26
3.4.1: e405851fd97abe7cc7ef042385c79f679d4317672c8262cc17110f10ee5d3e26
