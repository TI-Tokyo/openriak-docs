---
title: "Booking.com: Using Riak as Events Storage – Part 4"
date: "2017-02-07T12:35:40+00:00"
author: "Dorothy Pults"
original_url: "http://basho.com/posts/technical/booking-com-using-riak-as-events-storage-part-4/"
archive_url: "https://web.archive.org/web/20170211193943http://basho.com/posts/technical/booking-com-using-riak-as-events-storage-part-4/"
categories:
  - "Case Studies"
---
[Booking.com](http://booking.com) is the world’s leading online accommodation provider,[![booking.com and Basho](../images/booking-com-using-riak-as-events-storage-part-4/booking-1.png)](../images/booking-com-using-riak-as-events-storage-part-4/booking-1.png) operating across 220+ countries in 43 languages. They process billions of events per day, streaming at more than 100MB per second, and adding more than 6 TB of data per day. These events are schema-less and difficult for standard analytics tools to handle.

Two engineers at Booking.com, Damien Krotkine and Ivan Poponov, have published a 4 part blog series entitled “Using Riak as Events Storage”.  In this blog series, they describe the Booking.com data pipeline and go into detail on their events, data flow, data design, real-time events analysis, and optimizing data transformation. Part 4 in the series was recently published and explains how to use post-commit hooks to apply transformations to event data in Riak without using MapReduce jobs. We highly recommend that you start with Part 1 and read the blog posts sequentially. Each blog post builds on information in the previous post.

[Using Riak as Events Storage – Part 1](https://blog.booking.com/using-riak-as-events-storage-part1.html): explains how Booking.com collects and stores events from its back-end into central storage, and why they chose [Riak](http://basho.com/products) for events storage.

[Using Riak as Events Storage – Part 2](https://blog.booking.com/using-riak-as-events-storage-part2.html): explains how Booking.com pushes data to Riak, how they read it, and how they perform real-time data processing to do event analysis.

[Using Riak as Events Storage – Part 3](https://blog.booking.com/using-riak-as-events-storage-part3.html): explains how Booking.com applies transformations to event data stored in Riak without the data leaving the cluster.

[Using Riak as Events Storage – Part 4](https://blog.booking.com/using-riak-as-events-storage-part4.html): explains how Booking.com uses post-commit hooks to apply transformation to event data stored in Riak.

Other Resources:

[Riak KV Technical Overview](http://info.basho.com/rs/721-DGT-611/images/RiakKV%20Enterprise%20Technical%20Overview-6page.pdf)  
[Riak TS Technical Overview](http://info.basho.com/rs/721-DGT-611/images/RiakTS-Enterprise-Technical-Overview.PDF)  
[Basho Academy](http://academy.basho.com)  
[Riak Documentation](http://docs.basho.com)  
[Contact Us for a techtalk](http://basho.com/contact)  
Dorothy Pults  
@deepults
