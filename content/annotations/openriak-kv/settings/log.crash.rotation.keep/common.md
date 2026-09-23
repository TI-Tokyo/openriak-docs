# Description

Legacy `log.crash.rotation.keep` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.max_files` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: bc7647791b0b3b00391abe347a7397c1ffe8142316be6bf78a542b1950fb9123
3.4.1: bc7647791b0b3b00391abe347a7397c1ffe8142316be6bf78a542b1950fb9123
