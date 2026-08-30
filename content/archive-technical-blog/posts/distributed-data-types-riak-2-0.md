---
title: "Distributed Data Types – Riak 2.0"
date: "2014-10-23T14:30:46+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/distributed-data-types-riak-2-0/"
archive_url: "https://web.archive.org/web/20170429184634http://basho.com/posts/technical/distributed-data-types-riak-2-0/"
categories:
  - "Data Modeling"
  - "Architecture & Distributed Systems"
  - "Releases"
---
In a previous [post](http://basho.com/riak-2-0-new-capabilities-new-use-cases-available-for-download/) we briefly introduced Riak 2.0 data types. The addition of these distributed Data Types simplifies application development by automatically handling sibling resolution. This means developers can spend less time thinking about the complexities of vector clocks and sibling resolution and, instead, let Data Types support their applications’ data access patterns.

Understanding these data types requires a brief trip through history…

## Riak 1.4 Counters

Riak 1.4 introduced counters as the first data types. Prior to 1.4 we’ve always said: “Your data is opaque to Riak,” — and it still can be — but with the addition of counters that is not longer the case. Riak knows what is stored in a counter key, and how to increment and decrement it through the counter API. It isn’t necessary to fetch, mutate, or put a counter. Instead you just incremented by 5 or decremented by 100. Vector Clocks, as discussed in the post entitled [*Clocks Are Bad, or, Welcome to the Wonderful World of Distributed Systems*](http://basho.com/clocks-are-bad-or-welcome-to-distributed-systems/), as Riak knew how to merge concurrent writes there was never a sibling created.

Counters are very valuable, but you can not build many applications on just counters. Now, in Riak 2.0, we’ve added more data types. We believe that, with the addition of these data types you can model many applications’ data storage needs with greater simplicity, and never have to write sibling merge functions again.

## What are CRDTs?

You may have heard a Basho presentation, or blog post, reference “CRDTs”. CRDT stands for (variously) Conflict-free Replicated Data Type, Convergent Replicated Data Type, Commutative Replicated Data Type, and others. The key, repeated, phrase is “Replicated Data Types”.

Replication is inherent in Riak. It is what the n-value defines. It is part of what lends to the availability and fault tolerance characteristics that Riak provides. Data Types are a common construct in computing. Sets, Bags, Lists, Registers, Maps, Counters…etc.

That leaves us to consider the “C”.

## Conflict Free, or “Opaque No More”

Riak is an eventually consistent system. It leans, very much, towards the AP end of the CAP spectrum. (For more reading on the topic, the [Practical Tradeoffs](http://littleriakbook.com/#toc_8) section of *A Little Riak Book* is particularly illuminating). This availability is achieved with mechanisms like sloppy quorum writes to fallback nodes. However, even without partitions and many nodes, interleaved or concurrent writes can lead to conflicts. Traditionally, Riak keeps all values and presents them to the user to resolve. The client application must have a deterministic way to resolve conflicts. It might be to pick the highest timestamp, or union all the values in a list, or something more complex. Whatever approach is chosen, it is ad-hoc, and created specifically for the data model and application at hand.

With Riak data types, there is still “conflict”. However, the resolution for that conflict is inherent and part of the data type’s design. The data types for Riak 2.0 converge automatically, at write and read time, on the server. If a client application can model its data using the data types provided, no sibling values will be seen and there is no longer a need to write ad-hoc, custom merge functions.

When modeling an applications data domain in a programming language, developers are familiar with composing state from a few primitive data types. Riak Data Types give the developer that power back and expressivity, and relieve them of the burden of design and testing deterministic merge functions. The key is that the data is no longer opaque to Riak. When the Data Types API is leveraged, Riak “knows” what type of thing is being stored and is able to perform the merge automatically.

When reading a Data Type from Riak, you will only ever see a single value. That value is still eventually consistent, but it will be as correct as it can be given the amount of entropy in the database. When the system is stable, all values will converge on a single, deterministic, correct value.

## What Data Types Are Available?

Riak 2.0 includes the following Data Types:

- **Counters:** as in Riak 1.4
- **Flags:** enabled/disabled
- **Sets:** collections of binary values
- **Registers:** named Binary values with values also binary
- **Maps:** a collection of fields that supports the nesting of multiple Data Types

The conflict resolution, as discussed above, is intrinsic to the Data Type itself. This table provides greater detail.

| Data Type | Use Cases | Conflict Resolution Rule |
| --- | --- | --- |
| Counters (v1.4) | - Track number of page likes - Track number of followers | Each actor keeps and independent count for increments and decrements. Upon merge, the pairwise maximum of any two actors will win (e.g. if one actor holds 172 and other holds 173, 173 will win upon merge) |
| Flags | - Has a tweet been re-tweeted - Is a user eligible for preferred pricing | Enable wins over disable |
| Sets | - List of items in an online shopping cart - UUIDs of a user’s friends in a social networking app | If an element is concurrent added and removed the add will win |
| Registers | - Store user profile names - Store primary search location for a search engine user | The most chronologically recent value wins, based on timestamps |
| Maps | - Store user profile data comnposed - register: user\_name - flag: email\_notifications - counter: site\_visits | If a field is concurrently added, or updated and removed, the addd / update will win |

A new version of Riak, with new Data Types, allowing you to model your application in more expansive ways. Take these Data Types for a spin and be sure to let us know how you use them in your applications.

## Resources

- [Using Data Types](http://docs.basho.com/riak/latest/dev/using/data-types/)
- [Data Modeling with Riak Data Types](http://docs.basho.com/riak/latest/dev/data-modeling/data-types/)
- [Riak Data Types – Theory & concepts](http://docs.basho.com/riak/latest/theory/concepts/crdts/)

[Basho Team](http://twitter.com/basho)
