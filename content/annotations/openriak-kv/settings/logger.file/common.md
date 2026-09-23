# Description

Path of the default Erlang log file. Ensure the Riak service account can write it; `logger.max_file_size` and `logger.max_files` control its rotation and retention.

# Tags

feature: observability
repository: riak
module: riak.schema
concept: diagnostics, filesystem-layout

# Reviewed against

3.4.0: f0b7f190a51f9e34bcb3ec5031441f3668307104afe2e70a7aa17d2dcc3c3441
3.4.1: f0b7f190a51f9e34bcb3ec5031441f3668307104afe2e70a7aa17d2dcc3c3441
