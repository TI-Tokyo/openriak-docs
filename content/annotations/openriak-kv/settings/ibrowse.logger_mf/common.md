# Description

Optional `{Module, Function}` callback for ibrowse logging, called with a format string and argument list. It also receives enabled trace output; without it, trace output uses `io:format/2` and ordinary library log messages are ignored.

# Datatype

Tuple

# Constraints

- `{Module, Function}` with atom names; the callback accepts `(Format, Arguments)` (arity 2).

# Inferred default

Unset. Enabled trace output uses `io:format/2`; ordinary library messages have no logger callback.

# Tags

feature: observability
repository: ibrowse
module: ibrowse_lib
concept: diagnostics

# Notes

This is the Erlang application environment key `logger_mf` in `ibrowse`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [ibrowse/src/ibrowse_lib.erl](https://github.com/OpenRiak/ibrowse/blob/3fd17dd33c474800a4d02ad4e5ae9d4db45e0335/src/ibrowse_lib.erl#L405)

# Reviewed against

3.4.0: 9196240b23452d1c9c6a270dff13249372ee212d9b2fc7edd3b9fe91f714f629
3.4.1: 9196240b23452d1c9c6a270dff13249372ee212d9b2fc7edd3b9fe91f714f629
