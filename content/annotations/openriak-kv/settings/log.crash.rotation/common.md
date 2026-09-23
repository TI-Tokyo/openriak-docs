# Description

Legacy `log.crash.rotation` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: f004ed15d257abf40a87eaf226542a58d6ff63ac7462d427f8fd2d95a58b2911
3.4.1: f004ed15d257abf40a87eaf226542a58d6ff63ac7462d427f8fd2d95a58b2911
