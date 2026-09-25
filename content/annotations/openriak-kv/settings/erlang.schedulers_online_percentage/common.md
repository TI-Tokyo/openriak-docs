# Description

Percentage-based sizing of normal schedulers and their online count relative to available processors. Use workload measurements when overriding it, especially on hosts sharing CPU with other services.

# Constraints

- Use two integer percentages separated by a colon, such as `100:75`. Each percentage must be from 1 through 100 inclusive.

# Notes

The schema checks each percentage independently. Although its error message mentions an ordering between the two percentages, the validator does not enforce that ordering. The value 1 is accepted.

# Tags

feature: erlang-runtime
repository: riak
module: riak.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: c96b5118145b7834ee3e3f70dd9c588ec383580f10bd552bd9ac905b78501d5f
3.4.1: c96b5118145b7834ee3e3f70dd9c588ec383580f10bd552bd9ac905b78501d5f
