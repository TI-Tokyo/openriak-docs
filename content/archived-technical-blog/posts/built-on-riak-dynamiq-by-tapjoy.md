---
title: "Built on Riak: Dynamiq by Tapjoy"
date: "2015-08-11T06:46:51+00:00"
author: "Stephen Condon"
original_url: "http://basho.com/posts/technical/built-on-riak-dynamiq-by-tapjoy/"
archive_url: "https://web.archive.org/web/20170629035355http://basho.com/posts/technical/built-on-riak-dynamiq-by-tapjoy/"
categories:
  - "Case Studies"
---
It’s a pleasure to see when Riak users find new and effective ways to build innovative applications on top of the distributed, open source system that is Riak. The team at Tapjoy leveraged Riak KV as a basis for a message queue and chose the Go programming language (aka Golang) to do so. They call it **Dynamiq**.

# Why Message Queues?

Message queues are a powerful, and necessary, requirement of modern application architectures because of the simple fact that they allow for asynchronous processes.

Need a visual aid? I highly recommend watching the first 10 minutes of [Martin Kleppmann](https://martin.kleppmann.com/)’s talk from Craft Conf titled [*Using logs to build a solid data infrastructure*](http://martin.kleppmann.com/2015/04/24/logs-for-data-infrastructure-at-craft.html). At the culmination of his architectural diagram, he gets to this view of the stack:

[![martinkl-at-craftconf-insanity](../images/built-on-riak-dynamiq-by-tapjoy/martinkl-at-craftconf-insanity-1024x582.png)](../images/built-on-riak-dynamiq-by-tapjoy/martinkl-at-craftconf-insanity-1024x582.png)

You can see a message queue on the side of this insanity.

# Why the Mess?

What can be tricky about all this?

Nearly all infrastructures require more than one type of data index. Each data source provides a query pattern that’s unique and, in some beneficial way, required by part of the application. The intuitive solution, to have the application write to multiple data sources, leads to a race condition (visualized below). Martin covers this practice in the talk above, which I borrow from (with his permission) in this [introduction to message queues](http://www.slideshare.net/BashoTechnologies/a-little-about-message-queues-boston-riak-meetup) talk.

[![martink-at-craftconf-dual-writer](../images/built-on-riak-dynamiq-by-tapjoy/martink-at-craftconf-dual-writer-1024x689.png)](../images/built-on-riak-dynamiq-by-tapjoy/martink-at-craftconf-dual-writer-1024x689.png)

Knowing that writing to multiple sources isn’t reliable, how do we manage data indexing across these platforms?

**Cue message queues.**

An asynchronous workflow allows applications to process data reliably without slowing down the end user experience. Whether you want to write to 4 or 400 different data services, a message queues gives you an asynchronous method to decouple applications by separating the actions of sending and receiving data.

# What’s Dynamiq?

Dynamiq is an [at-least-once](https://lobste.rs/s/ecjfcm/why_is_exactly-once_messaging_not_possible_in_a_distributed_queue) queue that benefits from the scalability and fault-tolerance of Riak KV. Messages are tagged with a 64-bit integer and partitioned across the cluster. This, in turn, is partitioned across Riak KV, which inherits its low-latency, high-performing distribution of data. This message ID is later queried through the 2i secondary search index.

Data is retrieved through the REST API, a [ruby client](https://github.com/basho-labs/the-riak-community/issues/63), and there is a scala client in the works. You can unpack its implementation, API endpoints, and recommended configuration in the [detailed README](https://github.com/Tapjoy/dynamiq).

# But *Why*Dynamiq?

[![Tapjoy-why-Dynamiq](../images/built-on-riak-dynamiq-by-tapjoy/Tapjoy-why-Dynamiq-1024x560.png)](../images/built-on-riak-dynamiq-by-tapjoy/Tapjoy-why-Dynamiq-1024x560.png)

There are a number of message queues in the wild, from fellow Erlang-ers at [RabbitMQ](https://www.rabbitmq.com/) to the easy-to-use [SNS and SQS](https://aws.amazon.com/blogs/aws/queues-and-notifications-now-best-friends/) services from Amazon, so you might wonder why Tapjoy decided to build their own. There are four specific business drivers that lead to this new project.

### **1. High Availability at Scale**

Just like databases, not all queues are created with the same system architectures in mind. We know [how complicated distributed systems](./why-riak-just-works.md) can be to implement. Designing a system that provides for high availability with low latency while keeping it easily scalable is a challenge for most. Leveraging Riak KV as a platform for Dynamiq ensured each of these requirements from the start given the masterless, AP-architecture of Riak KV. As [Sean Kelly](https://github.com/stabbycutyou), one of the creators of Dyamiq, put it: “we’re leveraging a known product [in Riak KV], that is a rock solid distributed system.”

### **2. Cost**

SNS and SQS are well loved inside Tapjoy and are still leveraged for other services. The use case that Dynamiq was designed for hit a level where these services were cost prohibitive. The [README](https://github.com/Tapjoy/dynamiq/blob/master/README.md) states Dyamiq’s goal as a “drop-in replacement for the Amazon’s SNS / SQS services, which can become expensive at scale, both in terms of price as well as latency.”

Hosting an open source software, on-premises, was a money saver and resulted in an even faster (i.e. lower latency) service.

### **3. Expertise**

Tapjoy has expertise with Riak KV from years of running it in production. This in-house familiarity gives them the good fortune of being comfortable spinning up further Riak clusters and scaling them, up and down, based on demand. “It’s a thing we just know how to do,” Sean says when he discusses using Riak KV for Dynamiq.

The dev team at Tapjoy continue to find new and novel ways to build Riak KV into their services. There is a benefit to standardization, especially when it comes to how the Ops team monitors these clusters like any other in the production environment.

### **4. Always be Learning**

The team at Tapjoy are proud polyglots, continuing to pick up new programming languages on a regular basis. Part of the inspiration to design this solution was for that team to build a system — from start to finish — in Golang.

Golang has increased in popularity in the Riak community to the point where we have engineers who have an [open Beta of the Golang client](https://github.com/basho/riak-go-client).

[![go-gopher3](../images/built-on-riak-dynamiq-by-tapjoy/go-gopher3.png)](../images/built-on-riak-dynamiq-by-tapjoy/go-gopher3.png)

# Message Queues: Go Pick Something

The engineers at Tapjoy have created a powerful distributed message queue that will feel simple and familiar to any Riak KV user today. As Sean states in [his presentation on message queues](http://www.slideshare.net/StabbyCutyou/messaging-49839058), we should start by becoming familiar with the use cases.

Here are some follow up posts for you:

- [Introduction to Amazon SQS](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/Welcome.html) (at Sean’s recommendation)
- [Kafka or RabbitMQ for durability](http://www.quora.com/Which-one-is-better-for-durable-messaging-with-good-query-features-RabbitMQ-or-Kafka) (great quora thread)
- [Exploring message brokers](http://java.dzone.com/articles/exploring-message-brokers) (prototypes from ActiveMQ to Kafka w/specific needs)

Some key takeaways:

- Distributed systems are hard – make sure your message queue knows how to scale
- It’s worth the extra effort to wrap your Publisher code to prevent tight coupling with a specific message broker / queuing platform
- It’s NOT worth doing the same on the Consumer side
- Pay attention to client implementations (and its buffers)
- If you have moderate scale, use SQS from Amazon
- If you have a more challenging scale, don’t be shy about using [Dynamiq from Tapjoy](https://github.com/Tapjoy/dynamiq) ( built [on top of Riak KV](http://basho.com/products/riak-kv/))

Whether you need a message queue in your infrastructure or are inspired to open source your next project on Riak KV, be sure to share with our broader community.  We curate code using the Basho Labs organization on GitHub. [Share your latest work with us here](https://github.com/basho-labs/the-riak-community/issues/62).
