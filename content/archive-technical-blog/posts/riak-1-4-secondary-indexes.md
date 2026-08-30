---
title: "Riak 1.4: Secondary Indexes"
date: "2013-07-11T09:00:05+00:00"
author: "John Daily"
original_url: "http://basho.com/posts/technical/riak-1-4-secondary-indexes/"
archive_url: "https://web.archive.org/web/20170407130023http://basho.com/posts/technical/riak-1-4-secondary-indexes/"
categories:
  - "Releases"
  - "Data Modeling"
---
*July 11, 2013*

*To learn more about what’s new in Riak 1.4, [sign up for our webcast](http://info.basho.com/Riak1.4_July12.html) on July 12th at 11am PT/2pm ET*

With the [introduction of Riak 1.4](http://basho.com/basho-announces-availability-of-riak-1-4), Basho offers developers new ways to leverage secondary indexes (often referred to as **2i**). This is a short review of what they are and what has been added.

## Secondary indexes in Riak

Values in Riak are treated as opaque, although optional add-ons such as Riak Search and Yokozuna can index the contents.

With two of the supported storage backends (LevelDB and Memory), developers can add their own indexes for querying. These can be numeric or string values, matched as exact values or ranges, and can have as much or as little to do with the stored value as the developer wishes.

Primary key lookups will always be the fastest way to retrieve values from Riak, but 2i is a useful way to label and retrieve data.

## What has changed with Riak 1.4?

Previously, results from 2i queries were presented as a comprehensive list of unordered keys. Depending on the size of the result set, this could be awkward (or impossible) for a client application to handle.

With 1.4, the following features have been added:

- Pagination and streaming are available on request.
- Results are now sorted: first by index value, then by keys.
- If requested as part of a range query, the matched index value will be returned alongside each key.

### 2i illustrated

Here is an example of a range query via HTTP. Pagination is specified via `max_results=5` and the return of matched index values via `return_terms=true`.

In this case we are querying a small Twitter firehose data set; each tweet was added to Riak with nested hashtag values as indexes. The query is designed to match hashtags in the range `ri` (inclusive) to `ru` (exclusive).

Requested URL:  
`http://localhost:10018/buckets/tweets/index/hashtags_bin/ri/ru?max_results=5&return_terms=true`

JSON results:  
 `{  
"continuation": "g2gCbQAAAAdyaXBqYWtlbQAAABIzNDkyMjA2ODcwNTcxMjk0NzM=",  
"results": [`

{  
“rice”: “349222574510710785”  
},  
{  
“rickross”: “349222868095217664”  
},  
{  
“ridelife”: “349221819552763905”  
},  
{  
“ripjake”: “349220649341952001”  
},  
{  
“ripjake”: “349220687057129473”  
}

]  
}

The `continuation` value is necessary to retrieve the next page of results, and as expected the results are sorted by index value and key.

## Where to find more information?

Basho’s docs site has been updated for 1.4:

- ~~http://docs.basho.com/riak/latest/tutorials/Secondary-Indexes—Examples/~~
- ~~http://docs.basho.com/riak/latest/references/apis/http/HTTP-Secondary-Indexes/~~
- ~~http://docs.basho.com/riak/latest/dev/references/protocol-buffers/secondary-indexes/~~

[John R. Daily](https://twitter.com/macintux)
