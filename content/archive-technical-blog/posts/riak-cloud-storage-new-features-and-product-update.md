---
title: "Riak Cloud Storage – New Features and Product Update"
date: "2012-08-21T00:00:00+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/riak-cloud-storage-new-features-and-product-update/"
archive_url: "https://web.archive.org/web/20170801115128http://basho.com/posts/technical/riak-cloud-storage-new-features-and-product-update/"
categories:
  - "Releases"
  - "Cloud & Deployment"
---
*August 21, 2012*

Earlier this year we launched [Riak CS](http://basho.com/products/riakcs/) – simple, available cloud storage built on Riak. We gave it an S3-compatible API, made it multi-tenant, and added per-user reporting on network and storage utilization. Riak CS provides the core features to build public or private clouds that are distributed, fault-tolerant and easy to scale.

Since then, we’ve rolled out [a startup program](http://basho.com/products/riak-cs-for-startups/) to make Riak CS affordable for earlier-stage shops. And we’ve talked to a number of companies who wanted to license Riak CS based on the amount of storage they need, rather than the number of nodes, so now you can do that too. (Get in touch if you [want a quote](http://info.basho.com/RiakCS_quote.html).) Riak CS docs are now also publicly [available on our wiki](http://wiki.basho.com/Riak-CS.html).

Today we’re announcing some new features and additions to Riak CS, including more options for user admin, auth and object metadata, plus improved stats and troubleshooting. We’ll walk thru the Riak CS architecture, operations and new functionality in an [upcoming webcast](http://info.basho.com/webinar1.1riakcs.html), or read on.

## New in Riak CS

### Better User Administration

We’ve beefed up the Riak CS user API so admins can now list all users, issue new credentials to a user, or disable a user. We’ve also got new configuration options to restrict user creation to admins or let anyone create a user directly.

### List All Objects in a Bucket Much Faster

User objects in Riak CS are stored in flat namespaces called “buckets”. We sped up one of the most common bucket operations: listing all of its objects. Riak CS now uses MapReduce to look up objects, yielding significant performance gains.

### Arbitrary Metadata

One of our top customer requests. Now you can store some additional metadata with your Riak CS objects – whatever is most useful to you.

### New Basic Health Check

If you’ve ever set up Riak, you’ve probably used the basic health check to test Riak nodes. Now you can send an HTTP “ping” to Riak CS nodes as well to make sure they are responsive. The “ping” will also fail if the Riak CS node can’t reach the underlying Riak database (Riak CS nodes have a 1×1 mapping onto Riak nodes).

### Better Inspection and Troubleshooting

We have added DTrace probing in Riak CS and we are working on SmartOS packaging. We will also be working on packaging for other platforms that support DTrace. Once these packages are available it should help operators who use DTrace platforms troubleshoot any issues with Riak CS and have more visibility into their stack. We also now expose more stats information on the Riak CS runtime by HTTP request.

### Improved S3 API Coverage

We also added support for query parameter authentication, increasing compliance with [S3’s REST Authentication scheme](http://s3.amazonaws.com/doc/s3-developer-guide/RESTAuthentication.html). This means that Riak CS users can now authenticate thru a request header or a URL-encoded query string parameter.

Stay tuned because we’re hard at work on the next Riak CS features and improvements. What do you want to see? We’d love to [hear from you](http://basho.com/contact/riakcs/).
