# Description

In-memory queue limit for the background reader used to prompt object reads and read repair. Additional work spills into the separately bounded overflow queue.

# Datatype

Integer

# Units

- references

# Constraints

- Expected to be a positive integer.

# Inferred default

`100000`.

# Tags

feature: read-repair
repository: riak_kv
module: riak_kv_reader
concept: queueing, replica-repair

# Notes

This is the Erlang application environment key `reader_queue_limit` in `riak_kv`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_kv/src/riak_kv_reader.erl](https://github.com/OpenRiak/riak_kv/blob/48285d5d7aa72c4167e338b3d28ae9ba434cfcb7/src/riak_kv_reader.erl#L116)

# Reviewed against

3.4.0: d1f90b65693ed8497738aaf5fd0219b528bbb760bbe264c749347490b1c19cb2
3.4.1: f6e6ff2cffbe7a5efd4a220676179a6b9d6c205d7b8843dd3118add095a21b27
