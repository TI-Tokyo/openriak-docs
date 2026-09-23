# Description

Legacy `log.error.file` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics, filesystem-layout

# Reviewed against

3.4.0: 293017c1c016dd4b02ffa592da981e2c676323bc9f093e0ff16d814438d55244
3.4.1: 293017c1c016dd4b02ffa592da981e2c676323bc9f093e0ff16d814438d55244
