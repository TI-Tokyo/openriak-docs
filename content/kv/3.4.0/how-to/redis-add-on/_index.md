---
title: 'Use the Redis add-on'
description: 'Introduce practical procedures for deploying and using the Redis add-on for OpenRiak.'
weight: 1
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis\redis-add-on-features.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce practical procedures for deploying and using the Redis add-on for OpenRiak.

## Before you begin

Access to the affected OpenRiak KV environment, the exact product version, a record of the current state, and a safe rollback plan.

## Overview

### Add-ons

In the days of Basho, integrations between OpenRiak KV and other best-of-breed components were developed for your application stack. Each integration, called an add-on, is explained in this section, from installation to feature-set.

* [Riak Redis Add-on]({{< baseurl >}}kv/3.4.0/how-to/redis-add-on/)

### OpenRiak Redis Add-on

[addon redis develop]: ./developing-rra/
[addon redis features]: ./redis-add-on-features/
[addon redis setup]: ./set-up-rra/
[addon redis use]: ./get-started-with-rra/
[ee]: https://www.tiot.jp/en/about-us/contact-us/

**Warning: No longer actively maintained**
Since moving to Open Source, the Riak Redis Add-on is no longer actively maintained. As basic functionality has not changed, we expect the add-on to continue working with newer versions without incident but cannot guarantee this. The text below is left from the last known good version.

Riak Redis Add-on (RRA) is a distributed cache service that joins the power of Redis caching with the eventual consistency guarantees of OpenRiak KV.

RRA enables you to reduce latency for OpenRiak KV reads through the use of a distributed cache layer. This type of caching is most effective for keys that are immutable or have an infrequent change rate.

Whether you are looking to build out a session, shopping cart, advertisement or other dynamically-rendered copy, RRA helps reduce read pressure on your persistent store (OpenRiak KV).

#### Compatibility

RRA is supported on the following platforms:

* RHEL/CentOS 6
* RHEL/CentOS 7
* Ubuntu 12.04 LTS "Precise Pangolin"
* Ubuntu 14.04 LTS "Trusty Tahr"
* Debian 7 "Wheezy"
* Debian 8 "Jessie"

RRA is compatible with the following services:

* OpenRiak KV Enterprise (2.1.4+)
* Riak TS Enterprise (1.4.0+)
* Redis 2.x and 3.x (in 3.x, not supporting Redis Cluster)
  * Redis Cluster and RRA's consistent hash are at odds, which surface as errors
    such as MOVED, ASK, and CROSSSLOT messages from Redis, see (WIP):
    https://github.com/antirez/redis-rb-cluster

#### Get Started

