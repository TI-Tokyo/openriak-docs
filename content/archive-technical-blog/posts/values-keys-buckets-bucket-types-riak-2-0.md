---
title: "Values, Keys, Buckets, Bucket Types – Riak 2.0"
date: "2014-12-23T11:50:42+00:00"
author: "Tyler Hannan"
original_url: "http://basho.com/posts/technical/values-keys-buckets-bucket-types-riak-2-0/"
archive_url: "https://web.archive.org/web/20170801120846http://basho.com/posts/technical/values-keys-buckets-bucket-types-riak-2-0/"
categories:
  - "Data Modeling"
  - "Releases"
---
*December 23, 2014*

This is a continuation in our blog series covering Riak 2.0. Below are links to the previously covered blogs and we continue with a discussion on Values, Keys, Buckets and Bucket Types.

- [Riak 2.0 – New Capabilities, New Use Cases, Available for Download](http://basho.com/riak-2-0-new-capabilities-new-use-cases-available-for-download/)
- [Write it like Riak; Query it Like Solr](http://basho.com/write-it-like-riak-query-it-like-solr/)
- [Riak Security 2.0: Not Just a Firewall Anymore](http://basho.com/riak-security-2-0-not-just-a-firewall-anymore/)
- [Distributed Data Types – Riak 2.0](http://basho.com/distributed-data-types-riak-2-0/)
- [Strong Consistency in Riak 2.0](http://basho.com/strong-consistency-in-riak-2-0/)

## Bucket Types

If you have tested Riak 2.0, or used it in production, you will also be aware of a new feature called Riak Bucket Types

The *[Using Bucket Types](http://docs.basho.com/riak/latest/dev/advanced/bucket-types/)* documentation covers the implementation, usage, and configuration of Bucket Types in great detail. Throughout the documentation there are code samples (e.g. *[Using Data Types](http://docs.basho.com/riak/latest/dev/using/data-types/)*) including code for creating the bucket types associated with each individual Riak Data Types.

Bucket types are a major improvement over the older system of bucket configuration. The ability to define a bucket configuration, and then change the configuration if necessary, for entire group of buckets, is a powerful new way to consider data modeling. In addition, bucket types are more reliable as buckets that have a given type (or configuration) only have their properties change when the type is changed. Previously, it was possible to change the properties of a bucket only through client requests.

In prior versions of Riak, bucket properties were altered by clients interacting with Riak…in contrast, bucket types are an operational concept. The `riak-admin bucket-type` interface enables Riak users to manage bucket configurations at an operational level, without recourse to the Riak clients.

In versions of Riak prior to 2.0, all queries were made to a bucket/key pair as in the following example:  
 `curl http://localhost:8098/buckets/my_bucket/keys/my_key`

Now in Riak 2.0 with the addition of bucket types, there is an additional namespace on top of buckets and keys. The same bucket name can be associated with completely different data if it is used in accordance with a different bucket type.  
 `curl http://localhost:8098/types/type1/buckets/my_bucket/keys/my_key  
curl http://localhost:8098/types/type2/buckets/my_bucket/keys/my_key`

If a request is made to a bucket/key pair without a specified bucket type, `default` will be used in place of a bucket type. The following request are identical.  
 `curl http://localhost:8098/buckets/my_bucket/keys/my_key  
curl http://localhost:8098/types/default/my_bucket/keys/my_key`

## In Summary

Bucket types allow groups of buckets to share configuration details. This allows Riak users, and administrators, to manage bucket properties more efficiently than in the older configuration systems that were based on [bucket properties](http://docs.basho.com/riak/latest/dev/using/basics/#bucket-properties-and-operations).

For a broader discussion of application data modeling, and using Riak as a data store, the *[Building Applications with Riak](http://docs.basho.com/riak/latest/dev/using/application-guide/)* documentation covers these concepts, and more, in great detail.

Riak 2.0 was the culmination of substantial effort by the Basho team. A particular focus was adding functionality (like Riak Search) that had been requested by customer. In addition, this release further the Basho commitment to providing a scalable and available database that has the operational simplicity for which Riak is known.

It just works.

[Tyler Hannan](http://twitter.com/tylerhannan)
