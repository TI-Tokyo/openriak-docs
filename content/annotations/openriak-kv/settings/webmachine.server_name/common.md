# Description

String placed in the HTTP `Server` response header. If no string is configured, Webmachine constructs one at startup from the Webmachine and Mochiweb versions.

# Datatype

String

# Constraints

- Erlang character list for the HTTP Server header. A non-list application value is replaced by the generated name.

# Inferred default

Constructed at application startup as `MochiWeb/<version> WebMachine/<version> (<quip>)`.

# Tags

feature: client-networking
repository: webmachine
module: webmachine_app, webmachine_request
concept: connections

# Notes

This is the Erlang application environment key `server_name` in `webmachine`. Its presence in source metadata does not establish a `riak.conf` mapping.

Source review (3.4.1 dependency revisions):

- [webmachine/src/webmachine_app.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_app.erl#L57)
- [webmachine/src/webmachine_request.erl](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine_request.erl#L972)

Additional type/default evidence:

- [webmachine/src/webmachine.app.src](https://github.com/OpenRiak/webmachine/blob/1a0c47adacc84fe1e3b28afb991b60832afae343/src/webmachine.app.src)

# Reviewed against

3.4.0: 8c96f51ab9bcd5ab53d726a1140ac74e975eec3ac3226374c0605fe95ef9663d
3.4.1: 8c96f51ab9bcd5ab53d726a1140ac74e975eec3ac3226374c0605fe95ef9663d
