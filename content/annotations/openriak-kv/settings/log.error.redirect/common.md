# Description

Legacy `log.error.redirect` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: 9bb56845c461d221c3f34d3efd336b9f0e3f0c8e3cf0fbab838e39b619359527
3.4.1: 9bb56845c461d221c3f34d3efd336b9f0e3f0c8e3cf0fbab838e39b619359527
