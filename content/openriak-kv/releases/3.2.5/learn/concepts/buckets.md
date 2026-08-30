---
weight: 101
slug: 'buckets'
title: "Buckets"
description: ""
project: "riak_kv"
project_version: "3.2.5"
lastmod: 2025-03-24T00:00:00-00:00
sitemap:
  priority: 0.9
menu:
  riak_kv-3.2.5:
    name: "Buckets"
    identifier: "learn_concepts_buckets"
    weight: 101
    parent: "learn_concepts"
toc: true
aliases:
  - /riak/3.2.5/theory/concepts/Buckets
  - /riak/kv/3.2.5/theory/concepts/Buckets
  - /riak/3.2.5/theory/concepts/buckets
  - /riak/kv/3.2.5/theory/concepts/buckets
---

[apps cluster metadata]: {{< product-version-root >}}developing/app-guide/cluster-metadata
[cluster ops bucket types]: {{< product-version-root >}}using/cluster-operations/bucket-types
[cluster ops strong consistency]: {{< product-version-root >}}using/cluster-operations/strong-consistency
[concept causal context]: {{< product-version-root >}}learn/concepts/causal-context
[concept causal context sib]: {{< product-version-root >}}learn/concepts/causal-context/#siblings
[concept replication]: {{< product-version-root >}}learn/concepts/replication
[concept strong consistency]: {{< product-version-root >}}using/reference/strong-consistency
[config basic]: {{< product-version-root >}}configuring/basic
[dev api http]: {{< product-version-root >}}developing/api/http
[dev data types]: {{< product-version-root >}}developing/data-types
[glossary ring]: {{< product-version-root >}}learn/glossary/#ring
[plan backend leveldb]: {{< product-version-root >}}setup/planning/backend/leveldb
[plan backend bitcask]: {{< product-version-root >}}setup/planning/backend/bitcask
[plan backend memory]: {{< product-version-root >}}setup/planning/backend/memory
[plan backend multi]: {{< product-version-root >}}setup/planning/backend/multi
[usage bucket types]: {{< product-version-root >}}developing/usage/bucket-types
[usage commit hooks]: {{< product-version-root >}}developing/usage/commit-hooks
[usage conflict resolution]: {{< product-version-root >}}developing/usage/conflict-resolution
[usage replication]: {{< product-version-root >}}developing/usage/replication

Buckets are used to define a virtual keyspace for storing Riak objects.
They enable you to define non-default configurations over that keyspace
concerning [replication properties][concept replication] and [other
parameters][config basic].

In certain respects, buckets can be compared to tables in relational
databases or folders in filesystems, respectively. From the standpoint
of performance, buckets with default configurations are essentially
"free," while non-default configurations, defined [using bucket
types][cluster ops bucket types], will be gossiped around [the ring][glossary read rep] using Riak's [cluster metadata][apps cluster metadata] subsystem.

## Configuration

Bucket configurations are defined [using bucket types][cluster ops bucket types], which enables
you to create and modify sets of configurations and apply them to as
many buckets as you wish. With bucket types, you can configure the
following bucket-level parameters, overriding the default values if you
wish.

#### allow_mult

Determines whether sibling values can be created. See [siblings][concept causal context sib]. The default can be `true` or `false` depending on
the context. See the documentation on [`allow_mult`][usage bucket types] for more
information.

#### n_val

Specifies the number of copies of each object to be stored in the
cluster. See the documentation on [replication properties][usage replication]. Default:
`3`.

#### last_write_wins

Indicates if an object's timestamp will be used to decide the canonical
write in the case of a conflict. See the documentation on [vector
clocks][concept causal context] and on [conflict resolution][usage conflict resolution] for more information. Default:
`false`.

#### r, pr, w, dw, pw, rw, notfound_ok, basic_quorum

See the documentation on [replication properties][usage replication] for more information
on all of these properties.

#### precommit

