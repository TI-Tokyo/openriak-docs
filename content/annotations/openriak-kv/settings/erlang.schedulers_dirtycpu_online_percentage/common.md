# Description

Percentage used to size online dirty CPU schedulers. Keep it consistent with the normal scheduler percentage and tune using workload measurements; dirty CPU demand depends on the native functions in use.

# Constraints

- Use two integer percentages separated by a colon, such as `50:25`. Each percentage must be from 1 through 100 inclusive.

# Notes

The schema checks each percentage independently. Although its error message mentions an ordering between the two percentages, the validator does not enforce that ordering. The value 1 is accepted.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: 54f1674cec83b10438ee79c9d71b55c91b30dfcf512b18aa8c7725c2376e1ec8
3.4.1: 54f1674cec83b10438ee79c9d71b55c91b30dfcf512b18aa8c7725c2376e1ec8
