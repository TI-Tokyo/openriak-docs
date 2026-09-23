# Description

Legacy `log.crash.size` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.max_file_size` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics

# Reviewed against

3.4.0: c0a8dacde1ee01a5cd88de9fc6b47aa2162bbde6baae77b2fde4a9ca1ff569b7
3.4.1: c0a8dacde1ee01a5cd88de9fc6b47aa2162bbde6baae77b2fde4a9ca1ff569b7
