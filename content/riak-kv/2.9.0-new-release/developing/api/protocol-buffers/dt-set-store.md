---
title: "PBC Data Type Set Store"
description: ""
project: "riak_kv"
project_version: "2.9.0"
lastmod: 2019-11-21T00:00:00-00:00
sitemap:
  priority: 0.2
menu:
  riak_kv-2.9.0:
    name: "Data Type Set Store"
    identifier: "pbc_dt_set_store"
    weight: 118
    parent: "apis_pbc"
toc: true
aliases:
  - /riak/2.9.0/dev/references/protocol-buffers/dt-set-store
  - /openriak-kv/2.9.0/dev/references/protocol-buffers/dt-set-store
  - /riak/2.9.0/developing/api/protocol-buffers/dt-set-store/
  - /riak/2.9.0/developing/api/protocol-buffers/dt-set-store/
  - /openriak-kv/2.9.0/developing/api/protocol-buffers/dt-set-store/
  - /openriak-kv/2.9.0p1/developing/api/protocol-buffers/dt-set-store/
  - /openriak-kv/2.9.0p2/developing/api/protocol-buffers/dt-set-store/
  - /openriak-kv/2.9.0p3/developing/api/protocol-buffers/dt-set-store/
  - /openriak-kv/2.9.0p4/developing/api/protocol-buffers/dt-set-store/
linkTitle: "Data Type Set Store"
weight: 118
---

An operation to update a set, either on its own (at the bucket/key
level) or [inside of a map]({{<baseurl>}}openriak-kv/2.9.0/developing/api/protocol-buffers/dt-map-store).

## Request

```protobuf
message SetOp {
    repeated bytes adds    = 1;
    repeated bytes removes = 2;
}
```

Set members are binary values that can only be added (`adds`) or removed
(`removes`) from a set. You can add and/or remove as many members of a
set in a single message as you would like.
