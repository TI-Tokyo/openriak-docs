---
title: 'Keys, objects, and buckets'
description: 'Explain keys, objects, and buckets, its trade-offs, and its effect on application design.'
weight: 6
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\buckets.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\keys-and-objects.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects'
  - 'https://openriak.github.io/riak/InitialDesignDecisions.html#mapping-data-to-objects---changing-the-choice'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain keys, objects, and buckets, its trade-offs, and its effect on application design.

## Overview

### Buckets

[apps cluster metadata]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/cluster-metadata/
[cluster ops bucket types]: {{< baseurl >}}kv/3.4.0/how-to/operate/manage-bucket-types/
[cluster ops strong consistency]: {{< baseurl >}}kv/3.4.0/explanation/consistency/strong-consistency/
[concept causal context]: {{< baseurl >}}kv/3.4.0/explanation/data-model/causal-context/
[concept causal context sib]: {{< baseurl >}}kv/3.4.0/explanation/data-model/causal-context/#siblings
[concept replication]: {{< baseurl >}}kv/3.4.0/explanation/replication/
[concept strong consistency]: {{< baseurl >}}kv/3.4.0/reference/specialized-apis/strong-consistency-api/
[config basic]: {{< baseurl >}}kv/3.4.0/how-to/configure/basic-node-settings/
[dev api http]: {{< baseurl >}}kv/3.4.0/reference/http-api/
[dev data types]: {{< baseurl >}}kv/3.4.0/reference/data/distributed-data-types/
[glossary ring]: {{< baseurl >}}kv/3.4.0/explanation/foundations/glossary/#ring
[plan backend leveldb]: {{< baseurl >}}kv/3.4.0/explanation/storage/leveldb/
[plan backend bitcask]: {{< baseurl >}}kv/3.4.0/explanation/storage/bitcask/
[plan backend memory]: {{< baseurl >}}kv/3.4.0/explanation/storage/memory/
[plan backend multi]: {{< baseurl >}}kv/3.4.0/explanation/storage/multi-backend/
[usage bucket types]: {{< baseurl >}}kv/3.4.0/how-to/develop/use-bucket-types/
[usage commit hooks]: {{< baseurl >}}kv/3.4.0/how-to/develop/write-commit-hook/
[usage conflict resolution]: {{< baseurl >}}kv/3.4.0/how-to/develop/resolve-conflicts/
[usage replication]: {{< baseurl >}}kv/3.4.0/explanation/replication/

Buckets are used to define a virtual keyspace for storing Riak objects.
They enable you to define non-default configurations over that keyspace
concerning [replication properties][concept replication] and [other
parameters][config basic].

In certain respects, buckets can be compared to tables in relational
databases or folders in filesystems, respectively. From the standpoint
of performance, buckets with default configurations are essentially
"free," while non-default configurations, defined [using bucket
types][cluster ops bucket types], will be gossiped around [the ring][glossary read rep] using OpenRiak's [cluster metadata][apps cluster metadata] subsystem.

#### Configuration

Bucket configurations are defined [using bucket types][cluster ops bucket types], which enables
you to create and modify sets of configurations and apply them to as
many buckets as you wish. With bucket types, you can configure the
following bucket-level parameters, overriding the default values if you
wish.

##### allow_mult

Determines whether sibling values can be created. See [siblings][concept causal context sib]. The default can be `true` or `false` depending on
the context. See the documentation on [`allow_mult`][usage bucket types] for more
information.

###### n_val

Specifies the number of copies of each object to be stored in the
cluster. See the documentation on [replication properties][usage replication]. Default:
`3`.

###### last_write_wins

Indicates if an object's timestamp will be used to decide the canonical
write in the case of a conflict. See the documentation on [vector
clocks][concept causal context] and on [conflict resolution][usage conflict resolution] for more information. Default:
`false`.

###### r, pr, w, dw, pw, rw, notfound_ok, basic_quorum

See the documentation on [replication properties][usage replication] for more information
on all of these properties.