* [Set up RRA.][addon redis setup]
* [Use RRA with various clients.][addon redis use]
* [Develop with RRA.][addon redis develop]
* [Learn about RRA's features.][addon redis features]

### OpenRiak Redis Add-on Features

[ee]: https://www.tiot.jp/en/about-us/contact-us/
[GET-sequence]: {{< baseurl >}}images/redis/GET_seq.msc.png
[SET-sequence]: {{< baseurl >}}images/redis/SET_seq.msc.png
[DEL-sequence]: {{< baseurl >}}images/redis/DEL_seq.msc.png
[Object-lifetime]: {{< baseurl >}}images/redis/Object_lifetime.msc.png
[redis docs]: http://redis.io/commands
[twemproxy docs]: https://github.com/twitter/twemproxy/blob/master/notes/redis.md

#### Overview

The cache proxy service in Riak Redis Add-on (RRA) provides pre-sharding and connection aggregation as a service, which reduces latency and increases addressable cache memory space with lower-cost hardware.

On this page, you will find detailed descriptions of cache proxy service components, including what each component does and how you implement it. The following components are available:

* [Pre-sharding](#pre-sharding)
* [Connection Aggregation](#connection-aggregation)
* [Command Pipelining](#command-pipelining)
* [Read-through Cache](#read-through-cache)
* [Write-around Cache](#write-around-cache)
* [Commands](#commands)
* [Object Lifetime](#object-lifetime)

#### Pre-sharding

Pre-sharding with consistent hashing dispatches object reads and writes based
on a configurable hash function, spreading load across multiple cache servers.
The cache proxy service uses pre-sharding to extend the total addressable cache memory space based on the number of Redis servers. Request keys are hashed, then
requests are routed to the Redis server that handles that portion of the key
range.

Redis with no persistence is used as the frontend cache proxy service, and
Redis as a data server holds all data in memory. The addressable memory of
cache proxy is limited. By employing pre-sharding, the total addressable cache
memory space is extended by the number of Redis servers.

#### Connection Aggregation

Redis client connections are a limited resource. Using the cache proxy service, connections may be spread across multiple Riak Redis Add-on (RRA) servers. This reduces the total required connections to the Redis server for the same key.

Redis clients in various languages support specifying multiple servers, as well
as implementing multiple methods of spreading load across those servers (i.e.
round-robin load balancing or consistent hashing).  Since the cache proxy service is providing consistent hashing, any Redis client method of supporting multiple
servers will suffice.

#### Command Pipelining

The cache proxy service increases performance by pipelining requests to Redis. While pipelining can be performed at the client, the cache proxy service is ideal due to connection aggregation. Pipelining reduces network roundtrips to Redis and
lowers CPU usage on Redis.

#### Read-Through Cache

Implementing caching strategies in the cache proxy service reduces the cost of implementing cache strategies in client code in multiple applications and languages. The cache proxy service supports the read-through cache strategy, the most prevalent caching strategy used in distributed computing.

The read-through cache strategy of the GET command is represented by the
following sequence diagram:

![GET command sequence diagram]({{< baseurl >}}images/redis/GET_seq.msc.png)

The `CACHE_TTL` configuration option establishes how long the cache takes to
become consistent with the backend server during a write (DELETE or PUT) to the
backend server.

A short `CACHE_TTL`, for example "15s", reduces a significant amount of read
pressure from Riak, increasing performance of the overall solution.

#### Write-Around Cache

The read-through cache strategy requires a TTL to keep cache as coherent as possible given that writes to OpenRiak KV can and will be issued without the cache proxy service being informed of the write. The effect is that the cache proxy service is eventually consistent with the underlying OpenRiak KV data store, with the time to consistency equal to the TTL.

The cache proxy service write-around cache strategy was introduced to provide a means to keep cache coherent with zero time to consistency with the underlying OpenRiak KV data store for all writes that the cache proxy is informed of. For the Redis String (Value in KV) datatype, SET and DEL commands result in writes to the underlying OpenRiak KV data store followed by a PEXPIRE to invalidate cache.

Of the three write cache strategies, the write-around cache strategy is the least
prone to race condition, but least optimal for the read which immediately follows
the write. In the overwhelming majority of distributed application data access
patterns, the added certainty of cache coherency afforded by write-around over
write-through is well worth the single cache miss. By definition, a key that is
cached is expected to be accessed frequently, hence the single cache miss is
expected to be followed by several accurate cache hits.

The write-around cache strategy of the SET command is represented by the
following sequence diagram:

![SET command sequence diagram]({{< baseurl >}}images/redis/SET_seq.msc.png)

The write-around cache strategy of the DEL command is represented by the
following sequence diagram:

![DEL command sequence diagram]({{< baseurl >}}images/redis/DEL_seq.msc.png)

#### Commands

For command details, refer to the Redis [documentation][redis docs].

The cache proxy service supports the following augmented Redis commands fully:

* GET - get the value of a key from Redis or OpenRiak KV utilizing the read-through
  caching strategy with a TTL set at service configuration time.

* SET - set the value of a key to OpenRiak KV and invalidate cache, issue a PEXPIRE
  to Redis.

* DEL - delete the value of a key to OpenRiak KV and invalidate cache, issue a
  PEXPIRE to Redis.

The cache proxy service also supports the set of Redis commands supported by Twemproxy, but only to the point of pre-sharding and command pipelining, issued only to Redis. Refer to the Twemproxy [documentation][twemproxy docs].

>**Important:** While the cache proxy service does support issuing DEL commands, PEXPIRE, with a small TTL, is suggested instead when the semantic intent is to remove an item from cache.  With write-around, the DEL command will issue a delete to the Riak backend.

#### Object Lifetime

With the combination of read-through and write-around cache strategies, the
full object lifetime for a key-value is represented by the following
sequence diagram:

![Object lifetime sequence diagram]({{< baseurl >}}images/redis/Object_lifetime.msc.png)

## Verify the result

Confirm the requested outcome, inspect cluster health and logs, and test the relevant client or operational path.

## In this section

- [Extend the Redis add-on]({{< baseurl >}}kv/3.4.0/how-to/redis-add-on/develop/) — Show developers how to add and test a supported Redis add-on feature.
- [Set up the Redis add-on]({{< baseurl >}}kv/3.4.0/how-to/redis-add-on/set-up/) — Show operators how to deploy the Redis add-on in a supported topology and verify connectivity.
- [Use the Redis add-on]({{< baseurl >}}kv/3.4.0/how-to/redis-add-on/use/) — Show developers how to perform supported Redis operations against OpenRiak.