A list of Erlang functions to be executed before writing an object. See
our documentation on [pre-commit hooks][usage commit hooks] for more information. Default: no pre-commit
hooks, i.e. an empty list.

#### postcommit

A list of Erlang functions to be executed after writing an object. See
our documentation on [pre-commit hooks][usage commit hooks] for more information. Default: no post-commit
hooks, i.e. an empty list.

#### old_vclock, young_vclock, small_vclock, big_vclock

These settings enable you to manage [vector clock pruning][concept causal context].

#### backend

If you are using the [Multi][plan backend multi] backend, this property enables you to
determine which of Riak's available backends---[Bitcask][plan backend bitcask], [LevelDB][plan backend leveldb], or [Memory][plan backend memory]---will be used in buckets of this type. If you are using
LevelDB, Bitcask, or the Memory backend at a cluster-wide level, _all_
buckets of all types will use the assigned backend.

#### consistent

If you are using Riak's experimental [strong consistency][concept strong consistency] feature for buckets
bearing a type, this setting must be set to `true`. The default is
`false`. More information can be found in our documentation on [using
strong consistency][cluster ops strong consistency].

#### datatype

If you are using [Riak data types][dev data types], this setting
determines which data type will be used in
buckets of this bucket type. Possible values: `counter`, `set`, or
`map`.

#### dvv_enabled

Whether [dotted version vectors][concept causal context]
will be used instead of traditional vector clocks for [conflict resolution][usage conflict resolution]. Default: `false`.

#### chash_keyfun, linkfun

These settings involve features that have been deprecated. You will not
need to adjust these values.

## Fetching Bucket Properties

If you'd like to see how a particular bucket has been configured, you
can do so using our official client libraries or through Riak's [HTTP
API][dev api http]. The following would fetch the properties for the bucket
`animals` if that bucket had a default configuration, i.e. the `default`
bucket type:

```java
Namespace animalsBucket = new Namespace("animals");
FetchBucketProperties fetchProps =
    new FetchBucketProperties.Builder(animalsBucket).build();
FetchBucketProperties.Response response = client.execute(fetchProps);
BucketProperties props = response.getProperties();
```

```ruby
bucket = client.bucket('animals')
bucket.properties
```

```php
$bucketProperties = (new \Basho\Riak\Command\Builder\FetchBucketProperties($riak))
  ->buildBucket('animals')
  ->build()
  ->execute()
  ->getBucket()
  ->getProperties();
```

```python
bucket = client.bucket('animals')
bucket.get_properties()
```

```erlang
{ok, Props} = riakc_pb_socket:get_bucket(Pid, <<"animals">>).
```

```curl
# Assuming that Riak is running on "localhost" and port 8087:

curl http://localhost:8087/types/default/buckets/animals/props
```

If the bucket `animals` had a different type that you had created and
activated, e.g. `my_custom_type`, you could fetch the bucket properties
like so:

```java
Namespace customTypedBucket = new Namespace("my_custom_type", "animals");
FetchBucketProperties fetchProps =
    new FetchBucketProperties.Builder(customTypedBucket).build();
FetchBucketProperties.Response response = client.execute(fetchProps);
BucketProperties props = response.getProperties();
```

```ruby
bucket = client.bucket_type('my_custom_type').bucket('animals')
bucket.properties
```

```php
$bucketProperties = (new \Basho\Riak\Command\Builder\FetchBucketProperties($riak))
  ->buildBucket('animals', 'my_custom_type')
  ->build()
  ->execute()
  ->getBucket()
  ->getProperties();
```

```python
bucket = client.bucket_type('my_custom_type').bucket('animals')
bucket.get_properties()
```

```erlang
{ok, Props} = riakc_pb_socket:get_bucket(Pid, {<<"my_custom_type">>, <<"animals">>}).
```

```curl
curl http://localhost:8087/types/my_custom_type/buckets/animals/props
```

[glossary read rep]: {{< product-version-root >}}learn/glossary/#read-repair
