# Description

Include tombstone keys in `$key` secondary-index results when using Leveled. Disabling this hides tombstone entries from those queries; other backends ignore the setting.

# Tags

feature: secondary-indexes
repository: riak_kv
module: riak_kv_leveled_backend
concept: querying

# Reviewed against

3.4.0: ef90d41c0c317c114acdf4e200f00f242aff1fb6a04f33275d76f51cbec813fe
3.4.1: 4a17248e3edd3582fe46006a29596fe5c463541d6aff4465a8f64bb1ba0b0d46
