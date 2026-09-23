# Description

Select object-version merge behaviour for untyped buckets. Strategy `2` uses dotted version vectors to reduce duplicate siblings; strategy `1` retains the older merge behaviour that can produce extra siblings under interleaved writes.

# Tags

feature: bucket-properties
repository: riak_kv
module: riak_kv.schema
concept: compaction, data-policy

# Reviewed against

3.4.0: 72c7014d1c1fbb6e114b74f698ff57db2d33f01de4b63117082eb3b392c455d7
3.4.1: b0ff62ec4a102b645809256f3ba9dbfe772a347422c9522a1c6afec2d318eb85
