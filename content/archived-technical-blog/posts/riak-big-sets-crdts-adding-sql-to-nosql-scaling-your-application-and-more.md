---
title: "Riak Big Sets, CRDTs, Adding SQL to NoSQL, Scaling your application, and more"
date: "2016-10-26T20:02:41+00:00"
author: "Dorothy Pults"
original_url: "http://basho.com/posts/technical/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/"
archive_url: "https://web.archive.org/web/20170705011055http://basho.com/posts/technical/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/"
categories:
  - "Data Modeling"
---
The Basho team of distributed systems engineers continues to develop new Riak functionality to help companies build innovative applications. A few members of the Basho team recently took a break from their day jobs to share some of the details of their recent work at the Erlang User Conference in Stockholm. In case you missed them, we wanted to share videos of these presentations. (Hint: They aren’t just for people passionate about Erlang)

[Russell Brown](#crdts) provided an update on the research and implementation of CRDTs and his recent work on expanding CRDT support for bigger sets in Riak. [Gordon Guthrie](#moresql) showed how NoSQL really means “not only SQL” and explained the new capabilities and techniques in Riak that are specifically optimized for time series data. [Torben Hoffmann](#startup) gave some hints on application architectures that have the flexibility to serve both the short and long term needs of a start-up. [Andy Till](#erlyberly) explained how to debug Erlang, Elixir, and LFE applications using tracing with Erlyberly. Plus, [Magnus Kessler](#riak-data-types) leads a hands-on tutorial of Riak Distributed Data Types (CRDTs).  
  
See more information on each of these presentations below.

Grab your popcorn and enjoy!

### [Big(ger) Sets: Making CRDT Sets Scale in Riak](http://www.erlang-factory.com/euc2016/russell-brown)

Russell Brown  
Eventually Consistent CRDTist at Basho

GitHub: [russelldb](http://www.github.com/russelldb)

![video-bigger-sets-making-crdt-sets-scale-in-riak](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/video-bigger-sets-making-CRDT-sets-scale-in-riak.jpg)

[![play video](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/youtube-48.png) Watch Video](https://www.youtube.com/embed/f20882ZSdkU?autoplay=1&rel=0)

**Presentation overview:**

This talk looks at the original implementation of Riak Distributed Data Types (CRDTs) and shows a new approach to designing CRDTs in Riak from the ground up that comes with a great deal more scale and performance.  
  
**Talk objective:**

Illustrate the engineering challenges inherent in taking research papers into a real world product. This is both a cautionary tale and a showcase of our recent work.

### [From NoSQL to More SQL – Adding Structure and Queriability to Riak](http://www.erlang-factory.com/euc2016/gordon-guthrie)

Gordon Guthrie  
Senior Engineer @ Basho and Serial Entrepreneur  
GitHub: [gordonguthrie](http://www.github.com/gordonguthrie)  Twitter: [@gordonguthrie](http://www.twitter.com/gordonguthrie)

![video-from-nosql-to-more-sql-adding-structure-and-queriability-to-riak](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/video-from-nosql-to-more-sql-adding-structure-and-queriability-to-riak.jpg)

[![play video](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/youtube-48-831c2bca.png) Watch Video](https://www.youtube.com/embed/uN0GIPWiRYo?autoplay=1&rel=0)

**Presentation overview:**

Riak is an industry leader in the NoSQL space but with the new Riak Time Series offering more traditional tools like native SQL querying is being added. This talk will look at meta-programming being used in a gossip-based cluster to build an adaptive Riak that reconfigures itself to handle structured data – and how we use standard SQL to interrogate that data.  
  
**Talk objective:**

Explain the new capabilities and techniques in Riak TS

### [Winning as a Start-Up by Failing Fast](http://www.erlang-factory.com/euc2016/torben-hoffmann)

Torben Hoffmann  
Chief Architect at Basho  
GitHub: [LeHoff](http://www.github.com/LeHoff)   Twitter: [@LeHoff](http://www.twitter.com/LeHoff)

![video-winning-as-a-start-up-by-failing-fast](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/video-winning-as-a-start-up-by-failing-fast.jpg)

[![play video](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/youtube-48-831c2bca.png) Watch Video](https://www.youtube.com/embed/FF5GaL2sqCI?autoplay=1&rel=0)

**Presentation Overview:**

Scalability is a word often used to describe Riak KV & Erlang/Elixir, but it is not the first concern for a start-up. Scalability is a rich man’s problem.

Sure, you need a stack that can scale… when you are ready!

Until that point, you need something that is flexible and allows you to iterate over a lot of experiments in a short period of time.

Experiments with software often involve errors. Erlang/Elixir has a unique approach to dealing with errors that lend itself well to do the experiments and, at the same time, keep a start-up rolling. We will look into how you should architect your software to leverage this, so you work with the BEAM and not against it.

Riak KV is a scalable, reliable NoSQL database that takes the Erlang philosophy regarding failures to heart – don’t ignore failure, embrace failure!!

But wait a second… if scalability is a rich man’s problem, what role does Riak KV play for a start-up?

This talk will go into how to approach this dilemma by attacking it with an architecture that has the flexibility that serves both the short and long term needs of a start-up.  
  
**Talk objective:**

Show how Riak KV and Erlang/Elixir can help a start-up focus on the most important thing: conducting experiments fast to get to a viable business model before the money runs out.

### [Trace Debugging With ErlyBERLY](http://www.erlang-factory.com/euc2016/andy-till)

Andy Till  
Riak Time Series Database Developer  
GitHub: [andytill](http://www.github.com/andytill)  Twitter: [@andy\_till](http://www.twitter.com/andy_till)

![video-trace-debugging-with-erlyberly](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/video-trace-debugging-with-erlyberly.jpg)

[![play video](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/youtube-48-831c2bca.png) Watch Video](https://www.youtube.com/embed/RAOO53vYuxo?autoplay=1&rel=0)

**Presentation overview:**

The BEAM virtual machine has flexible and powerful tooling from introspection, statistics, and debugging without affecting the running application. Erlyberly is an ongoing project to lower the barrier for entry for using these capabilities which focus on tracing.  
  
**Talk objective:**

Learn how to debug Erlang, Elixir, and LFE applications using tracing with erlyberly.

### [Tutorial: No more fighting with your siblings. Riak distributed Data Types (CRDTs) remove the stress](http://www.erlang-factory.com/euc2016/magnus-kessler)

![CRDTs in Riak](../images/riak-big-sets-crdts-adding-sql-to-nosql-scaling-your-application-and-more/slide-crdts.png)

[Slides](http://www.erlang-factory.com/static/upload/media/1473243122628734magnuskesslereuc_2016_crdt_tutorial.pdf) (no video available)

Magnus Kessler  
Client Services Engineer @ Basho

**Tutorial Overview:**  
Choosing a highly available database can mean sacrificing some consistency of data during failure scenarios, but it should not mean data loss. Databases designed with partition tolerance and eventual consistency in mind can offer multiple ways to handle conflict resolution, but some can be difficult to reason about or so be simple that you lose the configurability you need.

In Riak KV, we recommend you allow ‘siblings’ or multiple versions of data to be stored whenever there is no way to determine the correct latest version. But once you have multiple siblings, how do you get back to the single correct and consolidated version of data your application is expecting to use?

Riak Data Types are distributed data structures designed to provide deterministic resolution logic, removing the need for the application developer to write such functionality in an ad-hoc manner or multiple varying ways across a large project.

**Summary:**

We will demonstrate why Riak KV would generate siblings and then implement each of the Riak Data Types available in Riak KV to solve the challenges of working with a highly available and eventually consistent database.

### Next Steps

If you found these presentations interesting, you might also enjoy these blogs:

[Running Riak in Docker](./running-riak-in-docker.md)  
[Basho’s Spark-Riak Connector 1.6.0 Now Available](./bashos-spark-riak-connector-1-6-0-now-available.md)  
[NoSQL Riak TS Gets JDBC Driver Inspired by SQL](./nosql-riak-ts-gets-jdbc-driver-inspired-by-sql.md)

4 part series by Damien Krotkine, Ivan Paponov at booking.com

[Using Riak as Events Storage – Part 1](https://medium.com/booking-com-development/using-riak-as-events-storage-part-1-9b423f0ef97a)  
[Using Riak as Events Storage – Part 2](https://medium.com/booking-com-development/using-riak-as-events-storage-part-2-b1a3db5ef139)  
[Using Riak as Events Storage – Part 3](https://medium.com/booking-com-development/using-riak-as-events-storage-part-3-a79d629790c7)  
[Using Riak as Events Storage – Part 4](https://medium.com/booking-com-development/using-riak-as-events-storage-part-4-43d088f80b7c)