###### precommit

A list of Erlang functions to be executed before writing an object. See
our documentation on [pre-commit hooks][usage commit hooks] for more information. Default: no pre-commit
hooks, i.e. an empty list.

###### postcommit

A list of Erlang functions to be executed after writing an object. See
our documentation on [pre-commit hooks][usage commit hooks] for more information. Default: no post-commit
hooks, i.e. an empty list.

###### old_vclock, young_vclock, small_vclock, big_vclock

These settings enable you to manage [vector clock pruning][concept causal context].

###### backend

If you are using the [Multi][plan backend multi] backend, this property enables you to
determine which of OpenRiak's available backends---[Bitcask][plan backend bitcask], [LevelDB][plan backend leveldb], or [Memory][plan backend memory]---will be used in buckets of this type. If you are using
LevelDB, Bitcask, or the Memory backend at a cluster-wide level, _all_
buckets of all types will use the assigned backend.

###### consistent

If you are using OpenRiak's experimental [strong consistency][concept strong consistency] feature for buckets
bearing a type, this setting must be set to `true`. The default is
`false`. More information can be found in our documentation on [using
strong consistency][cluster ops strong consistency].

###### datatype

If you are using [Riak data types][dev data types], this setting
determines which data type will be used in
buckets of this bucket type. Possible values: `counter`, `set`, or
`map`.

###### dvv_enabled

Whether [dotted version vectors][concept causal context]
will be used instead of traditional vector clocks for [conflict resolution][usage conflict resolution]. Default: `false`.

###### chash_keyfun, linkfun

These settings involve features that have been deprecated. You will not
need to adjust these values.

##### Fetching Bucket Properties

If you'd like to see how a particular bucket has been configured, you
can do so using our official client libraries or through OpenRiak's [HTTP
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
#### Assuming that Riak is running on "localhost" and port 8087:

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

### Keys and Objects

[concept buckets]: {{< baseurl >}}kv/3.4.0/explanation/data-model/keys-objects-and-buckets/
[concept causal context vc]: {{< baseurl >}}kv/3.4.0/explanation/data-model/causal-context/#vector-clocks

In an RDBMS, data is organized by tables that are individually
identifiable entities. Within those tables exist rows of a data
organized into columns. It is possible to retrieve or update entire
tables, individual rows, or a group of columns within a set of
rows. In contrast, Riak has a simpler data model in which the Object
(explained below) is both the largest and smallest data element. When
performing any fetch or update operation in Riak, the entire Riak
Object must be retrieved or modified; there are no partial fetches or
updates.

#### Keys

Keys in Riak are simply binary values (or strings) used to identify
Objects. From the perspective of a client interacting with Riak,
each bucket appears to represent a separate keyspace. It is important
to understand that Riak treats the bucket-key pair as a single entity
when performing fetch and store operations (see: [Buckets][concept buckets]).

#### Objects

Objects are the only unit of data storage in Riak. Riak Objects are
essentially structs identified by bucket and key and composed of the
following parts: a bucket, key, vector clock, and a list of
metadata-value pairs. Normally, objects have only one metadata-value
pair, but when there are more than one, the object is said to have
"siblings". These siblings may occur both within a single node and
across multiple nodes, and do occur when either more than one actor
updates an object, a network partition occurs, or a stale vector clock
is submitted when updating an object (see: [Vector Clocks][concept causal context vc]).

#### Mapping data to objects - changing the choice

Riak is designed to be agnostic to the format of the data, the schema belongs to the application and not the database.  It is therefore necessary to plan for schema migration within the application - detecting the schema version for an object, finding objects within a given schema version, updating a schema version in parallel to other application activity.

> It is recommended to plan for a lazy migration strategy, whereby the application can roll forward each object to the latest version on GET, without necessarily updating the persisted version, and then only updating the schema for the object on update.  With a lazy migration strategy, at the point of change only freshly updated objects will change.  Eventually all objects may need to be changed, and planning for a batch process to touch all objects not updated since the migration point will be required.
