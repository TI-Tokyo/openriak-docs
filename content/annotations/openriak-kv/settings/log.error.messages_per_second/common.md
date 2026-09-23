# Description

Legacy `log.error.messages_per_second` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 08b01c1f44a5e1e039c67863caef2015023a0cdfb532b36edc1aeb05b8a16c58
3.4.1: 08b01c1f44a5e1e039c67863caef2015023a0cdfb532b36edc1aeb05b8a16c58
