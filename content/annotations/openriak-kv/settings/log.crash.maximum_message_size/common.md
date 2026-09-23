# Description

Legacy `log.crash.maximum_message_size` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 259c3e623aaa0a7e7d07556c49f87b889e0646ff56b1d3853f5c380fafb371d8
3.4.1: 259c3e623aaa0a7e7d07556c49f87b889e0646ff56b1d3853f5c380fafb371d8
