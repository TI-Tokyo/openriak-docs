---
title: 'Replication concepts'
description: 'Introduce repair, convergence, and multi-cluster data movement in OpenRiak.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\replication.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\learn\concepts\replication.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#overview'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#riak-kv---replication-and-reconciliation'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce repair, convergence, and multi-cluster data movement in OpenRiak.

## Overview

### Replication

[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[concept eventual consistency]: {{< product-version-root >}}foundations/consistency/eventual-consistency/
[plan backend leveldb]: {{< product-version-root >}}foundations/storage/leveldb/
[plan backend bitcask]: {{< product-version-root >}}foundations/storage/bitcask/
[use ref strong consistency]: {{< product-version-root >}}reference/specialized-apis/strong-consistency-api/
[concept clusters]: {{< product-version-root >}}foundations/foundations/clusters-rings-and-partitions/

Riak was built to act as a multi-node [cluster][concept clusters].  It
distributes data across multiple physical servers, which enables it to
provide strong availability guarantees and fault tolerance.

The [CAP theorem](http://en.wikipedia.org/wiki/CAP_theorem), which
undergirds many of the design decisions behind OpenRiak's architecture,
defines distributed systems in terms of three desired properties:
consistency, availability, and partition (i.e. failure) tolerance. Riak
can be used either as an AP, i.e. available/partition-tolerant, system
or as a CP, i.e. consistent/partition-tolerant, system. The former
relies on an [Eventual Consistency][concept eventual consistency] model, while the latter relies on
a special [strong consistency][use ref strong consistency] subsystem.

Although the [CAP theorem](http://en.wikipedia.org/wiki/CAP_theorem)
dictates that there is a necessary trade-off between data consistency
and availability, if you are using Riak in an eventually consistent
manner, you can fine-tune that trade-off. The ability to make these
kinds of fundamental choices has immense value for your applications and
is one of the features that differentiates Riak from other databases.

At the bottom of the page, you'll find a [screencast]({{< product-version-root >}}foundations/replication/references-and-triggers/#screencast) that briefly explains how to adjust your
replication levels to match your application and business needs.

**Note on strong consistency**
An option introduced in Riak version 2.0 is to use Riak as a
<a href="{{< product-version-root >}}reference/specialized-apis/strong-consistency-api/">strongly
consistent</a> system for data in specified buckets. Using Riak in this way is
fundamentally different from adjusting replication properties and fine-tuning
the availability/consistency trade-off, as it sacrifices _all_ availability
guarantees when necessary. Therefore, you should consult the
<a href="{{< product-version-root >}}reference/specialized-apis/strong-consistency-api/">Using
Strong Consistency</a> documentation, as this option will not be covered in
this tutorial.

#### How Replication Properties Work

When using Riak, there are two ways of choosing replication properties:

1. On a per-request basis
2. In a more programmatic fashion, [using bucket types][usage bucket types]

##### Per-request Replication Properties

The simplest way to apply replication properties to objects stored in
Riak is to specify those properties

##### Replication Properties Through Bucket Types

Let's say, for example, that you want to apply an `n_val` of 5, an `r`
of 3, and a `w` of 3 to all of the data in some of the [buckets]({{< product-version-root >}}foundations/data-model/keys-objects-and-buckets/) that
you're using. In order to set those replication properties, you should
create a bucket type that sets those properties. Below is an example:

```bash
riak admin bucket-type create custom_props '{"props":{"n_val":5,"r":3,"w":3}}'
riak admin bucket-type activate custom_props
```

Now, any time you store an object in a bucket with the type
`custom_props` those properties will apply to it.

#### Available Parameters

The table below lists the most frequently used replication parameters
that are available in Riak. Symbolic values like `quorum` are discussed
[below](#symbolic-consistency-names). Each
parameter will be explained in more detail in later sections:

Parameter | Common name | Default value | Description
:---------|:------------|:--------------|:-----------
`n_val` | N | `3` | Replication factor, i.e. the number of nodes in the cluster on which an object is to be stored
`r` | R | `quorum` | The number of servers that must respond to a read request
`w` | W | `quorum` | Number of servers that must respond to a write request
`pr` | PR | `0` | The number of primary <a href="{{< product-version-root >}}foundations/foundations/virtual-nodes/">vnodes</a> that must respond to a read request
`pw` | PW | `0` | The number of primary <a href="{{< product-version-root >}}foundations/foundations/virtual-nodes/">vnodes</a> that must respond to a write request
`dw` | DW | `quorum` | The number of servers that must report that a write has been successfully written to disk
`rw` | RW | `quorum` | If R and W are undefined, this parameter will substitute for both R and W during object deletes. It is extremely unlikely that you will need to adjust this parameter.
`notfound_ok` | | `true` | This parameter determines how Riak responds if a read fails on a node. Setting to `true` (the default) is the equivalent to setting R to 1: if the first node to respond doesn't have a copy of the object, Riak will immediately return a `not found` error. If set to `false`, Riak will continue to look for the object on the number of nodes specified by N (aka `n_val`).
`basic_quorum` | | `false` | If `notfound_ok` is set to `false`, Riak will be more thorough in looking for an object on multiple nodes. Setting `basic_quorum` to `true` in this case will instruct Riak to wait for only a `quorum` of responses to return a `notfound` error instead of N responses.

#### A Primer on N, R, and W

The most important thing to note about OpenRiak's replication controls is
that they can be at the bucket level. You can use [bucket types]({{< product-version-root >}}how-to/develop/use-bucket-types/)
to set up bucket `A` to use a particular set of replication properties
and bucket `B` to use entirely different properties.

At the bucket level, you can choose how many copies of data you want to
store in your cluster (N, or `n_val`), how many copies you wish to read
from at one time (R, or `r`), and how many copies must be written to be
considered a success (W, or `w`).

In addition to the bucket level, you can also specify replication
properties on the client side for any given read or write. The examples
immediately below will deal with bucket-level replication settings, but
check out the [section below](#client-level-replication-settings)
for more information on setting properties on a per-operation basis.

The most general trade-off to be aware of when setting these values is
the trade-off between **data accuracy** and **client responsiveness**.
Choosing higher values for N, R, and W will mean higher accuracy because
more nodes are checked for the correct value on read and data is written
to more nodes upon write; but higher values will also entail degraded
responsiveness, especially if one or more nodes is failing, because Riak
has to wait for responses from more nodes.

#### N Value and Replication

All data stored in Riak will be replicated to the number of nodes in the
cluster specified by a bucket's N value (`n_val`). The default `n_val`
in Riak is 3, which means that data stored in a bucket with the default
N will be replicated to three different nodes, thus storing three
**replicas** of the object.

In order for this to be effective, you need at least three nodes in your
cluster. The merits of this system, however, can be demonstrated using
your local environment.

Let's create a bucket type that sets the `n_val` for any bucket with
that type to 2. To do so, you must create and activate a bucket type
that sets this property:

```bash
riak admin bucket-type create n_val_equals_2 '{"props":{"n_val":2}}'
riak admin bucket-type activate n_val_equals_2
```

Now, all buckets that bear the type `n_val_equals_2` will have `n_val`
set to 2. Here's an example write:

```curl
curl -XPUT http://localhost:8098/types/n_val_equals_2/buckets/test_bucket/keys/test_key \
  -H "Content-Type: text/plain" \
  -d "the n_val on this write is 2"
```

Now, whenever we write to a bucket of this type, Riak will write a
replica of the object to two different nodes.

**A Word on Setting the N Value**
`n_val` must be greater than 0 and less than or equal to the number of actual
nodes in your cluster to get all the benefits of replication. We advise
against modifying the `n_val` of a bucket after its initial creation as this
may result in failed reads because the new value may not be replicated to all
the appropriate partitions.

#### R Value and Read Failure Tolerance

Read requests to Riak are sent to all N nodes that are known to be
currently responsible for the data. The R value (`r`) enables you to
specify how many of those nodes have to return a result on a given read
for the read to be considered successful. This allows Riak to provide
read availability even when nodes are down or laggy.

You can set R anywhere from 1 to N; lower values mean faster response
time but a higher likelihood of Riak not finding the object you're
looking for, while higher values mean that Riak is more likely to find
the object but takes longer to look.

As an example, let's create and activate a bucket type with `r` set to
`1`. All reads performed on data in buckets with this type require a
result from only one node.

```bash
riak admin bucket-type create r_equals_1 '{"props":{"r":1}}'
riak admin bucket-type activate r_equals_1
```

Here's an example read request using the `r_equals_1` bucket type:

```ruby
bucket = client.bucket_type('r_equals_1').bucket('animal_facts')
obj = bucket.get('chimpanzee')
```

```java
Location chimpanzeeFact =
  new Location(new Namespace("r_equals_1", "animal_facts"), "chimpanzee");
FetchValue fetch = new FetchValue.Builder(chimpanzeeFact).build();
FetchValue.Response response = client.execute(fetch);
RiakObject obj = response.getValue(RiakObject.class);
System.out.println(obj.getValue().toString());
```

```php
$response = (new \Basho\Riak\Command\Builder\FetchObject($riak))
  ->buildLocation('chimpanzee', 'animal_facts', 'r_equals_1')
  ->build()
  ->execute();

echo $response->getObject()->getData();
```

```python
bucket = client.bucket_type('r_equals_1').bucket('animal_facts')
bucket.get('chimpanzee')
```

```erlang
{ok, Obj} = riakc_pb_socket:get(Pid,
                                {<<"r_equals_1">>, <<"animal_facts">>},
                                <<"chimpanzee">>).
```

```curl
curl http://localhost:8098/types/r_equals_1/buckets/animal_facts/keys/chimpanzee
```

As explained above, reads to buckets with the `r_equals_1` type will
typically be completed more quickly, but if the first node to respond
to a read request has yet to receive a replica of the object, Riak will
return a `not found` response (which may happen even if the object lives
on one or more other nodes). Setting `r` to a higher value will mitigate
this risk.

#### W Value and Write Fault Tolerance

As with read requests, writes to Riak are sent to all N nodes that are
know to be currently responsible for the data. The W value (`w`) enables
you to specify how many nodes must complete a write to be considered
successful---a direct analogy to R. This allows Riak to provide write
availability even when nodes are down or laggy.

As with R, you can set W to any value between 1 and N. The same
performance vs. fault tolerance trade-offs that apply to R apply to W.

As an example, let's create and activate a bucket type with `w` set to
`3`:

```bash
riak admin bucket-type create w_equals_3 '{"props":{"w":3}}'
riak admin activate w_equals_3
```

Now, we can attempt a write to a bucket bearing the type `w_equals_3`:

```ruby
bucket = client.bucket_type('w_equals_3').bucket('animal_facts')
obj = Riak::RObject.new(bucket, 'giraffe')
obj.raw_data = 'The species name of the giraffe is Giraffa camelopardalis'
obj.content_type = 'text/plain'
obj.store
```

```java
Location storyKey =
  new Location(new Namespace("w_equals_3", "animal_facts"), "giraffe");
RiakObject obj = new RiakObject()
        .setContentType("text/plain")
        .setValue(BinaryValue.create("The species name of the giraffe is Giraffa camelopardalis"));
StoreValue store = new StoreValue.Builder(obj)
        .withLocation("giraffe")
        .build();
client.execute(store);
```

```php
(new \Basho\Riak\Command\Builder\StoreObject($riak))
  ->buildLocation('giraffe', 'animal_facts', 'w_equals_3')
  ->build()
  ->execute();
```

```python
bucket = client.bucket_type('w_equals_3').bucket('animal_facts')
obj = RiakObject(client, bucket, 'giraffe')
obj.content_type = 'text/plain'
obj.data = 'The species name of the giraffe is Giraffa camelopardalis'
obj.store()
```

```erlang
Obj = riakc_object:new({<<"w_equals_3">>, <<"animal_facts">>},
                       <<"giraffe">>,
                       <<"The species name of the giraffe is Giraffa camelopardalis">>,
                       <<"text/plain">>),
riakc_pb_socket:put(Pid, Obj).
```

```curl
curl -XPUT \
  -H "Content-type: text/plain" \
  -d "The species name of the giraffe is Giraffa camelopardalis" \
  http://localhost:8098/types/w_equals_3/buckets/animal_facts/keys/giraffe
```

Writing our `story.txt` will return a success response from Riak only if
3 nodes respond that the write was successful. Setting `w` to 1, for
example, would mean that Riak would return a response more quickly, but
with a higher risk that the write will fail because the first node it
seeks to write the object to is unavailable.

#### Primary Reads and Writes with PR and PW

In OpenRiak's replication model, there are N [vnodes]({{< product-version-root >}}foundations/foundations/glossary/#vnode),
called _primary vnodes_, that hold primary responsibility for any given
key. Riak will attempt reads and writes to primary vnodes first, but in
case of failure, those operations will go to failover nodes in order to
comply with the R and W values that you have set. This failover option
is called _sloppy quorum_.

In addition to R and W, you can also set integer values for the *primary
read* (PR) and _primary write_ (PW) parameters that specify how many
primary nodes must respond to a request in order to report success to
the client. The default for both values is zero.

Setting PR and/or PW to non-zero values produces a mode of operation
called _strict quorum_. This mode has the advantage that the client is
more likely to receive the most up-to-date values, but at the cost of a
higher probability that reads or writes will fail because primary vnodes
are unavailable.

**Note on PW**
If PW is set to a non-zero value, there is a higher risk (usually very small)
that failure will be reported to the client upon write. But this does not
necessarily mean that the write has failed completely. If there are reachable
primary vnodes, those vnodes will still write the new data to Riak. When the
failed vnode returns to service, it will receive the new copy of the data via
either read repair or active anti-entropy.

#### Durable Writes with DW

The W and PW parameters specify how many vnodes must _respond_ to a
write in order for it to be deemed successful. What they do not specify
is whether data has actually been written to disk in the storage backend.
The DW parameters enables you to specify a number of vnodes between 1
and N that must write the data to disk before the request is deemed
successful. The default value is `quorum` (more on symbolic names below).

How quickly and robustly data is written to disk depends on the
configuration of your backend or backends. For more details, see the
documentation on [Bitcask][plan backend bitcask], [LevelDB][plan backend leveldb], and [multiple backends]({{< product-version-root >}}foundations/storage/multi-backend/).

#### Delete Quorum with RW

**Deprecation notice**
It is no longer necessary to specify an RW value when making delete requests.
We explain its meaning here, however, because RW still shows up as a property
of Riak buckets (as `rw`) for the sake of backwards compatibility. Feel free
to skip this explanation unless you are curious about the meaning of RW.

Deleting an object requires successfully reading an object and then
writing a tombstone to the object's key that specifies that an object
once resided there. In the course of their operation, all deletes must
comply with any R, W, PR, and PW values that apply along the way.

If R and W are undefined, however, the RW (`rw`) value will substitute
for both R and W during object deletes. In recent versions of Riak, it
is nearly impossible to make reads or writes that do not somehow specify
oth R and W, and so you will never need to worry about RW.

#### The Implications of `notfound_ok`

The `notfound_ok` parameter is a bucket property that determines how
Riak responds if a read fails on a node. If `notfound_ok` is set to
`true` (the default value) and the first vnode to respond doesn't have a
copy of the object, Riak will assume that the missing value is
authoritative and immediately return a `not found` result to the client.
This will generally lead to faster response times.

On the other hand, setting `notfound_ok` to `false` means that the
responding vnode will wait for something other than a `not found` error
before reporting a value to the client. If an object doesn't exist under
a key, the coordinating vnode will wait for N vnodes to respond with
`not found` before it reports `not found` to the client. This setting
makes Riak search more thoroughly for objects but at the cost of slower
response times, a problem can be mitigated by setting `basic_quorum` to
`true`, which is discussed in the next section.

#### Early Failure Return with `basic_quorum`

Setting `notfound_ok` to `false` on a request (or as a bucket property)
is likely to introduce additional latency. If you read a non-existent
key, Riak will check all 3 responsible vnodes for the value before
returning `not found` instead of checking just one.

This latency problem can be mitigated by setting `basic_quorum` to
`true`, which will instruct Riak to query a quorum of nodes instead of N
nodes. A quorum of nodes is calculated as floor(N/2) + 1, meaning that 5
nodes will produce a quorum of 3, 6 nodes a quorum of 4, 7 nodes a
quorum of 4, 8 nodes a quorum of 5, etc.

The default for `basic_quorum` is `false`, so you will need to
explicitly set it to `true` on reads or in a bucket's properties. While
the scope of this setting is fairly narrow, it can reduce latency in
read-heavy use cases.

#### Symbolic Consistency Names

Riak provides a number of "symbolic" consistency options for R, W, PR,
RW, and DW that are often easier to use and understand than specifying
integer values. The following symbolic names are available:

* `all` - All replicas must reply. This is the same as setting R, W, PR, RW, or DW equal to N.
* `one` - This is the same as setting 1 as the value for R, W, PR, RW, or DW.
* `quorum` - A majority of the replicas must respond, that is, half plus one. For the default N value of 3, this calculates to 2, an N value of 5 calculates to 3, and so on.
* `default` - Uses whatever the per-bucket consistency property is for R, W, PR, RW, or DW, which may be any of the above symbolic values or an integer.

Not submitting a value for R, W, PR, RW, or DW is the same as using
`default`.

#### Client-level Replication Settings

Adjusting replication properties at the bucket level by [using bucket types][usage bucket types]
is how you set default properties for _all_ of a bucket's reads and
writes. But you can also set replication properties for specific reads
and writes without setting those properties at the bucket level, instead
specifying them on a per-operation basis.

Let's say that you want to set `r` to 2 and `notfound_ok` to `true` for
just one read. We'll fetch [John Stockton](http://en.wikipedia.org/wiki/John_Stockton)'s
statistics from the `nba_stats` bucket.

```ruby
bucket = client.bucket('nba_stats')
obj = bucket.get('john_stockton', r: 2, notfound_ok: true)
```

```java
Location johnStocktonStats =
  new Namespace(new Namespace("nba_stats"), "john_stockton");
FetchValue fetch = new FetchValue.Builder(johnStocktonStats)
        .withOption(FetchOption.R, new Quorum(2))
        .withOption(FetchOption.NOTFOUND_OK, true)
        .build();
client.execute(fetch);
```

```php
(new \Basho\Riak\Command\Builder\FetchObject($riak))
  ->buildLocation('john_stockton', 'nba_stats')
  ->withParameter('r', 2)
  ->withParameter('notfound_ok', true)
  ->build()
  ->execute();
```

```python
bucket = client.bucket('nba_stats')
obj = bucket.get('john_stockton', r=2, notfound_ok=True)
```

```erlang
{ok, Obj} = riakc_pb_socket:get(Pid,
                                <<"nba_stats">>,
                                <<"john_stockton">>,
                                [{r, 2}, {notfound_ok, true}]).
```

```curl
curl http://localhost:8098/buckets/nba_stats/keys/john_stockton?r=2&notfound_ok=true
```

Now, let's say that you want to attempt a write with `w` set to 3 and
`dw` set to 2. As in the previous example, we'll be using the `default`
bucket type, which enables us to not specify a bucket type upon write.
Here's what that would look like:

```ruby
bucket = client.bucket('nba_stats')
obj = Riak::RObject.new(bucket, 'michael_jordan')
obj.content_type = 'application/json'
obj.data = '{"stats":{ ... large stats object ... }}'
obj.store(w: 3, dw: 2)
```

```java
Location michaelJordanKey =
  new Location(new Namespace("nba_stats"), "michael_jordan");
RiakObject obj = new RiakObject()
        .setContentType("application/json")
        .setValue(BinaryValue.create("{'stats':{ ... large stats object ... }}"));
StoreValue store = new StoreValue.Builder(obj)
        .withLocation(michaelJordanKey)
        .withOption(StoreOption.W, new Quorum(3))
        .withOption(StoreOption.DW, new Quorum(2))
        .build();
client.execute(store);
```

```php
(new \Basho\Riak\Command\Builder\StoreObject($riak))
  ->buildJsonObject('{'stats':{ ... large stats object ... }}')
  ->buildLocation('john_stockton', 'nba_stats')
  ->withParameter('w', 3)
  ->withParameter('dw', 2)
  ->build()
  ->execute();
```

```erlang
Obj = riakc_obj:new(<<"nba_stats">>,
                    <<"michael_jordan">>,
                    <<"{'stats':{ ... large stats object ... }}">>,
                    <<"application/json">>),
riakc_pb_socket:put(Pid, Obj).
```

```curl
curl -XPUT \
  -H "Content-Type: application/json" \
  -d '{"stats":{ ... large stats object ... }}' \
  http://localhost:8098/buckets/nba_stats/keys/michael_jordan?w=3&dw=2
```

All of Basho's [official Riak clients]({{< product-version-root >}}reference/client-libraries/) enable you to
set replication properties this way. For more detailed information,
refer to the tutorial on [basic key/value operations in OpenRiak KV]({{< product-version-root >}}tutorials/first-application/)
or to client-specific documentation:

* [Ruby](https://github.com/basho/riak-ruby-client/blob/master/README.md)
* [Java](http://basho.github.io/riak-java-client/2.0.0/)
* [Python](http://basho.github.io/riak-python-client/)
* [Erlang](http://basho.github.io/riak-erlang-client/)

#### Illustrative Scenarios

In case the above explanations were a bit too abstract for your tastes,
the following table lays out a number of possible scenarios for reads
and writes in Riak and how Riak is likely to respond. Some of these
scenarios involve issues surrounding conflict resolution, vector clocks,
and siblings, so we recommend reading the [Vector Clocks]({{< product-version-root >}}foundations/data-model/causal-context/#vector-clocks) documentation for more information.

##### Read Scenarios

These scenarios assume that a read request is sent to all 3 primary
vnodes responsible for an object.

Scenario | What happens in Riak
:--------|:--------------------
All 3 vnodes agree on the value | Once the first 2 vnodes return the value, that value is returned to the client
2 of 3 vnodes agree on the value, and those 2 are the first to reach the coordinating node | The value is returned to the client. Read repair will deal with the conflict per the later scenarios, which means that a future read may return a different value or <a href="{{< product-version-root >}}foundations/data-model/causal-context/#siblings">siblings</a>
2 conflicting values reach the coordinating node and <a href="{{< product-version-root >}}foundations/data-model/causal-context/#vector-clocks">vector clocks</a> allow for resolution | The vector clocks are used to resolve the conflict and return a single value, which is propagated via read repair to the relevant vnodes
2 conflicting values reach the coordinating node, vector clocks indicate a fork in the object history, and `allow_mult` is set to `false` | The object with the most recent timestamp is returned and propagated via read repair to the relevant vnodes
2 siblings or conflicting values reach the coordinating node, vector clocks indicate a fork in the object history, and `allow_mult` is set to `true` | All keys are returned as siblings, optionally with associated values (depending on how the request is made)

###### Write Scenarios

These scenarios assume that a write request is sent to all 3 primary
vnodes responsible for an object.

Scenario | What happens in Riak
:--------|:--------------------
A vector clock is included with the write request, and is newer than the vclock attached to the existing object | The new value is written and success is indicated as soon as 2 vnodes acknowledge the write
A vector clock is included with the write request but conflicts with the vclock attached to the existing object, with `allow_mult` set to `true` | The new value is created as a sibling for future reads
A vector clock is included with the write request but conflicts with (or is older than) the vclock attached to the existing object, with `allow_mult` set to `false` | Riak will decide which object "wins" on the basis of timestamps; no sibling will be created
A vector clock is not included with the write request and an object already exists, with `allow_mult` set to `true` | The new value is created as a sibling for future reads
A vector clock is not included with the write request and an object already exists, with `allow_mult` set to `false` | The new value overwrites the existing value

#### Screencast

Here is a brief screencast that shows just how the N, R, and W values
function in our running 3-node OpenRiak cluster:

<div style="display:none" class="iframe-video"
id="http://player.vimeo.com/video/11172656"></div>

<a href="http://vimeo.com/11172656">Tuning CAP Controls in Riak</a> from
<a href="http://vimeo.com/bashotech">Basho Technologies</a> on <a
href="http://vimeo.com">Vimeo</a>.

### Replication

[cluster ops v3 mdc]: {{< product-version-root >}}reference/replication-api/runtime-controls/
[concept aae]: {{< product-version-root >}}foundations/replication/active-anti-entropy/
[concept causal context vc]: {{< product-version-root >}}foundations/data-model/causal-context/#vector-clocks
[concept clusters]: {{< product-version-root >}}foundations/foundations/clusters-rings-and-partitions/
[concept vnodes]: {{< product-version-root >}}foundations/foundations/virtual-nodes/
[glossary node]: {{< product-version-root >}}foundations/foundations/glossary/#node
[glossary ring]: {{< product-version-root >}}foundations/foundations/glossary/#ring
[usage replication]: {{< product-version-root >}}foundations/replication/

Data replication is a core feature of OpenRiak's basic architecture. Riak
was designed to operate as a [clustered][concept clusters] system containing
multiple Riak [nodes][glossary node], which allows data to live
on multiple machines at once in case a node in the cluster goes down.

Replication is fundamental and automatic in Riak, providing security
that your data will still be there if a node in your OpenRiak cluster goes
down. All data stored in Riak will be replicated to a number of nodes in
the cluster according to the N value (`n_val`) property set in a
bucket's [bucket type]({{< product-version-root >}}how-to/develop/use-bucket-types/).

>**Note: Replication across clusters**
>
>If you're interested in replication not just within a cluster but across
multiple clusters, we recommend checking out our documentation on OpenRiak's
[Multi-Datacenter Replications]({{< product-version-root >}}how-to/configure/replication/configure-v3-multi-datacenter/) capabilities.

#### Selecting an N value (`n_val`)

By default, Riak chooses an `n_val` of 3 default. This means that data
stored in any bucket will be replicated to 3 different nodes. For this
to be effective, you need at least 3 nodes in your cluster.

The ideal value for N depends largely on your application and the shape
of your data. If your data is highly transient and can be reconstructed
easily by the application, choosing a lower N value will provide greater
performance. However, if you need high assurance that data is available
even after node failure, increasing the N value will help protect
against loss. How many nodes do you expect will fail at any one time?
Choose an N value larger than that and your data will still be
accessible when they go down.

The N value also affects the behavior of read (GET) and write (PUT)
requests. The tunable parameters you can submit with requests are bound
by the N value. For example, if N=3, the maximum read quorum (known as
"R") you can request is also 3. If some nodes containing the data you
are requesting are down, an R value larger than the number of available
nodes with the data will cause the read to fail.

#### Setting the N value (`n_val`)

To change the N value for a bucket, you need to create a [bucket
type]({{< product-version-root >}}how-to/develop/use-bucket-types/) with `n_val` set to your desired value and
then make sure that the bucket bears that type.

In this example, we'll set N to 2. First, we'll create the bucket type
and call it `n_val_of_2` and then activate that type:

```bash
riak admin bucket-type create n_val_of_2 '{"props":{"n_val":2}}'
riak admin bucket-type activate n_val_of_2
```

Now, any bucket that bears the type `n_val_of_2` will propagate objects
to 2 nodes.

>**Note on changing the value of N**
>
>Changing the N value after a bucket has data in it is *not
recommended*. If you do change the value, especially if you
increase it, you might need to force read repair (more on that below).
Overwritten objects and newly stored objects will automatically be
replicated to the correct number of nodes.

#### Changing the N value (`n_val`)

While raising the value of N for a bucket or object shouldn't cause
problems, it's important that you never lower N. If you do so, you can
wind up with dead, i.e. unreachable data. This can happen because
objects' preflists, i.e. lists of [vnodes][concept vnodes] responsible for the object,
can end up

Unreachable data is a problem because it can negatively impact coverage
queries, e.g. [secondary index]({{< product-version-root >}}how-to/develop/query-secondary-indexes/) and
[MapReduce]({{< product-version-root >}}how-to/develop/run-mapreduce/) queries. Lowering an object or bucket's
`n_val` will likely mean that objects that you would expect to
be returned from those queries will no longer be returned.

#### Active Anti-Entropy

OpenRiak's active anti-entropy (AAE) subsystem is a continuous background
process that compares and repairs any divergent or missing object
replicas. For more information on AAE, see the following documents:

* [Active Anti-Entropy][concept aae]
* [Managing Active Anti-Entropy][cluster ops v3 mdc]

#### Read Repair

Read repair occurs when a successful read occurs---i.e. when the target
number of nodes have responded, as determined by R---but not all
replicas of the object agree on the value. There are two possibilities
here for the errant nodes:

1. The node responded with a `not found` for the object, meaning that
   it doesn't have a copy.
2. The node responded with a [vector clock][concept causal context vc] that is an
   ancestor of the vector clock of the successful read.

When this situation occurs, Riak will force the errant nodes to update
the object's value based on the value of the successful read.

##### Forcing Read Repair

When you increase the `n_val` of a bucket, you may start to see failed
read operations, especially if the R value you use is larger than the
number of replicas that originally stored the object. Forcing read
repair will solve this issue. Or if you have [active
anti-entropy][usage replication] enabled, your values will
eventually replicate as a background task.

For each object that fails read (or the whole bucket, if you like), read
the object using an R value less than or equal to the original number of
replicas. For example, if your original `n_val` was 3 and you increased
it to 5, perform your read operations with R=3 or less. This will cause
the nodes that do not have the object(s) yet to respond with `not
found`, invoking read repair.

#### So what does N=3 really mean?

N=3 simply means that three copies of each piece of data will be stored
in the cluster. That is, three different partitions/vnodes will receive
copies of the data. **There are no guarantees that the three replicas
will go to three separate physical nodes**; however, the built-in
functions for determining where replicas go attempts to distribute the
data evenly.

As nodes are added and removed from the cluster, the ownership of
partitions changes and may result in an uneven distribution of the data.
On some rare occasions, Riak will also aggressively reshuffle ownership
of the partitions to achieve a more even balance.

For cases where the number of nodes is less than the N value, data will
likely be duplicated on some nodes. For example, with N=3 and 2 nodes in
the cluster, one node will likely have one replica, and the other node
will have two replicas.

#### Understanding replication by example

To better understand how data is replicated in Riak let's take a look at
a put request for the bucket/key pair `my_bucket`/`my_key`. Specifically
we'll focus on two parts of the request: routing an object to a set of
partitions and storing an object on a partition.

##### Routing an object to a set of partitions

* Assume we have 3 nodes
  * Assume we store 3 replicas per object (N=3)
  * Assume we have 8 partitions in our [ring][glossary ring] \(ring_creation_size=8)

**Note**: It is not recommended that you use such a small ring size.
This is for demonstration purposes only.

With only 8 partitions our ring will look approximately as follows
(response from `riak_core_ring_manager:get_my_ring/0` truncated for
clarity):

```erlang
(dev1@127.0.0.1)3> {ok,Ring} = riak_core_ring_manager:get_my_ring().
[{0,'dev1@127.0.0.1'},
{182687704666362864775460604089535377456991567872, 'dev2@127.0.0.1'},
{365375409332725729550921208179070754913983135744, 'dev3@127.0.0.1'},
{548063113999088594326381812268606132370974703616, 'dev1@127.0.0.1'},
{730750818665451459101842416358141509827966271488, 'dev2@127.0.0.1'},
{913438523331814323877303020447676887284957839360, 'dev3@127.0.0.1'},
{1096126227998177188652763624537212264741949407232, 'dev1@127.0.0.1'},
{1278813932664540053428224228626747642198940975104, 'dev2@127.0.0.1'}]
```

The node handling this request hashes the bucket/key combination:

```erlang
(dev1@127.0.0.1)4> DocIdx = riak_core_util:chash_key({<<"my_bucket">>, <<"my_key">>}).
<<183,28,67,173,80,128,26,94,190,198,65,15,27,243,135,127,121,101,255,96>>
```

The DocIdx hash is a 160-bit integer:

```erlang
(dev1@127.0.0.1)5> <<I:160/integer>> = DocIdx.
<<183,28,67,173,80,128,26,94,190,198,65,15,27,243,135,127,121,101,255,96>>
(dev1@127.0.0.1)6> I.
1045375627425331784151332358177649483819648417632
```

The node looks up the hashed key in the ring, which returns a list of
_preferred_ partitions for the given key.

```erlang
(node1@127.0.0.1)> Preflist = riak_core_ring:preflist(DocIdx, Ring).
[{1096126227998177188652763624537212264741949407232, 'dev1@127.0.0.1'},
{1278813932664540053428224228626747642198940975104, 'dev2@127.0.0.1'},
{0, 'dev1@127.0.0.1'},
{182687704666362864775460604089535377456991567872, 'dev2@127.0.0.1'},
{365375409332725729550921208179070754913983135744, 'dev3@127.0.0.1'},
{548063113999088594326381812268606132370974703616, 'dev1@127.0.0.1'},
{730750818665451459101842416358141509827966271488, 'dev2@127.0.0.1'},
{913438523331814323877303020447676887284957839360, 'dev3@127.0.0.1'}]
```

The node chooses the first N partitions from the list. The remaining
partitions of the "preferred" list are retained as fallbacks to use if
any of the target partitions are unavailable.

```erlang
(dev1@127.0.0.1)9> {Targets, Fallbacks} = lists:split(N, Preflist).
{[{1096126227998177188652763624537212264741949407232, 'dev1@127.0.0.1'},
{1278813932664540053428224228626747642198940975104, 'dev2@127.0.0.1'},
{0,'dev1@127.0.0.1'}],
[{182687704666362864775460604089535377456991567872, 'dev2@127.0.0.1'},
{365375409332725729550921208179070754913983135744, 'dev3@127.0.0.1'},
{548063113999088594326381812268606132370974703616, 'dev1@127.0.0.1'},
{730750818665451459101842416358141509827966271488, 'dev2@127.0.0.1'},
{913438523331814323877303020447676887284957839360, 'dev3@127.0.0.1'}]}
```

The partition information returned from the ring contains a partition
identifier and the parent node of that partition:

```erlang
{1096126227998177188652763624537212264741949407232, 'dev1@127.0.0.1'}
```

The requesting node sends a message to each parent node with the object
and partition identifier (pseudocode for clarity):

```erlang
'dev1@127.0.0.1' ! {put, Object, 1096126227998177188652763624537212264741949407232}
'dev2@127.0.0.1' ! {put, Object, 1278813932664540053428224228626747642198940975104}
'dev1@127.0.0.1' ! {put, Object, 0}
```

If any of the target partitions fail, the node sends the object to one
of the fallbacks. When the message is sent to the fallback node, the
message references the object and original partition identifier. For
example, if `dev2@127.0.0.1` were unavailable, the requesting node would
then try each of the fallbacks. The fallbacks in this example are:

```erlang
{182687704666362864775460604089535377456991567872, 'dev2@127.0.0.1'}
{365375409332725729550921208179070754913983135744, 'dev3@127.0.0.1'}
{548063113999088594326381812268606132370974703616, 'dev1@127.0.0.1'}
```

The next available fallback node would be `dev3@127.0.0.1`. The
requesting node would send a message to the fallback node with the
object and original partition identifier:

```erlang
'dev3@127.0.0.1' ! {put, Object, 1278813932664540053428224228626747642198940975104}
```

Note that the partition identifier in the message is the same that was
originally sent to `dev2@127.0.0.1` only this time it is being sent to
`dev3@127.0.0.1`. Even though `dev3@127.0.0.1` is not the parent node of
that partition, it is smart enough to hold on to the object until
`dev2@127.0.0.1` returns to the cluster.

#### Processing partition requests

Processing requests per partition is fairly simple. Each node runs a
single process (`riak_kv_vnode_master`) that distributes requests to
individual partition processes (`riak_kv_vnode`). The
`riak_kv_vnode_master` process maintains a list of partition identifiers
and corresponding partition processes. If a process does not exist for a
given partition identifier a new process is spawned to manage that
partition.

The `riak_kv_vnode_master` process treats all requests the same and
spawns partition processes as needed even when nodes receive requests
for partitions they do not own. When a partition's parent node is
unavailable, requests are sent to fallback nodes (handoff). The
`riak_kv_vnode_master` process on the fallback node spawns a process to
manage the partition even though the partition does not belong to the
fallback node.

The individual partition processes perform hometests throughout the life
of the process. The hometest checks if the current node (`node/0`)
matches the parent node of the partition as defined in the ring. If the
process determines that the partition it is managing belongs on another
node (the parent node), it will attempt to contact that node. If that
parent node responds, the process will hand off any objects it has
processed for that partition and shut down. If that parent node does not
respond, the process will continue to manage that partition and check
the parent node again after a delay. The hometest is also run by
partition processes to account for changes in the ring, such as the
addition or removal of nodes to the cluster.

#### OpenRiak KV - Replication and Reconciliation

In the evolution of Riak, there have been two generations of solutions developed to support replication and reconciliation between clusters:

- The now legacy, [`riak_repl` replication]({{< product-version-root >}}foundations/replication/v2-and-v3-replication/) which was the recommended replication approach prior to Riak 3.0.10.
  - The `riak_repl` application has evolved through multiple versions of a real-time replication, that supported a push-based model to reliably deliver changes from a source cluster to a sink cluster;
  - The replication approach is backed-up by a reconciliation approach focused on time-consuming key-by-key comparisons, running in the background between clusters on a vnode-by-vnode basis.
- The NextGen replication solution which is the recommended approach in Riak 3.4.
  - The real-time replication approach is by comparison a pull-based model, to allow a sink cluster to fetch results from the source;
  - The replication approach is backed-up with reconciliation through rapid low-cost comparisons between the state of clusters using anti-entropy information, where the comparisons run reliably between clusters with different configurations (e.g. ring-size, node count or n_val).

This guide covers the NextGen replication solution, and further information on alternatives are linked from the [legacy replication section]({{< product-version-root >}}foundations/replication/v2-and-v3-replication/).

Replication is considered to have three stages:

- Seeding; populating data in one cluster from another cluster.
  - Not covered in this guide.
  - The recommended approach to seeding using `repl_keys_range` is explained as part of [the AAE Fold API guide]({{< product-version-root >}}reference/aae-fold-api/).
- **Real-time replication**; the forwarding of changes between connected clusters as they occur.
- **Reconciliation**; determining if two clusters have the same data at the same version, and automatically resolving any deltas that exist.

Real-time replication is asynchronous in Riak, the availability and performance of one cluster should have no impact on the clusters replicating to it.  With asynchronous replication, under-pinning the system with reconciliation is important to reduce the need for operator intervention.  Simple replication failures should not need to prompt operator activity, as the failure will eventually be automatically resolved.

> The speed and efficiency of inter-cluster reconciliation is a key feature of Riak.  It is normal in production systems to verify clusters are reconciled every few minutes, with the process taking less than 10s, even when clusters contain more than 10 billion objects.

The guide is split into the following sections:

- [An overview of the concepts]({{< product-version-root >}}foundations/replication/).
- [Configuration of real-time replication]({{< product-version-root >}}how-to/configure/replication/configure-real-time-replication/).
- [Configuration of all-cluster reconciliation]({{< product-version-root >}}how-to/configure/replication/configure-fullsync/).
- [Configuration of per-bucket reconciliation]({{< product-version-root >}}how-to/configure/replication/per-bucket-reconciliation/).
- [Managing a cluster migration]({{< product-version-root >}}how-to/configure/replication/migrate-cluster/).
- [The external Replication API]({{< product-version-root >}}reference/replication-api/).
- [Operations and the troubleshooting of replication]({{< product-version-root >}}how-to/operate/monitor-reconciliation/).
- [Configuring `riak_repl`]({{< product-version-root >}}foundations/replication/v2-and-v3-replication/).
- [Replication scope]({{< product-version-root >}}foundations/replication/reconciliation-scope/).

#### Overview

The Riak replication and reconciliation (full-sync) system has the following features:

- Allows for replication between clusters with different ring sizes, `n_val`s and node counts.
- Uses a pull model for real-time replication with low-cost queueing;
  - Support for low-impact suspension and resumption of replication,
  - Prevents recipient clusters from being overwhelmed by replicated PUT volumes.
- Provides very efficient reconciliation to confirm whole clusters are synchronised;
  - i.e. Confirmation that across multiple clusters all objects are at the same version.
- Efficient and fast resolution of small deltas between clusters;
  - With a specific focus on accelerating the recovery of recently occurring deltas (e.g. following a failure or real-time replication).
- Uses an API which is reusable for replication to and reconciliation with non-Riak databases.

The replication and reconciliation system works with these caveats:

- Reconciliation checks alone are slow to resolve very large deltas between clusters;
  - Partial re-seeding may be prompted where deltas are large, to accelerate the process.
- No support for complex replication topologies with loop prevention;
  - Every peer relationship between clusters must be formed directly.
- When not used exclusively with a leveled backend, a parallel keystore is required (which is shared with internal anti-entropy).

In Riak, replication and reconciliation are designed to be complementary processes.  Although it is possible to configure replication without reconciliation, and vice versa, it is assumed that normally both replication and reconciliation will be active concurrently.

Within the replication system, for any replication event, there is a **source** and a **sink**.  The source is the cluster which has an update of interest to another cluster, and the sink is a system that attempts to fetch a replication event from that cluster.

Replication and reconciliation is built on the following support infrastructure:

- [Queues and workers]({{< product-version-root >}}foundations/replication/queues/);
- [Replication references]({{< product-version-root >}}foundations/replication/references-and-triggers/);
- [Replication triggers]({{< product-version-root >}}foundations/replication/references-and-triggers/).

## In this section

- [Accelerated large-delta reconciliation]({{< product-version-root >}}foundations/replication/accelerated-reconciliation/) — Explain how {{< current-version >}} accelerates large replication-delta repair without resending an entire bucket.
- [Active anti-entropy]({{< product-version-root >}}foundations/replication/active-anti-entropy/) — Explain active anti-entropy, its data flow, failure behavior, and operational trade-offs.
- [Cascading replication writes]({{< product-version-root >}}foundations/replication/cascading-writes/) — Explain cascading replication writes, its data flow, failure behavior, and operational trade-offs.
- [Legacy active anti-entropy]({{< product-version-root >}}foundations/replication/legacy-aae/) — Explain legacy active anti-entropy, its data flow, failure behavior, and operational trade-offs.
- [Multi-datacenter replication architecture]({{< product-version-root >}}foundations/replication/multi-datacenter-architecture/) — Explain multi-datacenter replication architecture, its data flow, failure behavior, and operational trade-offs.
- [Next-generation replication]({{< product-version-root >}}foundations/replication/next-generation-replication/) — Explain next-generation replication, its data flow, failure behavior, and operational trade-offs.
- [Replication queues]({{< product-version-root >}}foundations/replication/queues/) — Explain replication queues, its data flow, failure behavior, and operational trade-offs.
- [Real-time and Fullsync replication]({{< product-version-root >}}foundations/replication/real-time-and-fullsync/) — Explain real-time and fullsync replication, its data flow, failure behavior, and operational trade-offs.
- [Reconciliation scope]({{< product-version-root >}}foundations/replication/reconciliation-scope/) — Explain all-cluster, per-bucket, time-window, and key-range reconciliation trade-offs.
- [Replication references and triggers]({{< product-version-root >}}foundations/replication/references-and-triggers/) — Explain how replication references and triggers select, queue, and transmit changes.
- [Replication sink nodes]({{< product-version-root >}}foundations/replication/sink-nodes/) — Explain replication sink nodes, its data flow, failure behavior, and operational trade-offs.
- [TicTac active anti-entropy]({{< product-version-root >}}foundations/replication/tictac-aae/) — Explain tictac active anti-entropy, its data flow, failure behavior, and operational trade-offs.
- [Legacy and current replication generations]({{< product-version-root >}}foundations/replication/v2-and-v3-replication/) — Explain legacy and current replication generations, its data flow, failure behavior, and operational trade-offs.
