# Description

List of `{Module, Configuration}` event-log handlers started by Webmachine. Each handler is supervised by a watcher and receives Webmachine logging events.

# Datatype

List

# Constraints

- List of `{Module, Config}` tuples; modules implement the event-handler interface and Config is the initialization argument.

# Inferred default

`[]`; no additional log handlers.

# Tags

feature: observability
repository: webmachine
module: webmachine_app
concept: diagnostics

# Notes

This is the Erlang application environment key `log_handlers` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [webmachine/src/webmachine_app.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_app.erl#L41)

Additional type/default evidence:

- [webmachine/src/webmachine.app.src](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine.app.src)

# Reviewed against

3.4.0: e79bf082e0b5d243cd3c6cec2c039ab2803687e2be6ef1ffda9271c762467c06
3.4.1: e79bf082e0b5d243cd3c6cec2c039ab2803687e2be6ef1ffda9271c762467c06
