---
title: 'Use bucket types in an application'
description: 'Show developers how to use bucket types in an application with a minimal verified example.'
weight: 10
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\bucket-types.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show developers how to use bucket types in an application with a minimal verified example.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Bucket Types

If you ever need to turn off indexing for a bucket, set the
`search_index` property to the `_dont_index_` sentinel value.

#### Bucket Properties

Although we recommend that you use all new buckets under a bucket type,
if you have existing data with a type-free bucket (i.e. under the
`default` bucket type) you can set the `search_index` property for a
specific bucket.

```java
Namespace catsBucket = new Namespace("cats");
StoreBucketPropsOperation storePropsOp = new StoreBucketPropsOperation.Builder(catsBucket)
        .withSearchIndex("famous")
        .build();
client.execute(storePropsOp);
```

```ruby
bucket = client.bucket('cats')
bucket.properties = {'search_index' => 'famous'}
```

```php
(new \Basho\Riak\Command\Builder\Search\AssociateIndex($riak))
    ->withName('famous')
    ->buildBucket('cats')
    ->build()
    ->execute();
```

```python
bucket = client.bucket('cats')
bucket.set_properties({'search_index': 'famous'})
```

```csharp
var properties = new RiakBucketProperties();
properties.SetSearchIndex("famous");
var rslt = client.SetBucketProperties("cats", properties);
```

```javascript
var bucketProps_cb = function (err, rslt) {
    if (err) {
        throw new Error(err);
    }
    // success
};

var store = new Riak.Commands.KV.StoreBucketProps.Builder()
    .withBucket("cats")
    .withSearchIndex("famous")
    .withCallback(bucketProps_cb)
    .build();

client.execute(store);
```

```erlang
riakc_pb_socket:set_search_index(Pid, <<"cats">>, <<"famous">>).
```

```golang
cmd, err := riak.NewStoreBucketPropsCommandBuilder().
    WithBucketType("animals").
    WithBucket("cats").
    WithSearchIndex("famous").
    Build()
if err != nil {
    return err
}

err = cluster.Execute(cmd)
```

```curl
curl -XPUT $RIAK_HOST/buckets/cats/props \
     -H'content-type:application/json' \
     -d'{"props":{"search_index":"famous"}}'
```

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
