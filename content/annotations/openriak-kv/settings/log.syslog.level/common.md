# Description

Legacy `log.syslog.level` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.additional_handlers` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 9dbd2337cbfd41362adcd36ed9dad3881cd0a89f2a085d783d36fb0acaa6165b
3.4.1: 9dbd2337cbfd41362adcd36ed9dad3881cd0a89f2a085d783d36fb0acaa6165b
