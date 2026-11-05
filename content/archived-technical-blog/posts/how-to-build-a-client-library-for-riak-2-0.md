---
title: "How to Build a Client Library for Riak 2.0"
date: "2015-01-27T06:50:00+00:00"
author: "Luc Perkins"
original_url: "http://basho.com/posts/technical/how-to-build-a-client-library-for-riak-2-0/"
archive_url: "https://web.archive.org/web/20170801115257http://basho.com/posts/technical/how-to-build-a-client-library-for-riak-2-0/"
categories:
  - "Developer Tools"
  - "Releases"
---
*January 27, 2014*

Client libraries are essential to using Riak, and we at Basho have always been proud to have a flourishing [client library ecosystem](http://docs.basho.com/riak/latest/dev/using/libraries/) surrounding Riak. The release of [Riak 2.0](http://docs.basho.com/riak/latest/intro-v20/) has brought a variety of fundamental changes that client builders and maintainers should be aware of, including a variety of [new features](http://docs.basho.com/riak/latest/intro-v20/) that clients should be equipped to utilize, such as [security](http://docs.basho.com/riak/latest/ops/running/authz/) and [Riak Data Types](http://docs.basho.com/riak/latest/dev/using/data-types/). Here, we’ll provide a list of some of those fundamental changes and suggest some approaches to addressing them, including examples from our [official libraries](http://docs.basho.com/riak/latest/dev/using/libraries/#Basho-Supported-Libraries).

## Protocol Buffers API

While Riak continues to have a fully featured [HTTP API](http://docs.basho.com/riak/latest/dev/references/http/) for the sake of backwards compatibility, we do not recommend that you use it to build new client libraries. Instead, we encourage you to design clients to interact with Riak’s [Protocol Buffers API](http://docs.basho.com/riak/latest/dev/references/protocol-buffers/), primarily because internal tests at Basho have shown performance gains of 25% or more when using Protocol Buffers.

The drawback behind using [Protocol Buffers](http://code.google.com/p/protobuf/) is that it’s not as widely known as HTTP and has a bit of a learning curve for those who aren’t familiar with it. But the good news is both that the learning curve is worth it and that Google offers official support for C++, Java, and Python support for PBC while [many other languages](https://github.com/google/protobuf/wiki/Third-Party-Add-ons) have strong community support.

When you start developing your client library, you’ll need to find a Protocol Buffers message generator in the language of your choice and convert a series of [.proto files](https://github.com/basho/riak_pb/tree/develop/src). Once you’ve generated all the necessary messages, you’ll need to implement a transport layer to interface with Riak. A full list of Riak-specific PBC messages can be found [here](http://docs.basho.com/riak/latest/dev/references/protocol-buffers/). The official [Python client](https://github.com/basho/riak-python-client), for example, has a single [RiakPbcTransport](https://github.com/basho/riak-python-client/blob/3c7530f047a3b29a779f7866b7fd3e5b57b113b5/riak/transports/pbc/transport.py#L81) class that handles all message building, sending, and receiving, while the official [Java client](https://github.com/basho/riak-java-client) takes a more piecemeal approach to message building (as shown by the [FetchOperation](https://github.com/basho/riak-java-client/blob/a74a9b99eda5e5f79c4be16dd432e04317b45e84/src/main/java/com/basho/riak/client/core/operations/FetchOperation.java) class, which handles reads from Riak). Once the transport layer is in place, you can start building higher-level abstractions on top.

## Nodes and clusters

Another thing to keep in mind when writing Riak clients is that Riak always functions as a [clustered](http://docs.basho.com/riak/latest/theory/concepts/Clusters/) (and hence multi-[node](http://docs.basho.com/riak/latest/theory/concepts/glossary/#Node)) system, and connecting clients need to be set up to interact with all nodes in a cluster on the basis of each node’s host and port.

While it’s certainly possible to build clients that are intended to interact only with a single node, this means that your client’s users will need to create their own cluster interaction logic. Life will be far easier for your client’s users if your client is able to do things like this:

- periodically [ping](http://docs.basho.com/riak/latest/dev/references/protocol-buffers/ping/) nodes to make sure they’re still online
- recognize when nodes are no longer responding and stop sending requests to those nodes
- provide a load-balancing scheme (or multiple possible schemes) to spread interactions across nodes

In general, you should think of the cluster interaction level as a kind of stateful registry of healthy nodes. In some systems, it might also be necessary to have configurable parameters for connections to Riak, e.g. minimum and/or maximum concurrent connections.

## Bucket types

Prior to 2.0, the location of objects in Riak was determined by [bucket](http://docs.basho.com/riak/latest/theory/concepts/Buckets/) and [key](http://docs.basho.com/riak/latest/theory/concepts/keys-and-values/#Keys). In version 2.0, [bucket types](http://docs.basho.com/riak/latest/dev/advanced/bucket-types/) were introduced as a third namespacing layer in addition to buckets and keys. Connecting clients now need to either specify a bucket type or use the [default](http://docs.basho.com/riak/latest/dev/advanced/bucket-types/#Default-Bucket-Properties) type for all K/V operations. Although creating, listing, modifying, and activating bucket types can be accomplished only via the [command line](http://docs.basho.com/riak/latest/dev/advanced/bucket-types/#Managing-Bucket-Types-Through-the-Command-Line), your client should provide an interface for seeing which bucket properties are associated with a bucket type.

One of the changes to be aware of when building clients is that Riak has changed its querying structure to accommodate bucket types. When performing K/V operations, you now need to specify a bucket type in addition to a bucket and a key. This means that the structure of all K/V operations needs to be modified to allow for this. We’d also recommend enabling users to perform K/V operations without specifying a bucket type, in which case the default type is used. In the official Python client, for example, the following two reads are equivalent:  
 `client.bucket(‘fruits’).get(‘apple’)  
client.bucket_type(‘default’).bucket(‘fruits’).get(‘apple’)`

## Dealing with objects and content types

One of the tricky things about dealing with objects in Riak is that objects can be of any data type you choose (Riak Data Types are a different matter, and covered in the section below). You can store JSON, XML, raw binaries, strings, mp3s and MPEGs (though you should probably consider [Riak CS](http://basho.com/riak-cloud-storage/) for larger files like that), and so on. While this makes Riak an extremely flexible database, it means that clients need to be able to work with a wide variety of content types.

All objects stored in Riak must have a specified content type, e.g. **application/json, text/plain, application/octet-stream**, etc. While a Riak client doesn’t need to be able to handle all data types, a client intended for wide use should be able to handle at least the following:

- JSON
- XML
- plain text
- binaries

You should also strongly consider building automatic type handling into your client. When the official Ruby and Python clients, for example, read JSON from Riak, they automatically convert it to hashes and dicts (respectively). The Java client, to give another example, automatically converts [POJO](http://en.wikipedia.org/wiki/Plain_Old_Java_Object)s to JSON by default and enables you to automatically convert stored JSON to [custom POJO classes](http://basho.github.io/riak-java-client/2.0.0/) when fetching objects, which enables you to easily interact with Riak in a type-specific way. If you’re writing a client in a language with strong type safety, this would be a good thing to offer users.

Another important thing to bear in mind: all of your client interactions with Riak should be [UTF-8](http://en.wikipedia.org/wiki/UTF-8) compliant, not just for the data stored in objects but also for things like bucket, key, and bucket type names. In other words, with your client it should be possible to store an object in the key **Möbelträgerfüße** in the bucket **tête-à-tête**.

## Conflict resolution

If you’re using either Riak Data Types or Riak’s strong consistency subsystem, you don’t have to worry about siblings because those features by definition do not involve sibling creation or resolution. But many users of your client will want to use Riak as an eventually consistent system, which means that they will need to create their own conflict resolution logic.

In essence, your users’ applications need to make intelligent, use-case-specific decisions about what to do when the application is confronted with siblings. Most fundamentally, this means that your client needs to enable objects to have multiple sibling values. In the official Python client, for example, each object of class RiakObject has parameters that you’d expect, like content\_type, bucket, and data, but it also has a siblings parameter that returns a list of sibling values.

In addition to enabling objects to have multiple values, we also strongly recommend providing some kind of helper logic that enables users to easily apply their own sibling resolution logic. What type of interface should be provided? That will depend heavily on the language. In a functional language, for example, that might mean enabling users to specify filtering functions that whittle the siblings down to a single “correct” value. To see conflict resolution in our official clients in action, see our tutorials for Java, Ruby, and Python.

## Riak Data Types

In version 2.0, Riak added support for conflict-free replicated data types (aka [CRDTs](http://dl.acm.org/citation.cfm?id=2050642)), which we call [Riak Data Types](http://docs.basho.com/riak/latest/theory/concepts/crdts/). These five special Data Types—flags, registers, counters, sets, and maps—enable you to forgo things like application-side conflict resolution because Riak handles the resolution logic for you (provided that your data can be modeled as one of the five types). What separates Riak Data Types from other Riak objects is that you interact with them *transactionally*, meaning that changing Data Types involves sending messages to Riak about what changes should be made rather than fetching the whole object and modifying it on the client side.

This means that your client interface needs to enable users to modify the Data Types as much as they need to on the client side before committing those changes all at once to Riak. So if an application needs to add five counters to a map and remove items from three different sets within that map, it should be able to commit those changes with one message to Riak. The official Python client, for example, has a [store()](https://github.com/basho/riak-python-client/blob/master/riak/datatypes/datatype.py#L107) function that sends all client-side changes to Riak at once, plus a [reload()](https://github.com/basho/riak-python-client/blob/master/riak/datatypes/datatype.py#L64) function that fetches the current value of the type from Riak (with no regard to client-side changes).

## Security

One of the most important features introduced in Riak 2.0 is [security](http://docs.basho.com/riak/latest/ops/running/authz/). When enabled, all clients connecting to Riak, regardless of which [security source](http://docs.basho.com/riak/latest/ops/running/security-sources/) is chosen, must communicate with Riak over a secure SSL connection rooted in an [x.509](http://en.wikipedia.org/wiki/X.509)-certificate-based Public Key Infrastructure (PKI). If you want your client’s users to be able to take advantage of Riak security, you’ll need to create an SSL interface. Fortunately, there are [OpenSSL](https://www.openssl.org/) (and other) libraries in all major languages. To see SSL in action in our official clients, see our tutorials for [Java](http://docs.basho.com/riak/latest/dev/advanced/client-security/java/), [Ruby](http://docs.basho.com/riak/latest/dev/advanced/client-security/ruby/), [Python](http://docs.basho.com/riak/latest/dev/advanced/client-security/python/), and [Erlang](http://docs.basho.com/riak/latest/dev/advanced/client-security/erlang/).

Although not strictly necessary, we also recommend enabling users to specify [certificate revocation lists](http://docs.basho.com/riak/latest/dev/advanced/client-security/python/#Specifying-a-Certificate-Revocation-List), [OCSP checking](http://docs.basho.com/riak/latest/dev/advanced/client-security/ruby/#Online-Certificate-Status-Protocol), and [cipher lists](http://docs.basho.com/riak/latest/dev/advanced/client-security/python/#Specifying-Ciphers).

## Features That Don’t Require Client Changes

The following features that became available in Riak 2.0 shouldn’t require any changes to client libraries:

- [Strong consistency](http://docs.basho.com/riak/2.0.2/dev/advanced/strong-consistency/) — While adding strong consistency has entailed a lot of changes within Riak itself, K/V operations involving strongly consistent data function just like their eventually consistent counterparts in most respects. The one small exception is that performing object updates without first fetching the object will necessarily fail because the initial fetched obtains the object’s [causal context](http://docs.basho.com/riak/2.0.2/theory/concepts/context/), which is necessary for strongly consistent operations. It may be a good idea to add this requirement to your client documentation.
- [New configuration system](http://docs.basho.com/riak/2.0.2/ops/advanced/configs/configuration-files/) — Configuration has been drastically simplified in Riak 2.0, but these changes won’t have a direct impact on client interfaces.
- [Dotted version vectors](http://docs.basho.com/riak/2.0.2/theory/concepts/context/#Dotted-Version-Vectors) — While dotted version vectors (DVVs) are superior to the older [vector clocks](http://docs.basho.com/riak/2.0.2/theory/concepts/context/#Vector-Clocks) in preventing problems like [sibling explosion](http://docs.basho.com/riak/2.0.2/theory/concepts/context/#Sibling-Explosion), client libraries interact with DVVs just like they interact with vector clocks. In fact, our Protocol Buffers messages still use a vclock field for both vector clocks and DVVs, for the sake of backward compatibility.

## How to Get Help

Building a 2.0-compliant Riak client has some non-trivial aspects but can be an exciting and rewarding project. Fortunately there are a variety of venues where you can get help, both from Basho engineers and from others in the Riak community.

For inspiration and education, the official Basho Riak clients in the GitHub repos are a good place to start. If you run into trouble, though, we highly recommend the [Riak mailing list](http://lists.basho.com/mailman/listinfo/riak-users_lists.basho.com). There could very well be other client builders and maintainers working through a similar problem.

[Luc Perkins](https://twitter.com/lucperkins)
