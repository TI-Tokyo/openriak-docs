---
title: "Riak and Mesos – Automating Scale"
date: "2015-08-18T22:07:37+00:00"
author: "Tyler Hannan"
original_url: "http://basho.com/posts/technical/riak-and-mesos-automating-scale/"
archive_url: "https://web.archive.org/web/20170422193129http://basho.com/posts/technical/riak-and-mesos-automating-scale"
categories:
  - "Cloud & Deployment"
  - "Integrations & Plugins"
---
Today we are excited to [announce](http://basho.com/posts/press/basho-and-cisco-mesos/) an alpha framework for running Riak KV on Mesos. Some of you may be familiar with Mesos, for those who are new to Mesos, we will provide a brief overview.

Last year at Ricon 2014, [David Greenberg](https://twitter.com/dgrnbrg) gave a presentation entitled [*Mesos: The Operating System for your Cluster*](https://www.youtube.com/watch?v=LQxnuPcRl4s)*.* It provides a technical overview of Mesos itself, some of the common usage scenarios, and series of tools to better understand why, and where, Mesos is used in production environments. We highly encourage those interested in learning more about Mesos to begin with this presentation. In short, Mesos is an open-source software that provides a resource scheduling model and “common services”. These enable multiple services and applications to run across a cluster of machines in a datacenter or cloud.

We will be demonstrating this framework at [MesosCon](http://events.linuxfoundation.org/events/mesoscon) August 20 and 21 in Basho’s booth #209 as well as in Cisco’s booth. While the technical implementation is compelling, using technology (in particular datacenter scale orchestration) to solve for operational challenges at datacenter scale is even more compelling.

## Orchestration: A Customer Example

We know that elasticity and scalability are required by those who face the challenges of seasonal scale. None typify this need more than the eCommerce provider. Amazon is even known for saying that an increase of 100ms of latency can cost them 1% of sales. If latency is a percentage of sales, the cost of downtime averages in the millions per hour.

To overcome this challenge, which encompasses both availability and scalability, an eCommerce company has chosen to deploy Mesosphere DCOS to manage their datacenter and cloud infrastructures and has chosen Riak KV as their datastore. Using the framework it is trivial to create a cluster, add nodes to the cluster, and view the status of the nodes via [Riak Explorer](https://github.com/basho-labs/riak_explorer).

In the current implementation, running on Mesosphere DCOS, the installation and adding 3 nodes to the cluster looks something like the below:

A cluster is now in place, and you are now enjoying the benefits of using Riak KV… but the holiday season approaches. As we know the benefit of Riak KV’s near-linear scale is that additional nodes not only increase capacity but throughput. Given expected or occurring increases in data volumes, you need to add nodes and add them quickly.

Once again, the framework can be used to add Riak nodes with a simple command. That’s it.  It’s that simple. The cluster can meet your  seasonal demands to scale while keeping operational costs extremely low.

But in a complex environment we know that there is not  just one production environment to consider, but also the staging and development environments. In fact, when using shared production resources, there could be multiple development teams who need to create, and remove, clusters frequently in their development and test environments. In traditional environments, such as with RDBMS deployments, this can be a lengthy and onerous process of provisioning. With Riak KV and Mesos, it’s as simple as issuing the command to create another cluster.

The above example shows the principle scenario we considered when building the demonstration that is being shown at MesosCon. In fact, you can walk through the same demo yourself on the [github page](http://basho-labs.github.io/riak-mesos/).

## Architectural Considerations

To be clear, *this is a beta version and unsupported codebase*. Much of the current code is expected to change as we harden and prepare it for a fully-supported release. With that said, there are some key architectural considerations that are worth exploring in greater detail. Many of the architectural decisions are based on the fact that Mesos implementations have an assumption that resources are ephemeral. Or, put slightly differently, Mesos is stateless.

Our customers implement Riak KV for its characteristics of scalability and fault-tolerance. If Mesos can be used to assist in the scalability, that is a positive outcome. But it cannot come at the expense of fault-tolerance.

To that end, the Riak Mesos Framework scheduler, at present, attempts to spread Riak nodes across as many different Mesos agents as possible to increase fault tolerance. If there are more nodes requested than there are agents available, the scheduler will then starting adding more Riak nodes to existing agents.

In addition, there is an inherent assumption in client code that a cluster is a stable set of available resources. Due to the nature of Mesos and the potential for Riak nodes to come and go regularly, client applications using a Mesos based cluster must be kept up to date on the cluster’s current state. Instead of requiring this intelligence to be built into the Riak client libraries, we chose a smart, proxy application that runs alongside client applications. This proxy, communicates with Zookeeper to maintain the status of Riak cluster changes and, subsequently, updates its list of Riak connections for consumption by the client application.

## What’s next?

We are pleased to announce this work, in collaboration with Cisco. If you are at MesosCon please stop by the Basho booth (#209) for a live demonstration.

- [Riak Mesos framework repository](https://github.com/basho-labs/riak-mesos)
- [Riak Explorer repository](https://github.com/basho-labs/riak_explorer)
- [Press Release](http://www.basho.com/posts/press/basho-and-cisco-mesos)

If you have a perspective on the usage of Riak KV with Mesos, please [contact us](http://basho.com/contact/) to discuss.

[Tyler Hannan](http://www.twitter.com/tylerhannan)
