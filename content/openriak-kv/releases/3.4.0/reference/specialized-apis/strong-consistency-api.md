---
title: 'Strong Consistency API reference'
description: 'Define strongly consistent operations, request fields, responses, constraints, and errors.'
weight: 4
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\app-guide\strong-consistency.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\strong-consistency.md'
source_material:
  - 'legacy-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#strong-consistency-api'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define strongly consistent operations, request fields, responses, constraints, and errors.

## Details

### Strong Consistency

[use ref strong consistency]: {{< product-version-root >}}reference/specialized-apis/strong-consistency-api/
[concept eventual consistency]: {{< product-version-root >}}explanation/consistency/eventual-consistency/
[use ref strong consistency#trade-offs]: {{< product-version-root >}}reference/specialized-apis/strong-consistency-api/#trade-offs
[glossary vnode]: {{< product-version-root >}}explanation/foundations/glossary/#vnode
[config strong consistency#enable]: {{< product-version-root >}}how-to/configure/strong-consistency/#enabling-strong-consistency
[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[cluster ops bucket types]: {{< product-version-root >}}how-to/operate/manage-bucket-types/
[apps replication properties]: {{< product-version-root >}}explanation/replication/references-and-triggers/
[config strong consistency]: {{< product-version-root >}}how-to/configure/strong-consistency/
[config strong consistency#fault]: {{< product-version-root >}}how-to/configure/strong-consistency/#fault-tolerance
[concept causal context]: {{< product-version-root >}}explanation/data-model/causal-context/
[concept causal context#vector]: {{< product-version-root >}}explanation/data-model/causal-context/#vector-clocks
[concept version vector]: {{< product-version-root >}}explanation/data-model/causal-context/#dotted-version-vectors
[usage conflict resolution]: {{< product-version-root >}}how-to/develop/resolve-conflicts/
[usage update objects]: {{< product-version-root >}}how-to/develop/update-object/
[use ref strong consistency#vs]: {{< product-version-root >}}reference/specialized-apis/strong-consistency-api/
[dev client libraries]: {{< product-version-root >}}reference/client-libraries/
[getting started]: {{< product-version-root >}}tutorials/first-application/
[config strong consistency#details]: {{< product-version-root >}}how-to/configure/strong-consistency/#implementation-details

> **Please Note:**
>
> OpenRiak KV's strong consistency is an experimental feature and may be removed from the product in the future. Strong consistency is not commercially supported or production-ready. Strong consistency is incompatible with Multi-Datacenter Replication, Riak Search, Bitcask Expiration, LevelDB Secondary Indexes, Riak Data Types and Commit Hooks. We do not recommend its usage in any production environment.

In versions 2.0 and later, Riak allows you to create buckets that
provide [strong consistency][use ref strong consistency] guarantees for the data stored within
them, enabling you to use Riak as a CP system (consistent plus partition
tolerant) for all of the data in that bucket. You can store just some of
your data in strongly consistent buckets or all of your data, depending
on your use case. Strong consistency was added to complement OpenRiak's
standard [eventually consistent][concept eventual consistency], high
availability mode.

#### Tradeoffs

When data is stored in a bucket with strong consistency guarantees, a
value is guaranteed readable by any client _immediately_ after a
successful write has occurred to a given key. In this sense, single-key
strongly consistent operations are atomic, and operations on a given key
are [linearizable](http://en.wikipedia.org/wiki/Linearizability). This
behavior comes at the expense of availability because a [quorum][use ref strong consistency#trade-offs] of primary [vnodes][glossary vnode] responsible for the key must be online and reachable or the request will
fail.

This trade-off is unavoidable for strongly consistent data, but the
[choice is now yours](http://en.wikipedia.org/wiki/CAP_theorem) to make.

#### Enabling Strong Consistency

Complete instructions on enabling strong consistency can be found in
our documentation on [configuring strong consistency][config strong consistency#enable].

#### Creating Consistent Bucket Types

[Strong Consistency][use ref strong consistency] requirements in Riak are applied on a bucket-by-bucket basis, meaning that you can use some buckets in an eventually consistent fashion and others in a strongly consistent
fashion, depending on your use case.

To apply strong consistency to a bucket, you must create a [bucket type][usage bucket types] that sets the `consistent` bucket property to
`true`, activate that type, and then apply that type to specific
bucket/key pairs.

To give an example, we'll create a bucket type called
`strongly_consistent` with the `consistent` bucket property set to
`true`:

```bash
riak admin bucket-type create strongly_consistent \
    '{"props":{"consistent":true}}'
```

> **Note on bucket type names**
>
> You can name [bucket types][usage bucket types] whatever you wish, with
the exception of `default`, which is a reserved term (a full listing of
the properties associated with the `default` bucket type can be found in
the documentation on [bucket properties and operations][cluster ops bucket types]).

Once the `strongly_consistent` bucket type has been created, we can
check the status of the type to ensure that it has propagated through
all nodes and is thus ready to be activated:

```bash
riak admin bucket-type status strongly_consistent
```

If the console outputs `strongly_consistent has been created and may be
activated` and the properties listing shows that `consistent` has been
set to `true`, then you may proceed with activation:

```bash
riak admin bucket-type activate strongly_consistent
```

When activation is successful, the console will return the following:

```bash
strongly_consistent has been activated
```

Now, any bucket that bears the type `strongly_consistent`---or whatever
you wish to name it---will provide strong consistency guarantees.

Elsewhere in the Riak docs, you can find more information on [using bucket types][usage bucket types], on the concept of [strong consistency][use ref strong consistency], and on strong
consistency [for operators][config strong consistency].

#### Replication Properties

Strongly consistent operations in Riak function much differently from
their [eventually consistent][concept eventual consistency] counterparts.
Whereas eventually consistent operations enable you to set values for a
variety of [replication properties][apps replication properties] either on each request or at the
bucket level, [using bucket types][usage bucket types], these settings are quietly ignored
for strongly consistent operations. These settings include `r`, `pr`,
`w`, `rw`, and others. Two replication properties that _can_ be set,
however, are `n_val` and `return_body`.

The `n_val` property is extremely important for two reasons:

1. It dictates how fault tolerant a strongly consistent bucket is. More
   information can be found in [our recommendations for operators][config strong consistency#fault].
2. Once the `n_val` property is set for a given bucket type, it cannot
   be changed. If you wish to change the `n_val` for one or more
   strongly consistent buckets [using bucket types][usage bucket types], you will need to
   create a new bucket type with the desired `n_val`.

We also recommend setting the `n_val` on strongly consistent buckets to
at least 5. More on why we make this recommendation can be found in
[Fault Tolerance][config strong consistency#fault].

#### Causal Context

Riak uses [causal context][concept causal context] to determine the causal history of objects.
In versions of OpenRiak KV prior to 2.0, [vector clocks][concept causal context#vector] were used to provide objects with causal context
metadata. In Riak versions 2.0 and later there is an option to use
[dotted version vectors][concept version vector], which function much like vector clocks from
the standpoint of clients, but with important advantages over vector
clocks.

While we strongly recommend attaching context to objects for all
updates---whether traditional vector clocks or the newer dotted version
vectors---they are purely [optional][usage conflict resolution] for all
eventually consistent operations in Riak. This is not the case for
strongly consistent operations. **When modifying strongly consistent
objects in Riak, you _must_ attach a causal context**.

If you attempt to modify a strongly consistent object without attaching
a context to the request, the request will always fail. And while it is
possible to make writes to non-existing keys without attaching context,
we recommend doing this only if you are certain that the key does not
yet exist.

Instructions on using causal context can be found in our documentation
on [object updates][usage update objects].

#### Strongly Consistent Writes

Writing to strongly consistent keys involves some of the same best
practices that we advise when writing to eventually consistent keys. We
recommend bearing the following in mind:

1. If you _know_ that a key does not yet exist, you can write to that
   key without supplying a context with the object. If you are unsure, then you should default to supplying a context object.
2. If an object already exists under a key, strong consistency demands
   that you supply a [causal context](#causal-context). If you do not supply one, the update
   will necessarily fail.
3. Because strongly consistent writes must occasionally
   [sacrifice availability][use ref strong consistency#vs] for the sake of
   consistency, **strongly consistent updates can fail even under normal
   conditions**, particularly in the event of concurrent updates.

#### Error Messages

For the most part, performing reads, writes, and deletes on data in
strongly consistent buckets works much like it does in
non-strongly-consistent-buckets. One important exception to this is how
writes are performed. Strongly consistent buckets cannot allow siblings
by definition, and so all writes to existing keys must include a context
with the object.

If you attempt a write to a non-empty key without including causal
context, you will receive the following error:

```ruby
Riak::Conflict: The object is in conflict (has siblings) and cannot be treated singly or saved:
```

```java
java.lang.IllegalArgumentException: VClock cannot be null.
```

```php
$response->isSuccess();  // false
$response->getStatusCode(); // 412
```

```python
riak.RiakError: 'failed'
```

```erlang
{error,<<"failed">>}
```

```curl
<html><head><title>412 Precondition Failed</title></head><body><h1>Precondition Failed</h1>Precondition Failed<p><hr><address>mochiweb+webmachine web server</address></body></html>
```

> **Getting Started with OpenRiak KV clients**
>
> If you are connecting to Riak using one of Basho's official
[client libraries][dev client libraries], you can find more information about getting started with your client in our [Developing with OpenRiak KV: Getting Started][getting started] section.

#### Known Issue with Client Libraries

All of Basho's official [client libraries][dev client libraries] currently convert errors returned by Riak into generic exceptions, with a message derived from the error message returned by Riak. In many cases this presents no
problems, since many error conditions are normal when using Riak.

When working with strong consistency, however, operations like
[conditional puts][config strong consistency#details] commonly
produce errors that are difficult for clients to interpret. For example,
it is expected behavior for conditional puts to fail in the case of
concurrent updates to an object. At present, the official Riak clients
will convert this failure into an exception that is no different from
other error conditions, i.e. they will not indicate any
strong-consistency-specific errors.

The best solution to this problem at the moment is to catch these
exceptions on the application side and parse server-side error messages
to see if the error involved a conditional failure. If so, you should
set up your application to retry any updates, perhaps a specified number
of times or perhaps indefinitely, depending on the use case.

If you do set up a retry logic of this sort, however, it is necessary
to retry the entire read/modify/put cycle, meaning that you will need
to fetch the object, modify it, and then write. If you perform a simple
put over and over again, without reading the object, the update will
continue to fail.

A future version of Riak will address these issues by modifying the
server API to more accurately report errors specific to strongly
consistent operations.

### Strong Consistency Reference

[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[concept eventual consistency]: {{< product-version-root >}}explanation/consistency/eventual-consistency/

Riak was originally designed as an [eventually consistent]({{< product-version-root >}}explanation/consistency/eventual-consistency/) system, fundamentally geared toward providing partition
(i.e. fault) tolerance and high read and write availability.

While this focus on high availability is a great fit for many data
storage needs, there are also many use cases for which strong data
consistency is more important than availability. Basho introduced a new
strong consistency option in version 2.0 to address these use cases.
In Riak, strong consistency is applied [using bucket types][usage bucket types], which
enables developers to apply strong consistency guarantees on a per-key
basis.

Elsewhere in the documentation there are instructions for [enabling and using]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/) strong consistency, as well as a [guide for operators]({{< product-version-root >}}how-to/configure/strong-consistency/) looking to manage,
configure, and monitor strong consistency.

#### Strong vs. Eventual Consistency

If you successfully write a value to a key in a strongly consistent
system, the next successful read of that key is guaranteed to show that
write. A client will never see out-of-date values. The drawback is that
some operations may fail if an insufficient number of object replicas
are available. More on this in the section on [trade-offs](#trade-offs).

In an eventually consistent system, on the other hand, a read may return
an out-of-date value, particularly during system or network failures.
The advantage of this approach is that reads and writes can succeed even
when a cluster is experiencing significant service degradation.

##### Example

Building on the example presented in the [eventual consistency][concept eventual consistency] doc,
imagine that information about who manages Manchester United is stored
in Riak, in the key `manchester-manager`. In the eventual consistency
example, the value associated with this key was originally
`David Moyes`, meaning that that was the first successful write to that
key. But then `Louis van Gaal` became Man U's manager, and a write was
executed to change the value of `manchester-manager`.

Now imagine that this write failed on one node in a multi-node cluster.
Thus, all nodes report that the value of `manchester-manager` is `Louis
van Gaal` except for one. On the errant node, the value of the
`manchester-manager` key is still `David Moyes`. An eventually
consistent system is one in which a get request will most likely return
`Louis van Gaal` but could return the outdated value `David Moyes`.

In a strongly consistent system, conversely, any successful read on
`manchester-manager` will return `Louis van Gaal` and never `David Moyes`.
Reads will return `Louis van Gaal` every single time until Man U gets a new
manager and someone performs a successful write to `manchester-manager`
to change its value.

It might also be useful to imagine it a bit more abstractly. The
following causal sequence would characterize a strongly consistent
system:

1. The value of the key `k` is set to `v`
2. All successful reads on `k` return `v`
3. The value of `k` is changed to `v2`
4. All successful reads on `k` return `v2`
5. And so forth

At no point in time does this system return an out-of-date value.

The following sequence could characterize an eventually consistent
system:

1. A write is made that sets the value of the key `k` to `v`
2. Nearly all reads to `k` return `v`, but a small percentage return
   `not found`
3. A write to `k` changes the value to `v2`
4. Nearly all reads to `k` now return `v2`, but a small number return
   the outdated `v` (or even `not found`) because the newer value hasn't
   yet been replicated to all nodes

#### Making the Strong vs. Eventual Decision

The first system described above may sound like the undisputed champion,
and the second system undesirable. However:

1. Reads and writes on the first system will often be slower---if only
   by a few milliseconds---because the system needs to manage reads and
   writes more carefully. If performance is of primary concern, the
   first system might not be worth the sacrifice.
2. Reads and writes on the first system may fail entirely if enough
   servers are unavailable. If high availability is the top priority,
   then the second system has a significant advantage.

So when deciding whether to use strong consistency in Riak, the
following question needs to be asked:

##### For the specific use case at hand, is it better for reads to fail than to return a potentially out-of-date value?

If the answer is yes, then you should seriously consider using Riak in a
strongly consistent way for the data that demands it, while bearing in
mind that other data can still be stored in Riak in an eventually
consistent way.

#### Trade-offs

Using Riak in a strongly consistent fashion comes with two unavoidable
trade-offs:

1. Less availability
2. Slightly slower performance

Strongly consistent operations are necessarily less highly available
than eventually consistent operations because they require a **quorum**
of available object replicas to succeed. Quorum is defined as N / 2 + 1,
or `n_val` / 2 + 1. If N is set to 7, at least 4 object replicas must be
available, 2 must be available if N=3, etc.

If there is a network partition that leaves less than a quorum of object
replicas available within an ensemble, strongly consistent operations
against the keys managed by that ensemble will fail.

Nonetheless, consistent operations do provide a great deal of fault
tolerance. Consistent operations can still succeed when a minority of
replicas in each ensemble can be offline, faulty, or unreachable. In
other words, **strongly consistent operations will succeed as long as
quorum is maintained**. A fuller discussion can be found in the
[operations]({{< product-version-root >}}how-to/configure/strong-consistency/#fault-tolerance)
documentation.

A second trade-off regards performance. OpenRiak's implementation of strong
consistency involves a complex [consensus subsystem]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/) that typically requires more communication between Riak nodes than eventually consistent operations,
which can entail a performance hit of varying proportions, depending on
a variety of factors.

Ways to address this issue can be found in [strong consistency and performance]({{< product-version-root >}}how-to/configure/strong-consistency/#performance).

#### Strong Consistency API

The use of the strong consistency API is deprecated in Riak 3.4, and the API will be retired in Riak 4.0.

From Riak 4.0, Riak will only have support for eventual consistency, but protection for conflicts can be improved through [conditional PUTs with token-based consensus]({{< product-version-root >}}reference/http-api/conditional-requests/).

The functionality of Strong Consistency is unchanged since Riak 2.2.3, so refer to the [legacy documentation](https://docs.riak.com/riak/kv/2.2.3/developing/app-guide/strong-consistency/index.html) for further information.
