# Description

Realtime queue process mailbox length at or below which an overloaded queue resumes accepting objects. This lower recovery watermark prevents rapid switching around the overload threshold.

# Datatype

Integer

# Units

- messages

# Constraints

- Positive integer recovery watermark, normally lower than `rtq_overload_threshold`.

# Inferred default

`1000`.

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl2_rtq
concept: queueing, overload-protection

# Notes

This is the Erlang application environment key `rtq_overload_recover` in `riak_repl`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [riak_repl/src/riak_repl2_rtq.erl](https://github.com/OpenRiak/riak_repl/blob/774519154717081ea7d1d09ec36c3dfbf95eb760/src/riak_repl2_rtq.erl#L101)

# Reviewed against

3.4.0: d10bbd8aaa67915b6c98eef3953541273caeb52d5096c1062b24bdcfadb86aaa
3.4.1: d10bbd8aaa67915b6c98eef3953541273caeb52d5096c1062b24bdcfadb86aaa
