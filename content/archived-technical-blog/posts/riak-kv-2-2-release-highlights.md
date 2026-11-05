---
title: "Riak KV 2.2 Release Highlights"
date: "2016-11-16T20:31:13+00:00"
author: "Charlie Voiselle"
original_url: "http://basho.com/posts/technical/riak-kv-2-2-release-highlights/"
archive_url: "https://web.archive.org/web/20170606160211http://basho.com/posts/technical/riak-kv-2-2-release-highlights/"
categories:
  - "Releases"
---
Riak KV 2.2 continues Basho’s commitment to our customers and community to develop and deliver a highly resilient, high-performance, key-value database.

The new features include:

- Global Object Expiration (LevelDB)
- Support for HyperLogLog Data Types
- Improved Active Anti-Entropy Performance
- Cluster Job Controls
- Improvements to Riak Search (up to 5X faster ingest)
- LZ4 compression (LevelDB)
- Support for Debian 8 “Jessie” and Ubuntu 16 “Xenial”
- Continued support for Upgrade / Downgrade

***Global Object Expiration***

[Global Object Expiration](http://docs.basho.com/riak/kv/latest/configuring/global-object-expiration/) is now available for both Bitcask and LevelDB storage backends. LevelDB support is new in v2.2. You can configure the expiry or [time to live (TTL)](https://en.wikipedia.org/wiki/Time_to_live) for your data in the `riak.conf` file. By default, expiration is disabled. By enabling it you can reclaim space or remove data based on a required retention period.

The example below shows how to configure LevelDB for a retention time of 5 hours:

```
leveldb.expiration = on
leveldb.expiration.retention_time = 5h
```

Data outside the retention time is deleted by the asynchronous LevelDB compaction process.

We have started development on bucket-level expiry which is expected to be available in a future release of Riak KV.

***HyperLogLog Data Type***

Riak Data Types now include [HyperLogLog](http://docs.basho.com/riak/kv/latest/learn/concepts/crdts/#hyperloglogs). As most of you are aware, a HyperLogLog is used to estimate the unique elements in a large set or stream of data while keeping memory usage low. Like other Riak Data Types, the HyperLogLog data type is enabled via bucket-level attribute.

Start by creating a bucket type with the `datatype` parameter set to `hyperloglog`:

```
riak_admin bucket-type create hlls '{"props" : {"datatype":"hll"}}'
```

Then activate the bucket type:

```
riak_admin bucket-type activate hlls
```

After creating and activating the new `hlls` bucket type, you can setup your client to start using it. To create a HyperLogLog data structure, you need to specify a bucket/key pair to hold the HyperLogLog. In the Riak client you simply increment and then store the value of the HyperLogLog. There are examples in the [HyperLogLog documentation](http://docs.basho.com/riak/kv/latest/developing/data-types/hyperloglogs/) on how to do these steps.

***Improved Active Anti-Entropy Performance***

We continue to improve Active Anti-Entropy (AAE) Performance by improving the [AAE hash](http://docs.basho.com/riak/kv/latest/learn/concepts/active-anti-entropy/#active-anti-entropy-and-hash-tree-exchange) functionality. Starting with Riak 2.2, AAE will hash the object’s version vector.

- Makes AAE more efficient
- Uses less network and disk IO

***Cluster Job Controls***

Now, in addition to integrated user security, you have the ability to [control commands](http://docs.basho.com/riak/kv/latest/configuring/reference/#cluster-job-controls) that run on your cluster. For critical applications, it may be important for you to ensure that the application is protected from accidental or malicious commands that can affect the overall cluster performance. Things like:

- Protecting production clusters from a new Riak operator who might run `list buckets`
- When you have a secondary cluster for analytics and want to lock out query commands on your primary cluster.

This functionality is `enabled` or `disabled` in `riak.conf`. Below are a few things to know when you enable this functionality:  
![This functionality is enabled or disabled in riak.conf. Below are a few things to know when you enable this functionality](../images/riak-kv-2-2-release-highlights/cluster.job_.code_.jpg)

- All attempts to run the command are denied.
- You can enable or disable features in real-time via riak attach.
- Denied operations are logged.
- Commands are all enabled by default.
- There is a predefined set of commands, individually configurable.

***Improvements to Riak Search (up to 5x faster ingest)***

In Riak KV 2.2, Riak Search has been updated to use Solr 4.10.4. We also improved integration with Solr adding batching and queuing.

- The new batching system for Riak Search makes index calls asynchronous. This allows Solr to process the data in chunks. Riak moves forward accepting new work at the vnode level without waiting for the call to Solr to complete. Batching writes into Solr can provide up to 5X improvement in ingest speed for Solr workloads. [Additional parameters](http://docs.basho.com/riak/kv/latest/configuring/reference/#search) have been added to support Riak Search batching.
- By moving to Solr 4.10.4, we incorporate fixes to Solr as well as improve the overall Riak integration with Solr.

***LZ4 compression***

In Riak 2.2, the default compression for [LevelDB backend](http://docs.basho.com/riak/kv/latest/configuring/backend/#leveldb) is now LZ4 instead of Snappy. This compression is on for new installs by default. LZ4 provides faster compression of data for enhanced cluster performance, as much as 2x faster on write and 4x faster on random reads from/to disk (compared to Snappy compression).

***Debian 8 and Ubuntu 16***

Debian 8 “Jessie” and Ubuntu 16 “Xenial” are now supported in Riak KV 2.2.

***Continued support for Upgrade / Downgrade***

Basho is committed to ensuring that your upgrade experience is as seamless as possible.  While we don’t expect you to have any issues upgrading, we test downgrades to ensure that in the case of an unexpected event, you can downgrade if needed. There are things you will want to consider as you plan your upgrade. Read more about [upgrading](http://docs.basho.com/riak/kv/latest/setup/upgrading/version/) or [downgrading](http://docs.basho.com/riak/kv/latest/setup/downgrade/) in the documentation.

#### **Get Started Now with Riak KV 2.2**

- [Download](http://basho.com/download) Open Source
- [Sign In](http://basho.zendesk.com/) to download Enterprise Edition
- [Learn more](http://docs.basho.com/riak/latest/) about developing with and deploying Riak KV

For a demo or to talk to one of our Riak Solution Architects, please [contact us](http://basho.com/contact/).

Finally, thanks to the many Basho engineers for their continued efforts working with our community and our customers on this new release of Riak KV.

Charlie  
Senior Product Manager – Riak KV, Basho Technologies  
**[@angrycub](https://www.twitter.com/@angrycub)**
