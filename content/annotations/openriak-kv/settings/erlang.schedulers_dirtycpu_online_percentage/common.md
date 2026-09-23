# Description

Percentage used to size online dirty CPU schedulers. Keep it consistent with the normal scheduler percentage and tune using workload measurements; dirty CPU demand depends on the native functions in use.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: 54f1674cec83b10438ee79c9d71b55c91b30dfcf512b18aa8c7725c2376e1ec8
3.4.1: 54f1674cec83b10438ee79c9d71b55c91b30dfcf512b18aa8c7725c2376e1ec8
