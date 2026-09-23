# Description

Legacy `log.syslog.facility` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.additional_handlers` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 2c9414aa6d8917ae475238dd09502d8428286590ce50c7a54192e0430a142648
3.4.1: 2c9414aa6d8917ae475238dd09502d8428286590ce50c7a54192e0430a142648
