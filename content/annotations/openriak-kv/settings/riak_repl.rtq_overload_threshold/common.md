# Description

Realtime queue process mailbox length above which the queue marks itself overloaded and new objects are dropped. This counts pending Erlang messages, rather than the bytes stored in the replication queue.

# Datatype

Integer

# Units

- messages

# Constraints

- Positive integer overload watermark, normally greater than `rtq_overload_recover`.

# Inferred default

`2000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtq
concept: queueing, overload-protection

# Notes

This is the Erlang application environment key `rtq_overload_threshold` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtq.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtq.erl#L100)

# Reviewed against

3.4.0: 84aa3e197e75710349f60fed6142a2186594af3425d909dcf62fdbf40a347519
3.4.1: 84aa3e197e75710349f60fed6142a2186594af3425d909dcf62fdbf40a347519
