# Description

For the named backend `$name`: Directory containing LevelDB partition databases. Ensure sufficient disk capacity and write access for the Riak service account; moving the configured path alone does not migrate existing data. Replace `$name` with the configured backend name; this entry is scoped to that backend.

# Tags

feature: leveldb
repository: eleveldb
module: eleveldb_multi.schema
concept: filesystem-layout, storage

# Reviewed against

3.4.0: f5f9bd92360b4da226cb395e0963a1e27ca19d5fe2ec24a50d9c8478794626e4
3.4.1: f5f9bd92360b4da226cb395e0963a1e27ca19d5fe2ec24a50d9c8478794626e4
