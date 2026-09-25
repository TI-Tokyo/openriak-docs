# Description

Module used to render HTTP error responses through `render_error/3`. Webmachine supplies the status, request state and error reason, then uses the returned body and updated request state.

# Datatype

Module atom

# Constraints

- Module atom implementing `render_error/3`.

# Inferred default

`webmachine_error_handler` from `webmachine.app.src`.

# Tags

feature: client-networking
repository: webmachine
module: webmachine_decision_core, webmachine_mochiweb
concept: diagnostics

# Notes

This is the Erlang application environment key `error_handler` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [webmachine/src/webmachine_decision_core.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_decision_core.erl#L125)
- [webmachine/src/webmachine_mochiweb.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_mochiweb.erl#L182)

Additional type/default evidence:

- [webmachine/src/webmachine.app.src](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine.app.src)

# Reviewed against

3.4.0: f5ad39b307b116b3f1c573afa9b55cb2ca8ee7a8dd66ec762eefeacf5aa860d7
3.4.1: f5ad39b307b116b3f1c573afa9b55cb2ca8ee7a8dd66ec762eefeacf5aa860d7
