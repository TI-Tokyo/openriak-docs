---
title: "Customer.io Gains 6x Speed Improvement by Moving from MongoDB to Riak"
date: "2013-08-28T18:42:53+00:00"
author: "Basho"
original_url: "http://basho.com/posts/technical/customer-io-gains-6x-speed-improvement-by-moving-from-mongodb-to-riak/"
archive_url: "https://web.archive.org/web/20170408080024http://basho.com/posts/technical/customer-io-gains-6x-speed-improvement-by-moving-from-mongodb-to-riak/"
categories:
  - "Case Studies"
  - "Performance"
---
*August 28, 2013*

[Customer.io](http://customer.io/) is passionate about helping their customers grow happy customers. Their focus is on creating genuine, relevant interactions for their customers. Of course, happy customers expect great performance. As Customer.io continues to rapidly grow, they are putting in place the foundation to deliver on those commitments.

Yesterday, Customer.io announced that they upgraded their architecture – moving from MongoDB to Riak. As described in their recent blog post, the move to Riak has provided an immediate and dramatic performance boost. Some performance highlights include:

- User segmentation can run anywhere from 6x faster (raw performance) to 100x faster, taking into account that customer requests are now parallelizable. (To send more relevant, timely emails, Customer.io enables subsets of people to be grouped around similar characteristics.)
- Processing time was reduced from 3 hrs to 30 minutes on a large segment.
- Customer.io launched a new feature that shows percentage complete.

In addition from gaining the inherent benefits from Riak as a scalable, distributed system, Customer.io also implemented Go, an increasingly popular programming language. Go adds powerful message queuing, systems programming, and exceptional concurrency.

You can view the entire blog post from Customer.io here: [customer.io/blog/Segment-customer-data-faster.html](http://customer.io/blog/Segment-customer-data-faster.html)

[Basho](http://www.twitter.com/basho)
