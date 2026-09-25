# Description

Maximum number of unread HTTP request-body bytes Webmachine attempts to drain after request processing finishes. If it cannot finish draining within the limit, the connection cannot be safely reused for another request.

# Datatype

Integer

# Units

- bytes

# Constraints

- Expected to be a non-negative integer byte budget; zero allows no further body flushing.

# Inferred default

`67108864` (64 MiB).

# Tags

feature: client-networking
repository: webmachine
module: webmachine_request
concept: connections

# Notes

This is the Erlang application environment key `max_flush_bytes` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [webmachine/src/webmachine_request.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_request.erl#L753)

Additional type/default evidence:

- [webmachine/src/webmachine.app.src](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine.app.src)

# Reviewed against

3.4.0: c8d2b26a7abe933c35ced662faa28465bc4bd09c18a305e02c99601070be2f4b
3.4.1: c8d2b26a7abe933c35ced662faa28465bc4bd09c18a305e02c99601070be2f4b
