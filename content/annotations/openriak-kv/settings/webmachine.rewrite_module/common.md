# Description

Optional request-rewrite module invoked before Webmachine dispatch. It can rewrite the raw request path and headers; the value `undefined` leaves the request unchanged.

# Datatype

Module atom

# Constraints

- Module atom implementing `rewrite/5`, or `undefined`.

# Inferred default

`undefined` from `webmachine.app.src`; rewriting is disabled.

# Tags

feature: client-networking
repository: webmachine
module: webmachine_mochiweb
concept: connections

# Notes

This is the Erlang application environment key `rewrite_module` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [webmachine/src/webmachine_mochiweb.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_mochiweb.erl#L123)

Additional type/default evidence:

- [webmachine/src/webmachine.app.src](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine.app.src)

# Reviewed against

3.4.0: 0f37a75bf80a2b70e6e26e26edef992e0422ca279813c436e8a5070355edc866
3.4.1: 0f37a75bf80a2b70e6e26e26edef992e0422ca279813c436e8a5070355edc866
