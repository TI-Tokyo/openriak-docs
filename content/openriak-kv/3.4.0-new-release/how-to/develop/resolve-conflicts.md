---
title: 'Resolve object conflicts'
description: 'Show developers how to resolve object conflicts with a minimal verified example.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\csharp.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\golang.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\java.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\nodejs.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\php.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\python.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\developing\usage\conflict-resolution\ruby.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show developers how to resolve object conflicts with a minimal verified example.

## Before you begin

A non-production OpenRiak KV cluster, client credentials, and disposable test data that represents the operation you need to implement.

## Overview

### Conflict Resolution

[usage bucket types]: {{< product-version-root >}}how-to/develop/use-bucket-types/
[use ref strong consistency]: {{< product-version-root >}}reference/specialized-apis/strong-consistency-api/

One of OpenRiak's [central goals]({{< product-version-root >}}foundations/foundations/why-openriak/) is high availability. It was built as a [clustered]({{< product-version-root >}}foundations/foundations/clusters-rings-and-partitions/) system in which any [node]({{< product-version-root >}}foundations/foundations/glossary/#node) is capable of receiving requests without requiring that
every node participate in each request.

If you are using Riak in an [eventually consistent]({{< product-version-root >}}foundations/consistency/eventual-consistency/) way, conflicts between object values on different nodes is
unavoidable. Often, Riak can resolve these conflicts on its own
internally if you use causal context, i.e. [vector clocks]({{< product-version-root >}}foundations/data-model/causal-context/#vector-clocks) or [dotted version vectors]({{< product-version-root >}}foundations/data-model/causal-context/#dotted-version-vectors), when updating objects. Instructions on this can be found in the section [below](#siblings).

**Important note on terminology**
In versions of Riak prior to 2.0, vector clocks were the only causal context
mechanism available in Riak, which changed with the introduction of dotted
version vectors in 2.0. Please note that you may frequent find terminology in
client library APIs, internal Basho documentation, and more that uses the term
"vector clock" interchangeably with causal context in general. OpenRiak's HTTP API
still uses a `X-Riak-Vclock` header, for example, even if you are using dotted
version vectors.

But even when you use causal context, Riak cannot always decide which
value is most causally recent, especially in cases involving concurrent
updates to an object. So how does Riak behave when it can't decide on a
single most-up-to-date value? **That is your choice**. A full listing of
available options can be found in the [section below]({{< product-version-root >}}how-to/develop/resolve-conflicts/). For now,
though, please bear in mind that we strongly recommend one of the
following two options:

1. If your data can be modeled as one of the currently available [Riak
   Data Types]({{< product-version-root >}}reference/data/distributed-data-types/), we recommend using one of these types,
   because all of them have conflict resolution _built in_, completely
   relieving applications of the need to engage in conflict resolution.
2. If your data cannot be modeled as one of the available Data Types,
   we recommend allowing Riak to generate [siblings](#siblings) and to design your application to resolve
   conflicts in a way that fits your use case. Developing your own
   **conflict resolution strategy** can be tricky, but it has clear
   advantages over other approaches.

Because Riak allows for a mixed approach when storing and managing data,
you can apply multiple conflict resolution strategies within a cluster.

> **Note on strong consistency**
>
> In versions of Riak 2.0 and later, you have the option of using Riak in
a strongly consistent fashion. This document pertains to usage of Riak
as an _eventually_ consistent system. If you'd like to use OpenRiak's
strong consistency feature, please refer to the following documents:
>
> * [Using Strong Consistency]({{< product-version-root >}}reference/specialized-apis/strong-consistency-api/) - A guide for developers
> * [Managing Strong Consistency]({{< product-version-root >}}how-to/configure/strong-consistency/) - A guide for operators
> * [strong consistency][use ref strong consistency] - A more theoretical explication of strong
  consistency

#### Client- and Server-side Conflict Resolution

OpenRiak's eventual consistency model is powerful because Riak is
fundamentally non-opinionated about how data resolution takes place.
While Riak _does_ have a set of [defaults]({{< product-version-root >}}foundations/replication/references-and-triggers/#available-parameters), there are a variety of general
approaches to conflict resolution that are available. In Riak, you can
mix and match conflict resolution strategies at the bucket level,
[using bucket types][usage bucket types]. The most important [bucket properties]({{< product-version-root >}}foundations/data-model/keys-objects-and-buckets/)
to consider when reasoning about conflict resolution are the
`allow_mult` and `last_write_wins` properties.

These properties provide you with the following basic options:

##### Timestamp-based Resolution

If the [`allow_mult`](#siblings) parameter is set to
`false`, Riak resolves all object replica conflicts internally and does
not return siblings to the client. How Riak resolves those conflicts
depends on the value that you set for a different bucket property,
[`last_write_wins`]({{< product-version-root >}}foundations/data-model/keys-objects-and-buckets/). If `last_write_wins` is set to `false`,
Riak will resolve all conflicts on the basis of
[timestamps](http://en.wikipedia.org/wiki/Timestamp), which are
attached to all Riak objects as metadata.

The problem with timestamps is that they are not a reliable resolution
mechanism in distributed systems, and they always bear the risk of data
loss. A better yet still-problematic option is to adopt a
last-write-wins strategy, described directly below.

###### Last-write-wins

Another way to manage conflicts is to set `allow_mult` to `false`, as
with timestamp-based resolution, while also setting the
`last_write_wins` parameter to
`true`. This produces a so-called last-write-wins (LWW) strategy whereby
Riak foregoes the use of all internal conflict resolution strategies
when making writes, effectively disregarding all previous writes.

The problem with LWW is that it will necessarily drop some writes in the
case of concurrent updates in the name of preventing sibling creation.
If your use case requires that your application be able to reason about
differing values produced in the case of concurrent updates, then we
advise against LWW as a general conflict resolution strategy.

However, LWW can be useful---and safe---if you are certain that there
will be no concurrent updates. If you are storing immutable data in
which each object is guaranteed to have its own key or engaging in
operations related to bulk loading, you should consider LWW.

**Undefined behavior warning**
Setting both `allow_mult` and `last_write_wins` to `true` necessarily leads to
unpredictable behavior and should always be avoided.

###### Resolve Conflicts on the Application Side

While setting `allow_mult` to `false` unburdens applications from having
to reason about siblings, delegating that responsibility to Riak itself,
it bears all of the drawbacks explained above. On the other hand,
setting `allow_mult` to `true` has the following benefits:

* Riak will retain writes even in the case of concurrent updates to a
  key, which enables you to capture the benefits of high availability
  with a far lower risk of data loss
* If your application encounters siblings, it can apply its own
  use-case-specific conflict resolution logic

Conflict resolution in Riak can be a complex business, but the presence
of this variety of options means that requests to Riak can always be
made in accordance with your data model(s), business needs, and use
cases. For examples of client-side sibling resolution, see the following
client-library-specific docs:

* [Java]({{< product-version-root >}}how-to/develop/resolve-conflicts/)
* [Ruby]({{< product-version-root >}}how-to/develop/resolve-conflicts/)
* [Python]({{< product-version-root >}}how-to/develop/resolve-conflicts/)
* [C#]({{< product-version-root >}}how-to/develop/resolve-conflicts/)
* [Node.js]({{< product-version-root >}}how-to/develop/resolve-conflicts/)

In Riak versions 2.0 and later, `allow_mult` is set to `true` by default
for any [bucket types]({{< product-version-root >}}how-to/develop/use-bucket-types/) that you create. This means
that if you wish to avoid client-side sibling resolution, you have a few
options:

* Explicitly create and activate [bucket types]({{< product-version-root >}}how-to/develop/use-bucket-types/)
  that set `allow_mult` to `false`
* Use OpenRiak's [Configuration Files]({{< product-version-root >}}reference/configuration/) to change the [default bucket properties]({{< product-version-root >}}reference/configuration/#default-bucket-properties) for your
  cluster. If you set the `buckets.default.allow_mult` parameter to
  `false`, all bucket types that you create will have `allow_mult` set
  to `false` by default.

##### Causal Context

When a value is stored in Riak, it is tagged with a piece of metadata
called a **causal context** which establishes the object's initial
version. Causal context comes in one of two possible forms, depending
on what value you set for `dvv_enabled`. If set to `true`, [dotted version vectors]({{< product-version-root >}}foundations/data-model/causal-context/#dotted-version-vectors) will be used; if set to `false` (the default), [vector clocks]({{< product-version-root >}}foundations/data-model/causal-context/#vector-clocks) will be used.

Causal context essentially enables Riak to compare the different values
of objects stored in Riak and to determine a number of important things
about those values:

* Whether one value is a direct descendant of the other
 * Whether the values are direct descendants of a common parent
 * Whether the values are unrelated in recent heritage

Using the information provided by causal context, Riak is frequently,
though not always, able to resolve conflicts between values without
producing siblings.

Both vector clocks and dotted version vectors are non human readable and
look something like this:

```
a85hYGBgzGDKBVIcR4M2cgczH7HPYEpkzGNlsP/VfYYvCwA=
```

If `allow_mult` is set to `true`, you should _always_ use causal context
when updating objects, _unless you are certain that no object exists
under that key_. Failing to use causal context with mutable data,
especially for objects that are frequently updated, can lead to
[sibling explosion]({{< product-version-root >}}how-to/tune/reduce-latency/#siblings), which can
produce a variety of problems in your cluster. Fortunately, much of the
work involved with using causal context is handled automatically by
Basho's official [client libraries]({{< product-version-root >}}reference/client-libraries/). Examples can be found for each
client library in the [Object Updates]({{< product-version-root >}}how-to/develop/update-object/) document.

##### Siblings

A **sibling** is created when Riak is unable to resolve the canonical
version of an object being stored, i.e. when Riak is presented with
multiple possible values for an object and can't figure out which one is
most causally recent. The following scenarios can create sibling values
inside of a single object:

1. **Concurrent writes** - If two writes occur simultaneously from
clients, Riak may not be able to choose a single value to store, in
which case the object will be given a sibling. These writes could happen
on the same node or on different nodes.
2. **Stale causal context** - Writes from any client using a stale
[causal context]({{< product-version-root >}}foundations/data-model/causal-context/). This is a less likely scenario if a client updates
the object by reading the object first, fetching the causal context
currently attached to the object, and then returning that causal context
to Riak when performing the update (fortunately, our client libraries
handle much of this automatically). However, even if a client follows
this protocol when performing updates, a situation may occur in which an
update happens from a different client while the read/write cycle is
taking place. This may cause the first client to issue the write with an
old causal context value and for a sibling to be created. A client is
"misbehaved" if it habitually updates objects with a stale or no context
object.
3. **Missing causal context** - If an object is updated with no causal
context attached, siblings are very likely to be created. This is an
unlikely scenario if you're using a Basho client library, but it _can_
happen if you are manipulating objects using a client like `curl` and
forgetting to set the `X-Riak-Vclock` header.

##### Siblings in Action

Let's have a more concrete look at how siblings work in Riak. First,
we'll create a bucket type called `siblings_allowed` with `allow_mult`
set to `true`:

```bash
riak admin bucket-type create siblings_allowed '{"props":{"allow_mult":true}}'
riak admin bucket-type activate siblings_allowed
riak admin bucket-type status siblings_allowed
```

If the type has been activated, running the `status` command should
return `siblings_allowed is active`. Now, we'll create two objects and
write both of them to the same key without first fetching the object
(which obtains the causal context):

```java
Location bestCharacterKey =
  new Location(new Namespace("siblings_allowed", "nickolodeon"), "best_character");

RiakObject obj1 = new RiakObject()
        .withContentType("text/plain")
        .withValue(BinaryValue.create("Ren"));
RiakObject obj2 = new RiakObject()
        .withContentType("text/plain")
        .withValue(BinaryValue.create("Stimpy"));
StoreValue store1 = new StoreValue.Builder(obj1)
        .withLocation(bestCharacterKey)
        .build();
StoreValue store2 = new StoreValue.Builder(obj2)
        .withLocation(bestCharacterKey)
        .build();
client.execute(store1);
client.execute(store2);
```

```ruby
bucket = client.bucket_type('siblings_allowed').bucket('nickolodeon')
obj1 = Riak::RObject.new(bucket, 'best_character')
obj1.content_type = 'text/plain'
obj1.raw_data = 'Ren'
obj1.store

obj2 = Riak::RObject.new(bucket, 'best_character')
obj2.content_type = 'text/plain'
obj2.raw_data = 'Stimpy'
obj2.store
```

```python
bucket = client.bucket_type('siblings_allowed').bucket('nickolodeon')
obj1 = RiakObject(client, bucket, 'best_character')
obj1.content_type = 'text/plain'
obj1.data = 'Ren'
obj1.store()

obj2 = RiakObject(client, bucket, 'best_character')
obj2.content_type = 'text/plain'
obj2.data = 'Stimpy'
obj2.store()
```

```csharp
var id = new RiakObjectId("siblings_allowed", "nickolodeon", "best_character");

var renObj = new RiakObject(id, "Ren", RiakConstants.ContentTypes.TextPlain);
var stimpyObj = new RiakObject(id, "Stimpy", RiakConstants.ContentTypes.TextPlain);

var renResult = client.Put(renObj);
var stimpyResult = client.Put(stimpyObj);
```

```javascript
var obj1 = new Riak.Commands.KV.RiakObject();
obj1.setContentType('text/plain');
obj1.setBucketType('siblings_allowed');
obj1.setBucket('nickolodeon');
obj1.setKey('best_character');
obj1.setValue('Ren');

var obj2 = new Riak.Commands.KV.RiakObject();
obj2.setContentType('text/plain');
obj2.setBucketType('siblings_allowed');
obj2.setBucket('nickolodeon');
obj2.setKey('best_character');
obj2.setValue('Ren');

var storeFuncs = [];
[obj1, obj2].forEach(function (obj) {
    storeFuncs.push(
        function (async_cb) {
            client.storeValue({ value: obj }, function (err, rslt) {
                async_cb(err, rslt);
            });
        }
    );
});

async.parallel(storeFuncs, function (err, rslts) {
    if (err) {
        throw new Error(err);
    }
});
```

```erlang
Obj1 = riakc_obj:new({<<"siblings_allowed">>, <<"nickolodeon">>},
                     <<"best_character">>,
                     <<"Ren">>,
                     <<"text/plain">>),
Obj2 = riakc_obj:new({<<"siblings_allowed">>, <<"nickolodeon">>},
                     <<"best_character">>,
                     <<"Stimpy">>,
                     <<"text/plain">>),
riakc_pb_socket:put(Pid, Obj1),
riakc_pb_socket:put(Pid, Obj2).
```

```curl
curl -XPUT http://localhost:8098/types/siblings_allowed/nickolodeon/whatever/keys/best_character \
  -H "Content-Type: text/plain" \
  -d "Ren"

curl -XPUT http://localhost:8098/types/siblings_allowed/nickolodeon/whatever/keys/best_character \
  -H "Content-Type: text/plain" \
  -d "Stimpy"
```

> **Getting started with OpenRiak KV clients**
>
> If you are connecting to Riak using one of Basho's official
[client libraries]({{< product-version-root >}}reference/client-libraries/), you can find more information about getting started with your client in [Developing with OpenRiak KV: Getting Started]({{< product-version-root >}}tutorials/first-application/) section.

At this point, multiple objects have been stored in the same key without
passing any causal context to Riak. Let's see what happens if we try to
read contents of the object:

FetchValue fetch = new FetchValue.Builder(bestCharacterKey).build();
FetchValue.Response response = client.execute(fetch);
RiakObject obj = response.getValue(RiakObject.class);
System.out.println(obj.getValue().toString());
```

```ruby
bucket = client.bucket_type('siblings_allowed').bucket('nickolodeon')
obj = bucket.get('best_character')
obj
```

```python
bucket = client.bucket_type('siblings_allowed').bucket('nickolodeon')
obj = bucket.get('best_character')
obj.siblings
```

```csharp
var id = new RiakObjectId("siblings_allowed", "nickolodeon", "best_character");
var getResult = client.Get(id);
RiakObject obj = getResult.Value;
Debug.WriteLine(format: "Sibling count: {0}", args: obj.Siblings.Count);
foreach (var sibling in obj.Siblings)
{
    Debug.WriteLine(
        format: "    VTag: {0}",
        args: sibling.VTag);
}
```

```javascript
client.fetchValue({
    bucketType: 'siblings_allowed', bucket:
        'nickolodeon', key: 'best_character'
}, function (err, rslt) {
    if (err) {
        throw new Error(err);
    }
    logger.info("nickolodeon/best_character has '%d' siblings",
        rslt.values.length);
});
```

```curl
curl http://localhost:8098/types/siblings_allowed/buckets/nickolodeon/keys/best_character
```

Uh-oh! Siblings have been found. We should get this response:

```java
com.basho.riak.client.cap.UnresolvedConflictException: Siblings found
```

```ruby
<Riak::RObject {nickolodeon,best_character} [#<Riak::RContent [text/plain]:"Ren">, #<Riak::RContent [text/plain]:"Stimpy">]>
```

```python
[<riak.content.RiakContent object at 0x10a00eb90>, <riak.content.RiakContent object at 0x10a00ebd0>]
```

```csharp
Sibling count: 2
    VTag: 1DSVo7VED8AC6llS8IcDE6
    VTag: 7EiwrlFAJI5VMLK87vU4tE
```

```javascript
info: nickolodeon/best_character has '2' siblings
```

```curl
Siblings:
175xDv0I3UFCfGRC7K7U9z
6zY2mUCFPEoL834vYCDmPe
```

As you can see, reading an object with sibling values will result in
some form of "multiple choices" response (e.g. `300 Multiple Choices` in
HTTP). If you're using the HTTP interface and want to view all sibling
values, you can attach an `Accept: multipart/mixed` header to your
request:

```curl
curl -H "Accept: multipart/mixed" \
  http://localhost:8098/types/siblings_allowed/buckets/nickolodeon/keys/best_character
```

Response (without headers):

```
ren
--WUnzXITIPJFwucNwfdaofMkEG7H

stimpy
--WUnzXITIPJFwucNwfdaofMkEG7H--
```

If you select the first of the two siblings and retrieve its value, you
should see `Ren` and not `Stimpy`.

###### Using Causal Context

Once you are presented with multiple options for a single value, you
must determine the correct value. In an application, this can be done
either in an automatic fashion, using a use case-specific resolver, or
by presenting the conflicting objects to the end user. For more
information on application-side conflict resolution, see our
client-library-specific documentation for the following languages:

We won't deal with conflict resolution in this section. Instead, we'll
focus on how to use causal context.

After having written several objects to Riak in the section above, we
have values in our object: `Ren` and `Stimpy`. But let's say that we
decide that `Stimpy` is the correct value based on our application's use
case. In order to resolve the conflict, we need to do three things:

1. Fetch the current object (which will return both siblings)
2. Modify the value of the object, i.e. make the value `Stimpy`
3. Write the object back to the `best_character` key

What happens when we fetch the object first, prior to the update, is
that the object handled by the client has a causal context attached. At
that point, we can modify the object's value, and when we write the
object back to Riak, _the causal context will automatically be attached
to it_. Let's see what that looks like in practice:

```java
// First, we fetch the object
Location bestCharacterKey =
  new Location(new Namespace("siblings_allowed", "nickolodeon"), "best_character");
FetchValue fetch = new FetchValue.Builder(bestCharacterKey).build();
FetchValue.Response res = client.execute(fetch);
RiakObject obj = res.getValue(RiakObject.class);

// Then we modify the object's value
obj.setValue(BinaryValue.create("Stimpy"));

// Then we store the object, which has the vector clock already attached
StoreValue store = new StoreValue.Builder(obj)
        .withLocation(bestCharacterKey);
client.execute(store);
```

```ruby
#### First, we fetch the object
bucket = client.bucket('nickolodeon')
obj = bucket.get('best_character', type: 'siblings_allowed')

#### Then we modify the object's value
obj.raw_data = 'Stimpy'

#### Then we store the object, which has the vector clock already attached
obj.store
```

```python
#### First, we fetch the object
bucket = client.bucket_type('siblings_allowed').bucket('nickolodeon')
obj = bucket.get('best_character')

#### Then we modify the object's value
new_obj.data = 'Stimpy'

#### Then we store the object, which has the vector clock already attached
new_obj.store(vclock=vclock)
```

```csharp
// First, fetch the object
var getResult = client.Get(id);

// Then, modify the object's value
RiakObject obj = getResult.Value;
obj.SetObject<string>("Stimpy", RiakConstants.ContentTypes.TextPlain);

// Then, store the object which has vector clock attached
var putRslt = client.Put(obj);
CheckResult(putRslt);

obj = putRslt.Value;
// Voila, no more siblings!
Debug.Assert(obj.Siblings.Count == 0);
```

```javascript
client.fetchValue({
        bucketType: 'siblings_allowed',
        bucket: 'nickolodeon',
        key: 'best_character'
    }, function (err, rslt) {
        if (err) {
            throw new Error(err);
        }

var riakObj = rslt.values.shift();
        riakObj.setValue('Stimpy');
        client.storeValue({ value: riakObj, returnBody: true },
            function (err, rslt) {
                if (err) {
                    throw new Error(err);
                }

assert(rslt.values.length === 1);
            }
        );
    }
);
```

```curl
curl -i http://localhost:8098/types/siblings_allowed/buckets/nickolodeon/keys/best_character

#### In the HTTP interface, the causal context can be found in the
#### "X-Riak-Vclock" header. That will look something like this:

X-Riak-Vclock: a85hYGBgzGDKBVIcR4M2cgczH7HPYEpkzGNlsP/VfYYvCwA=

#### When performing a write to the same key, that same header needs to
#### accompany the write for Riak to be able to use the vector clock
```

**Concurrent conflict resolution**
It should be noted that it is possible to have two clients that are
simultaneously engaging in conflict resolution. To avoid a pathological
divergence, you should be sure to limit the number of reconciliations and fail
once that limit has been exceeded.

###### Sibling Explosion

Sibling explosion occurs when an object rapidly collects siblings
without being reconciled. This can lead to myriad issues. Having an
enormous object in your node can cause reads of that object to crash
the entire node. Other issues include [increased cluster latency]({{< product-version-root >}}how-to/tune/reduce-latency/) as the object is replicated and out-of-memory errors.

###### Vector Clock Explosion

Besides sibling explosion, the vector clock itself can grow extremely
large when a significant volume of updates are performed on a single
object in a small period of time. While updating a single object
_extremely_ frequently is not recommended, you can tune OpenRiak's vector
clock pruning to prevent vector clocks from growing too large too
quickly. More on pruning in the [section below](#vector-clock-pruning).

###### How does `last_write_wins` affect resolution?

On the surface, it seems like setting `allow_mult` to `false`
(the default) and `last_write_wins` to `true` would result in the same
behavior, but there is a subtle distinction.

Even though both settings return only one value to the client, setting
`allow_mult` to `false` still uses vector clocks for resolution, whereas
if `last_write_wins` is `true`, Riak reads the timestamp to determine
the latest version. Deeper in the system, if `allow_mult` is `false`,
Riak will still allow siblings to exist when they are created (via
concurrent writes or network partitions), whereas setting
`last_write_wins` to `true` means that Riak will overwrite the value
with the one that has the later timestamp.

When you don't care about sibling creation, setting `allow_mult` to
`false` has the least surprising behavior: you get the latest value,
but network partitions are handled gracefully. However, for cases in
which keys are rewritten often (and quickly) and the new value isn't
necessarily dependent on the old value, `last_write_wins` will provide
better performance. Some use cases where you might want to use
`last_write_wins` include caching, session storage, and insert-only
(no updates).

**Note on combining `allow_mult` and `last_write_wins`**
The combination of setting both the `allow_mult` and `last_write_wins`
properties to `true` leads to undefined behavior and should not be used.

##### Vector Clock Pruning

Riak regularly prunes vector clocks to prevent overgrowth based on four
parameters which can be set for any bucket type that you create:

Parameter | Default value | Description
:---------|:--------------|:-----------
`small_vclock` | `50` | If the length of the vector clock list is smaller than this value, the list's entries will not be pruned
`big_vclock` | `50` | If the length of the vector clock list is larger than this value, the list will be pruned
`young_vclock` | `20` | If a vector clock entry is younger than this value (in milliseconds), it will not be pruned
`old_vclock` | `86400` (one day) | If a vector clock entry is older than this value (in milliseconds), it will be pruned

This diagram shows how the values of these parameters dictate the vector
clock pruning process:

![Vclock Pruning]({{< baseurl >}}images/vclock-pruning.png)

##### More Information

Additional background information on vector clocks:

* [Vector Clocks on Wikipedia](http://en.wikipedia.org/wiki/Vector_clock)
* [Why Vector Clocks are Easy](http://basho.com/why-vector-clocks-are-easy/)
* [Why Vector Clocks are Hard](http://basho.com/why-vector-clocks-are-hard/)
* The vector clocks used in Riak are based on the [work of Leslie Lamport](http://portal.acm.org/citation.cfm?id=359563)

### C Sharp

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a conflict resolution strategy that requires applications to resolve siblings according to use-case-specific
criteria. Here, we'll provide a brief guide to conflict resolution using the
official [Riak .NET client][riak_dotnet_client].

#### How the .NET Client Handles Conflict Resolution

In the Riak .NET client, every Riak object has a `siblings` property that
provides access to a list of that object's sibling values. If there are no
siblings, that property will return an empty list.

Here's an example of an object with siblings:

var renResult = client.Put(renObj);
var stimpyResult = client.Put(stimpyObj);

var getResult = client.Get(id);
RiakObject obj = getResult.Value;
Debug.WriteLine(format: "Sibling count: {0}", args: obj.Siblings.Count);
foreach (var sibling in obj.Siblings)
{
    Debug.WriteLine(
        format: "    VTag: {0}",
        args: sibling.VTag);
}
```

So what happens if the count of `obj.Siblings` is greater than 0, as in the case
above?

In order to resolve siblings, you need to either fetch, update and store a
canonical value, or choose a sibling from the `Siblings` list and store that as
the canonical value.

#### Basic Conflict Resolution Example

In this example, you will ignore the contents of the `Siblings` list and will
fetch, update and store the definitive value.

var getResult = client.Get(id);
RiakObject obj = getResult.Value;
Debug.Assert(obj.Siblings.Count == 2);

// Now, modify the object's value
obj.SetObject<string>("Stimpy", RiakConstants.ContentTypes.TextPlain);

##### Choosing a value from `Siblings`

This example shows a basic sibling resolution strategy in which the first
sibling is chosen as the canonical value.

// Pick the first sibling
RiakObject chosenSibling = getResult.Value.Siblings.First();

// Then, store the chosen object
var putRslt = client.Put(chosenSibling);
CheckResult(putRslt);

RiakObject updatedObject = putRslt.Value;
// Voila, no more siblings!
Debug.Assert(updatedObject.Siblings.Count == 0);
```

[riak_dotnet_client]: https://github.com/basho/riak-dotnet-client

### Go

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a conflict resolution strategy that
requires applications to resolve siblings according to usecase-specific
criteria. Here, we'll provide a brief guide to conflict resolution using the
official [Riak Go client](https://github.com/basho/riak-go-client).

#### How the Go Client Handles Conflict Resolution

In the Riak Go client, it is possible that the result of a fetch will return an array
of sibling objects. If there are no siblings, that property will return an
array with one value in it.

[*Example:* creating object with siblings](https://github.com/basho/riak-go-client/blob/master/examples/dev/using/conflict-resolution/main.go#L68-L70)

So what happens if the length of `Values` is greater than 1, as in the case
above?

In order to resolve siblings, you need to either: fetch, update, and store a
canonical value; or choose a sibling from the `Values` slice and store that as
the canonical value.

In this example, you will ignore the contents of the `Values` slice and will
fetch, update and store the definitive value.

[*Example:* resolving siblings via store](https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/using/conflict-resolution.js#L125-L146)

##### Choosing a value from `Values`

[*Example:* resolving siblings using the first value](https://github.com/basho/riak-go-client/blob/master/examples/dev/using/conflict-resolution/main.go#L148-L167)

##### Using `ConflictResolver`

This example shows a basic sibling resolution strategy in which the first
sibling is chosen as the canonical value via a conflict resolution type.

[*Example:* resolving siblings via `ConflictResolver`](https://github.com/basho/riak-go-client/blob/master/examples/dev/using/conflict-resolution/main.go#L169-L210)

### Java

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a
conflict resolution strategy that requires applications to resolve
siblings according to use-case-specific criteria. Here, we'll provide a
brief guide to conflict resolution using the official [Riak Java
client](https://github.com/basho/riak-java-client).

#### How the Java Client Handles Conflict Resolution

The official Riak Java client provides a `ConflictResolver` interface
for handling sibling resolution. This interface requires that you
implement a `resolve` method that takes a Java `List` of objects of a
specific type that are stored in Riak and produces a single object of
that type, i.e. converts a `List<T>` to a single `T`. Once that
interface has been implemented, it can be registered as a singleton and
thereby applied to all read operations on a specific data type. Below is
an example resolver for the class `Foo`:

```java
import com.basho.riak.client.api.cap.ConflictResolver;

public class FooResolver implements ConflictResolver<Foo> {
    @Override
    public Foo resolve(List<Foo> siblings) {
        // Insert your sibling resolution logic here
    }
}
```

What happens within the `resolve` method is up to you and will always
depend on the use case at hand. You can implement a resolver that
selects a random `Foo` from the list, chooses the `Foo` with the most
recent timestamp (if you've set up the class `Foo` to have timestamps),
etc. In this tutorial we'll provide a simple example to get you started.

Let's say that we're building a social network application and storing
lists of usernames representing each user's "friends" in the network.
Each user will bear the class `User`, which we'll create below. All of
the data for our application will be stored in buckets that bear the
[bucket type]({{< product-version-root >}}how-to/develop/use-bucket-types/) `siblings`, and for this bucket type
`allow_mult` is set to `true`, which means that Riak will generate
siblings in certain cases---siblings that our application will need to
be equipped to resolve when they arise.

The question that we need to ask ourselves now is this: if a given user
has sibling values, i.e. if there are multiple `friends` lists and Riak
can't decide which one is most causally recent, which list should be
deemed "correct" from the standpoint of the application? What criteria
should be applied in making that decision? Should the lists be merged?
Should we pick a `User` object at random?

This decision will always be yours to make. Here, though, we'll keep it
simple and say that the following criterion will hold: if conflicting
lists exist, _the longer list will be the one that our application deems
correct_. So if the user `user1234` has a sibling conflict where one
possible value has `friends` lists with 100, 75, and 10 friends,
respectively, the list of 100 friends will win out.  While this might
not make sense in real-world applications, it's a good jumping-off
point. We'll explore the drawbacks of this approach, as well as a better
alternative, in this document as well.

##### Creating Our Data Class

We'll start by creating a `User` class for each user's data. Each `User`
object will consist of a `username` as well as a `friends` property that
lists the usernames, as strings, of the user's friends. We'll use a
`Set` for the `friends` property to avoid duplicates.

```java
public class User {
    public String username;
    public Set<String> friends;

public User(String username, Set<String> friends) {
        this.username = username;
        this.friends = friends;
    }
}
```

Here's an example of instantiating a new `User` object:

```java
Set<String> friends = new HashSet<String>();
friends.add("fred");
friends.add("barney");
User bashobunny = new User("bashobunny", friends);
```

##### Implementing a Conflict Resolution Interface

So what happens if siblings are present and the user `bashobunny` has
different friend lists in different object replicas? For that we can
implement the `ConflictResolver` class described [above](#how-the-java-client-handles-conflict-resolution). We
need to implement that interface in a way that is specific to the need
at hand, i.e. taking a list of `User` objects and returning the `User`
object that has the longest `friends` list:

public class UserResolver implements ConflictResolver<User> {
    @Override
    public User resolve(List<User> siblings) {
        // If there are no objects present, return null
        if (siblings.size == 0) {
            return null;
        // If there is only one User object present, return that object
        } else if (siblings.size == 1) {
            return siblings.get(0);
        // And if there are multiple User objects, return the object
        // with the longest list
        } else {
            int longestList = 0;
            User userWithLongestList;

// Iterate through the User objects to check for the longest
            // list
            for (User user : siblings) {
                if (user.friends.size() > longestList) {
                    userWithLongestList = user;
                    longestList = user.friends.size();
                }
            }
            // If all sibling User objects have a friends list with a length
            // of 0, it doesn't matter which sibling is selected, so we'll
            // simply select the first one in the list:
            return userWithLongestList == null ? siblings.get(0) : userWithLongestList;
        }
    }
}
```

##### Registering a Conflict Resolver Class

To use a conflict resolver, we must register it:

```java
ConflictResolverFactory factory = ConflictResolverFactory.getInstance();
factory.registerConflictResolver(User.class, new UserResolver());
```

With the resolver registered, the resolution logic that we have created
will resolve siblings automatically upon read. Registering a custom
conflict resolver can occur at any point in the application's lifecycle
and will be applied on all reads that involve that object type.

#### Conflict Resolution and Writes

In the above example, we created a conflict resolver that resolves a
list of discrepant `User` objects and returns a single `User`. It's
important to note, however, that this resolver will only provide the
application with a single "correct" value; it will _not_ write that
value back to Riak. That requires a separate step. When this step should
be undertaken depends on your application. In general, though, we
recommend writing objects to Riak only when the application is ready to
commit them, i.e. when all of the changes that need to be made to the
object have been made and the application is ready to persist the state
of the object in Riak.

Correspondingly, we recommend that updates to objects in Riak follow
these steps:

1. **Read** the object from Riak
2. **Resolving sibling conflicts** if they exist, allowing the
application to reason about one "correct" value for the object (this
step is the subject of this tutorial)
3. **Modify** the object
4. **Write** the object to Riak once the necessary changes have been
made

You can find more on writing objects to Riak, including examples from
the official Java client library, in the [Developing with OpenRiak KV: Usage]({{< product-version-root >}}how-to/develop/) section.

#### More Advanced Example

Resolving sibling `User` values on the basis of which user has the
longest `friends` list has the benefit of being simple but it's probably
not a good resolution strategy for our social networking application
because it means that unwanted data loss is inevitable. If one friends
list contains `A`, `B`, and `C` and the other contains `D` and `E`, the
list containing `A`, `B`, and `C` will be chosen. So what about friends
`D` and `E`? Those usernames are essentially lost. In the sections
below, we'll implement some other conflict resolution strategies as
examples.

##### Merging the Lists

To avoid losing data like this, a better strategy may be to merge the
lists. We can modify our original `resolve` function in our
`UserResolver` to accomplish precisely that:

```java
public class UserResolver implements ConflictResolver<User> {
    @Override
    public User resolve(List<User> siblings) {
        // We apply the same logic as before, returning null if the
        // key is empty and returning the one sibling if there is only
        // one User in the siblings list
        if (siblings.size == 0) {
            return null;
        } else if (siblings.size == 1) {
            return siblings.get(0);
        } else {
            // We begin with an empty Set
            Set<String> setBuilder = new HashSet<String>();

// We know that all User objects in the List will have the
            // same username, since we used the username for the key, so
            // we can fetch the username of any User in the list:
            String username = siblings.get(0).username;

// Now for each User object in the list we add the friends
            // list to our empty Set
            for (User user : siblings) {
                setBuilder.addAll(user.friends);
            }

// Then we return a new User object that takes the Set we
            // built as the friends list
            return new User(username, setBuilder);
        }
    }
}
```

Since the `friends` list is a Java `Set`, we don't need to worry about
duplicate usernames.

The drawback to this approach is the following: with a conflict
resolution strategy like this, it's more or less inevitable that a user
will remove a friend from their friends list, and that that friend will
end up back on the list during a conflict resolution operation. While
that's certainly not desirable, that is likely better than the
alternative proposed in the first example, which entails usernames being
simply dropped from friends lists. Sibling resolution strategies almost
always carry potential drawbacks of this sort.

#### Riak Data Types

An important thing to always bear in mind when working with conflict
resolution is that Riak offers a variety of [Data Types]({{< product-version-root >}}reference/data/distributed-data-types/) that have
specific conflict resolution mechanics built in. If you have data that
can be modeled as a [counter]({{< product-version-root >}}reference/data/distributed-data-types/), [set]({{< product-version-root >}}reference/data/distributed-data-types/), or [map]({{< product-version-root >}}reference/data/distributed-data-types/), then you should seriously
consider using those Data Types instead of creating your own
application-side resolution logic.

In the example above, we were dealing with conflict resolution within a
set, in particular the `friends` list associated with each `User`
object. The merge operation that we built to handle conflict resolution
is analogous to the resolution logic that is built into Riak sets. For
more information on how you could potentially replace the client-side
resolution that we implemented above, see our [tutorial on Riak sets]({{< product-version-root >}}reference/data/distributed-data-types/).

### NodeJS

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a conflict resolution strategy that
requires applications to resolve siblings according to use-case-specific
criteria. Here, we'll provide a brief guide to conflict resolution using the
official [OpenRiak node.js client](https://github.com/basho/riak-nodejs-client).

#### How the Node.js Client Handles Conflict Resolution

In the OpenRiak node.js client, the result of a fetch can possibly return an array
of sibling objects.  If there are no siblings, that property will return an
array with one value in it.

[*Example:* creating object with siblings](https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/using/conflict-resolution.js#L21-L68)

So what happens if the length of `rslt.values` is greater than 1, as in the case
above?

In order to resolve siblings, you need to either fetch, update and store a
canonical value, or choose a sibling from the `values` array and store that as
the canonical value.

In this example, you will ignore the contents of the `values` array and will
fetch, update and store the definitive value.

[*Example:* resolving siblings via store](https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/using/conflict-resolution.js#L91-L111)

##### Choosing a value from `rslt.values`

[*Example:* resolving siblings via first](https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/using/conflict-resolution.js#L113-L133)

This example shows a basic sibling resolution strategy in which the first
sibling is chosen as the canonical value via a conflict resolution function.

[*Example:* resolving siblings via `conflictResolver](https://github.com/basho/riak-nodejs-client-examples/blob/master/dev/using/conflict-resolution.js#L135-L170)

### PHP

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a
conflict resolution strategy that requires applications to resolve
siblings according to use-case-specific criteria. Here, we'll provide a
brief guide to conflict resolution using the official [Riak PHP
client](https://github.com/basho/riak-php-client).

#### How the PHP Client Handles Conflict Resolution

Every `\Basho\Riak\Object` command returns a `\Basho\Riak\Command\Object\Response`
object, which provides what is needed to handle object conflicts. If siblings exist
and have been returned from the server within the response body, they will be
available within the response object. See below:

```php
$response = (new \Basho\Riak\Command\Builder\FetchObject($riak))
    ->buildLocation('conflicted_key', 'bucket_name', 'bucket_type')
    ->build()
    ->execute();

echo $response->getStatusCode(); // 300
echo $response->hasSiblings(); // 1
echo $response->getSiblings(); // \Basho\Riak\Object[]
```

```php
class User {
    public $username;
    public $friends;

public function __construct($username, array $friends = [])
    {
        $this->username = $username;
        $this->friends = $friends;
    }

public function __toString()
    {
        return json_encode([
            'username' => $this->username,
            'friends' => $this->friends,
            'friends_count' => count($this->friends)
        ]);
    }
}
```

```php
$bashobunny = new User('bashobunny', ['fred', 'barney']);
```

##### Implementing a Conflict Resolution Function

Let's say that we've stored a bunch of `User` objects in Riak and that a
few concurrent writes have led to siblings. How is our application going
to deal with that? First, let's say that there's a `User` object stored
in the bucket `users` (which is of the bucket type `siblings`, as
explained above) under the key `bashobunny`. We can fetch the object
that is stored there and see if it has siblings:

```php
$response = (new \Basho\Riak\Command\Builder\FetchObject($riak))
    ->buildLocation('bashobunny', 'users', 'siblings')
    ->build()
    ->execute();

echo $response->hasSiblings(); // 1
```

If we get `true`, then there are siblings. So what do we do in that
case? At this point, we need to write a function that resolves the list
of siblings, i.e. reduces the `$response->getSiblings()` array down to one member.
In our case, we need a function that takes a Riak response object as its argument,
applies some logic to the list of values contained in the `siblings` property
of the object, and returns a single value. For our example use case here, we'll
return the sibling with the longest `friends` list:

```php
use \Basho\Riak;
use \Basho\Riak\Command;

function longest_friends_list_resolver(Command\Object\Response $response)
{
    if ($response->hasSiblings()) {
        $siblings = $response->getSiblings();
        $max_key = 0;
        foreach ($siblings as $key => $sibling) {
            if ($sibling->getData()['friends_count'] > $siblings[$max_key]->getData()['friends_count']) {
                $max_key = $key;
            }
        }
    }

return $siblings[$max_key];
}
```

We can then embed this function into a more general function for fetching
objects from the users bucket:

```php
function fetch_user_by_username($username, Riak $riak)
{
    $response = (new Command\Builder\FetchObject($riak))
      ->buildLocation($username, 'users', 'siblings')
      ->build()
      ->execute();

return longest_friends_list_resolver($response);
}

bashobunny = fetch_user_by_username('bashobunny', $riak);
```

Now, when a `User` object is fetched (assuming that the username acts as
a key for the object), a single value is returned for the `friends`
list. This means that our application can now use a "correct" value
instead of having to deal with multiple values.

You can find more on writing objects to Riak, including examples from
the official PHP client library, in the [Developing with OpenRiak KV: Usage]({{< product-version-root >}}how-to/develop/) section.

Resolving sibling `User` values on the basis of which user has the longest
friends list has the benefit of being simple but it's probably not a
good resolution strategy for our social networking application because
it means that unwanted data loss is inevitable. If one friend list
contains `A`, `B`, and `C` and the other contains `D` and `E`, the list
containing `A`, `B`, and `C` will be chosen. So what about friends `D`
and `E`? Those usernames are essentially lost. In the sections below,
we'll implement an alternative strategy as an example.

To avoid losing data like this, a better strategy would be to merge the
lists. We can modify our original resolver function to accomplish
precisely that and will also store the resulting `User` object.

The drawback to this approach is that it's more or less inevitable that a user
will remove a friend from their friends list, and then that friend will
end up back on the list during a conflict resolution operation. While
that's certainly not desirable, that is likely better than the
alternative proposed in the first example, which entails usernames being
simply dropped from friends lists. Sibling resolution strategies almost
always carry potential drawbacks of this sort.

#### Riak Data Types

### Python

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a
conflict resolution strategy that requires applications to resolve
siblings according to use-case-specific criteria. Here, we'll provide a
brief guide to conflict resolution using the official [Riak Python
client](https://github.com/basho/riak-python-client).

#### How the Python Client Handles Conflict Resolution

In the official Python client, every object of the `RiakObject` class
has a `siblings` property that provides access to a list of an object's
sibling values. If there are no siblings, that property will return a
list with only one item. Here's an example of an object with siblings:

```python
bucket = client.bucket('seahawks')
obj = bucket.get('coach')
obj.siblings

#### The output:
[<riak.content.RiakContent object at 0x106cc51d0>, <riak.content.RiakContent object at 0x108x1da62c1>]
```

So what happens if the length of `obj.siblings` is greater than 1, as in
the case above? The easiest way to resolve siblings automatically with
the Python client is to create a conflict-resolving function that takes
a list of sibling values and returns a single value. Such resolution
functions can be registered either at the object level or the bucket
level. A more complete explanation can be found in the section directly
below.

##### Basic Conflict Resolution Example

Let's say that we're building a social network application and storing
lists of usernames representing each user's "friends." Each user will
be of the class `User`, which we'll create below. All of the data for our
application will be stored in buckets that bear the [bucket type]({{< product-version-root >}}how-to/develop/use-bucket-types/) `siblings`, and for this bucket type `allow_mult` is set
to `true`, which means that Riak will generate siblings in certain
cases---siblings that our application will need to be equipped to
resolve when necessary.

The question that we need to ask ourselves at this point is the
following: if a given user has conflicting lists, which list should be
deemed more "correct?" What criteria should be applied? Should the lists
be merged? Should we pick a list at random and deem that list correct?
We'll keep it simple here and say that the following criterion will
hold: if multiple conflict lists exist, _the longer list will be the one
that our application deems correct_. While this might not make sense in
real-world applications, it's a good jumping-off point.

###### Creating Our Data Class

We'll start by creating a `User` class for each user's data. Each `User`
object will consist of a `friends` property that lists the usernames, as
strings, of the user's friends. We will also create a `to_json` method,
as we'll be storing each `User` object as JSON:

```python
class User(object):
    def __init__(self, username, friends):
        self.username = username
        self.friends = friends

def to_json(self):
        return vars(self)
```

Now, we can create `User` objects and see what they look like as JSON:

```python
new_user = User('riakuser127', ['captheorem', 'siblingsrule572'])

new_user.to_json()
#### {'username': 'riakuser127', 'friends': ['captheorem238', 'siblingsrule572']}
```

###### Implementing and Registering a Conflict Resolution Function

```python
bucket = client.bucket_type('siblings').bucket('users')
obj = bucket.get('bashobunny')

print len(obj.siblings) > 1
```

If we get `True`, then there are siblings. So what do we do in that
case? The Python client allows us to write a conflict resolution hook
function that will be triggered any time siblings are found, i.e. any
time `len(obj.siblings) > 1`. A hook function like this needs to take a
single `RiakObject` object as its argument, apply some sort of logic to
the list of values contained in the `siblings` property, and ultimately
return a list with a single "correct" value. For our example case, we'll
return the value with the longest `friends` list:

```python
def longest_friends_list_resolver(riak_object):
    # We'll specify a lambda function that operates on the length of
    # each sibling's "friends" list:
    lm = lambda sibling: len(sibling.data['friends'])
    # Then we'll return a list that contains only the object with the
    # maximum value for the length of the "friends" list:
    riak_object.siblings = [max(riak_object.siblings, key=lm), ]
```

###### Registering a Conflict Resolver Function

In the Python client, resolver functions can be registered at the object
level, as in this example:

```python
bucket = client.bucket_type('siblings').bucket('users')
obj = RiakObject(client, bucket, 'bashobunny')
obj.resolver = longest_friends_list_resolver

#### Now, when the object is loaded from Riak, it will resolve to a single
#### value instead of multiple values when both commands are executed:
obj.reload()
obj.store()
```

Alternatively, resolvers can be registered at the bucket level, so that
the resolution is applied to all objects in the bucket:

```python
bucket = client.bucket_type('siblings').bucket('users')
bucket.resolver = longest_friends_list_resolver

obj = RiakObject(client, bucket, 'bashobunny')
obj.reload()
obj.store()

#### The resolver will also be applied if you perform operations using the
#### bucket object:

bucket.get('bashobunny')
bucket.get('some_other_user')
```

##### Conflict Resolution and Writes

In the above example, we created a conflict resolver that resolves a
list of discrepant `User` object values and returns a single value. It's
important to note, however, that this resolver will only provide the
application with a single "correct" value; it will _not_ write that
value back to Riak. That requires a separate step. When this step should
be undertaken depends on your application. In general, though, we
recommend writing objects to Riak only when the application is ready to
commit them, i.e. when all of the changes that need to be made to the
object have been made and the application is ready to persist the state
of the object in Riak.

You can find more on writing objects to Riak, including code examples
from the official Python client library, in the [Developing with OpenRiak KV: Usage]({{< product-version-root >}}how-to/develop/) section.

##### More Advanced Example

Resolving sibling `User` values on the basis of which user has the
longest `friends` list has the benefit of being simple but it's probably
not a good resolution strategy for our social networking application
because it means that unwanted data loss is inevitable. If one friend
list contains `A`, `B`, and `C` and the other contains `D` and `E`, the
list containing `A`, `B`, and `C` will be chosen. So what about friends
`D` and `E`? Those usernames are essentially lost. In the sections
below, we'll implement an alternative strategy as an example.

###### Merging the Lists

To avoid losing data like this, a better strategy would be to merge the
lists. We can modify our original resolver function to accomplish
precisely that and will also store the resulting `User` object:

```python
from riak.content import RiakContent

def longest_friends_list_resolver(riak_object):
    # We start with an empty set
    friends_list = set()

# Then we add all the friends from all siblings to the set
    for user in riak_object.siblings:
        friends_list.update(user.data['friends'])

# Then we make a new User object. First, we fetch the username from
    # any one of the siblings, then we pass in our new friends list.
    username = riak_object.siblings[0].data['username']
    new_user = User(username, list(friends_list))

# Now we reuse the first sibling as a container for the merged data
    riak_object.siblings[0].data = new_user.to_json()

# And finally we set the siblings property to include just the
    # single, resolved sibling
    riak_object.siblings = [riak_object.siblings[0]]
```

##### Riak Data Types

### Ruby

For reasons explained in the [Introduction to conflict resolution]({{< product-version-root >}}how-to/develop/resolve-conflicts/), we strongly recommend adopting a
conflict resolution strategy that requires applications to resolve
siblings according to use-case-specific criteria. Here, we'll provide a
brief guide to conflict resolution using the official [Riak Ruby
client](https://github.com/basho/riak-ruby-client).

#### How the Ruby Client Handles Conflict Resolution

In the official Ruby client, every Riak object has a `siblings` property
that provides access to a list of that object's sibling values. If there
are no siblings, that property will return an array with only one item.
Here's an example of an object with siblings:

```ruby
bucket = client.bucket('seahawks')
obj = bucket.get('coach')
obj.siblings

#### The output:
[#<Riak::RContent [content/type]: "Jim Mora">, #<Riak::RContent [content/type]: "Pete Carroll">]
```

So what happens if the length of `obj.siblings` is greater than 1, as in
the case above? In order to resolve siblings, you need to create a
resolution function that takes a Riak object and reduces the `siblings`
array down to a single value. An example is provided in the section
below.

We'll start by creating a `User` class for each user's data. Each `User`
object will consist of a `username` and a `friends` property that lists
the usernames, as strings, of the user's friends. We will also create a
`to_json` method, as we'll be storing each `User` object as JSON:

```ruby
class User
  def initialize(username, friends)
    @username = username
    @friends = friends
  end

def to_json
    { :username => @username, :friends => @friends }
  end
end
```

```ruby
new_user = User.new('riakuser127', ['captheorem238', 'siblingsrule572'])

new_user.to_json
#### {'username': 'riakuser127', 'friends': ['captheorem238', 'siblingsrule572']}
```

##### Implementing a Conflict Resolution Function

```ruby
bucket = client.bucket('users')
obj = bucket.get('bashobunny', type: 'siblings')
p obj.siblings.length > 1
```

If we get `true`, then there are siblings. So what do we do in that
case? At this point, we need to write a function that resolves the list
of siblings, i.e. reduces the `obj.siblings` array down to one member.
In our case, we need a function that takes a single Riak object (or
`RObject` in the Ruby client) as its argument, applies some logic to the
list of values contained in the `siblings` property of the object, and
returns a single value. For our example use case here, we'll return the
sibling with the longest `friends` list:

```ruby
def longest_friends_list_resolver(riak_object)
  # The "conflict?" method is built into the Ruby client
  if riak_object.conflict?
    # The "max_by" method enables us to select the sibling with the
    # longest "friends" list
    riak_object.siblings.max_by{ |user| user.data['friends'].length }
  else
    # If there are no siblings, we can simply return the object's
    # "content" as is
    riak_object.content
  end
end
```

We can then embed this function into a more general function for
fetching objects from the `users` bucket:

```ruby
def fetch_user_by_username(username)
  bucket = client.bucket('users')
  user_object = bucket.get(username)
  longest_friends_list_resolve(user_object)
  user_object
end

bashobunny = fetch_user_by_username('bashobunny')
```

You can find more on writing objects to Riak, including examples from
the official Ruby client library, in the [Developing with OpenRiak KV: Usage]({{< product-version-root >}}how-to/develop/) section.

Resolving sibling User values on the basis of which user has the longest
friends list has the benefit of being simple but it's probably not a
good resolution strategy for our social networking application because
it means that unwanted data loss is inevitable. If one friend list
contains `A`, `B`, and `C` and the other contains `D` and `E`, the list
containing `A`, `B`, and `C` will be chosen. So what about friends `D`
and `E`? Those usernames are essentially lost. In the sections below,
we'll implement an alternative strategy as an example.

```ruby
def longest_friends_list_resolver(riak_object)
  # An empty array for use later on
  friends_list = []
  if riak_object.conflict?
    # The "friends" arrays for all siblings will be merged into one
    # array
    riak_object.siblings.each do |sibling|
      friends_list.push(sibling.data['friends'])
    end

# Then we make a new User object. First, we fetch the username from
    # any one of the siblings, then we pass in our new friends list,
    # calling the "uniq" method to eliminate duplicate usernames.
    username = riak_object.siblings[0].data['username']
    new_user = User.new(username, friends_list.uniq)

# Now we reuse the first sibling as a container for the merged data
    riak_object.siblings[0].data = new_user.to_json

# And finally we set the siblings property to include just the
    # single, resolved sibling
    riak_object.siblings = [riak_object.siblings[0]]
  else
    riak_object.content
  end
end
```

In the example above, we were dealing with conflict resolution within a
set, in particular the `friends` list associated with each `User`

object. The merge operation that we built to handle conflict resolution
is analogous to the resolution logic that is built into Riak sets. For
more information on how you could potentially replace the client-side
resolution that we implemented above, see our [tutorial on Riak sets]({{< product-version-root >}}reference/data/distributed-data-types/).

## Verify the result

Run the operation against test data, inspect the stored result and response metadata, and exercise the expected failure path.
