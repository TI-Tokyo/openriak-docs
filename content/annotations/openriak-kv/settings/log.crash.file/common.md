# Description

Legacy `log.crash.file` option accepted for configuration compatibility but unused in these releases. Configure the current Erlang logger instead; start with `logger.file` and the handler-specific options.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics, filesystem-layout

# Reviewed against

3.4.0: 189a4afe74df49a6d33d179fc9204e8157fd3d4f8c1f68841abdfcaa8c64f039
3.4.1: 189a4afe74df49a6d33d179fc9204e8157fd3d4f8c1f68841abdfcaa8c64f039
