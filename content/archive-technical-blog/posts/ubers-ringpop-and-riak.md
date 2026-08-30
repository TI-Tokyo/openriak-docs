---
title: "Uber’s Ringpop and Riak"
date: "2015-05-07T09:19:02+00:00"
author: "Stephen Condon"
original_url: "http://basho.com/posts/technical/ubers-ringpop-and-riak/"
archive_url: "https://web.archive.org/web/20170629044230http://basho.com/posts/technical/ubers-ringpop-and-riak/"
categories:
  - "Architecture & Distributed Systems"
---
At the most recent San Francisco Riak meetup, we had the pleasure to invite Uber engineer & past OSCON speaker Jeff Wolski ([GitHub](https://github.com/jwolski)) to discuss his more recent work.

You may know [Uber](https://www.uber.com/) as the popular on-demand car service, but they’re so much more than that. Uber is innovating at the intersection of lifestyle and logistics at a rapid pace. To do so, they architect some of the most fascinating distributed architectures I know of.

A newer part of this ever-evolving distributed system is project **Ringpop** (also on [GitHub](https://github.com/uber/ringpop)). As Jeff puts it:

> “Ringpop is an open-source Node.js library developed at Uber that brings application-layer sharding to many of their dispatching platform services.”

This additional abstraction layer, maintained through a consistent hashing ring familiar to any Riak enthusiast, provides a means by which Jeff can add additional dispatching services without service interruption.

To leverage this scalability while providing stability, Ringpop keeps in mind that no distributed network is always reliable. Jeff dedicates a portion of his talk to exploring these complexities and how SWIM gossip protocol is implemented to handle bad actors:

> “Service instances that behave erratically, slow or otherwise, wreak havoc on the rest of the cluster by causing frequent and persistent changes to the state of the ring and ultimately, inconsistent hash ring lookups. In this talk you’ll hear about Ringpop, its implementation, and how we’ve had to employ a flap damping technique to suss out these bad actors to achieve higher levels of reliability for our services.”

The presentation, in the context of Ringpop, also shows how Uber relies on Riak for high availability. Riak acts as a persistent data store for a portion of new dispatching services as well as some functional extensions on top of Ringpop. For example, as objects are generated that require persistence, such as a new driver coming online and their associated mailbox of potential trips, these IDs are stored as keys within Riak.

These layers are used for further services, which rely on data stored in Riak, including:

- Stateful HTTP long-poll services
- Client/server sync services
- Rate limiters
- Geospatial services

It’s insanely interesting to see how Uber continues to scale as one of the most respected software companies today. To do so, Jeff notes a list of research that informs the design of Ringpop and will continue to be important to their development. What is often forgotten in our productivity-obsessed dev culture, is the importance of practice. In one Q&A, Jeff responds to a comment on the concern of creating a consistent hash on top of a consistent hash of Riak, he says “if it’s wrong I’ll go delete the repo right now.” His willingness to improve, even if it means deleting month’s worth of code, is refreshing to me.

There is a great deal of learning to be done if you’re looking to design a similar resilient set of services.

If you enjoy the video, you’ll love the documents mentioned. ~~The Dynamo paper~~ is close to our hearts at Basho since Riak is also based upon its goal. For further reading, check out [BGP route flap damping](http://www.cs.colostate.edu/~massey/pubs/tr/massey_usctr03-805.pdf), [SWIM protocol](https://www.cs.cornell.edu/~asdas/research/dsn02-swim.pdf), and Uber’s code on [tchannel](https://github.com/uber/tchannel).

Keep sharing, learning, building and re-building,  
Matt Brender  
[@mjbrender](https://twitter.com/@mjbrender)

Read the full story at:   
<https://www.google.com>
