# Description

Legacy `log.syslog.ident` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.additional_handlers` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 0f98a89e0d298b200e01245c8d539dbb9b401fb0bf4912ef0eebfcfcdb95f53f
3.4.1: 0f98a89e0d298b200e01245c8d539dbb9b401fb0bf4912ef0eebfcfcdb95f53f
