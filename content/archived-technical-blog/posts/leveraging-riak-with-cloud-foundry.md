---
title: "Leveraging Riak with Cloud Foundry"
date: "2013-11-26T12:00:29+00:00"
author: "Hector Castro"
original_url: "http://basho.com/posts/technical/leveraging-riak-with-cloud-foundry/"
archive_url: "https://web.archive.org/web/20170731124941http://basho.com/posts/technical/leveraging-riak-with-cloud-foundry"
categories:
  - "Cloud & Deployment"
---
*November 26, 2013*

From a developer’s perspective, interacting with a Platform as a Service (PaaS) allows you to defer most of the responsibilities associated with deploying an application (network, servers, storage, etc.). That leaves two primary responsibilities: write the code and push it up to the platform (along with some configuration settings).

Often the platform will provide you with an arsenal of data stores to persist data produced by your applications. Riak and Riak CS are attractive data storage solutions for PaaS deployments because, as applications are spun up and down, the databases housing their data needs to remain available. In addition, Riak and Riak CS can scale along with your applications so that reading and writing data isn’t a bottleneck.

(If you’re interested in the differences between Riak and Riak CS, [look no further](http://basho.com/riak-cs-vs-riak/).)

## Cloud Foundry

One of the most popular open source Platforms as a Service is [Cloud Foundry](http://www.cloudfoundry.com/run). So, how would you leverage data stores like Riak or Riak CS with it?

## Service Broker

At a high level, a Cloud Foundry service broker advertises a catalog of services and service plans. For Riak, the service is Riak itself and the service plans are either a Bitcask or a LevelDB bucket. Cloud Foundry will not supply a Riak cluster for you: this must be something you’ve deployed and configured per the **Wiring It Up** section below.

You can think of the service broker as a middleman between your cluster and Cloud Foundry. The broker implements a set of APIs referred to as the [Services API](http://docs.cloudfoundry.com/docs/running/architecture/services/). As you interact with Cloud Foundry services, its [Cloud Controller](http://docs.cloudfoundry.com/docs/running/architecture/cloud-controller.html) asks your broker to create, delete, bind, and unbind instances of your service. In turn, your broker talks to an appropriately configured Riak cluster and fulfills those requests (for example, by instructing the Riak cluster to create a new bucket with a Bitcask backend).

There are currently two versions of the Services API: v1 and v2. However, since v2 is the recommended broker by Cloud Foundry, we decided to use the [v2 Services API](http://docs.cloudfoundry.com/docs/running/architecture/services/writing-service.html) to build a Riak service broker for Cloud Foundry.

## Wiring It Up

The first step in connecting Riak and Cloud Foundry begins with having a specially configured Riak cluster. The “specially” part just means that it needs to be configured with the [multi-backend](http://docs.basho.com/riak/latest/ops/advanced/backends/multi/).

The multi-backend allows Riak to be configured with more than one backend (for example, Bitcast and LevelDB) at the same time on a single cluster:

Next, connect Riak and the service broker by editing the service broker’s configuration file and launching it:

**Note:** `riak_hosts` can contain one or more Riak nodes. It is generally recommended to front your Riak cluster with some form of load balancing technology. If you have your cluster behind a load balancer, simply add only one host to `riak_hosts`.

From there, you need to register it with your Cloud Foundry instance:

**Note:** [xip.io](http://xip.io/) is a service that provides wildcard DNS for any (public or private) IP address.

After that, just push your application to Cloud Foundry and create an instance of the service using the interactive prompt:

If we push up a [sample application](https://github.com/hectcastro/cf-riak-service-broker-sample-app) that just dumps the `VCAP_SERVICES` environment variable as JSON, it looks like this:

## Conclusion

The Riak service broker for Cloud Foundry is far from finished. The original use case was built to deal with application testing.

For example, the broker can allocate a Bitcask backed bucket to an application so that it runs its tests against a Bitcask backend. Afterwards, the broker can tear down that bucket and provide another bucket for testing backed by LevelDB.

Clearly, there are more use cases than this.

We encourage you to contribute to the project in ways that help steer it toward your use cases by opening [issues](https://github.com/hectcastro/cf-riak-service-broker/issues) and [pull requests](https://github.com/hectcastro/cf-riak-service-broker/pulls). The end goal is to pair this service broker with a full Riak [BOSH](https://github.com/cloudfoundry/bosh) release.

(If you’re interested in a Riak BOSH release now, the community has put together a [great starting point](https://github.com/BrianMMcClain/riak-release).)

To sum it up, Riak is a powerful storage platform for building applications that need to scale and cannot go down. Cloud Foundry is a tool that empowers developers by giving them an environment where they can simply push up code and have it transform into a running application.

Marrying the two is quite powerful and provides organizations with both a flexible application and data tier.

## Helpful Links

- [Cloud Foundry](http://www.cloudfoundry.com/run)
- [Cloud Foundry v2 Services API](http://docs.cloudfoundry.com/docs/running/architecture/services/writing-service.html)
- [Cloud Foundry Riak Service Broker](https://github.com/hectcastro/cf-riak-service-broker)
- [Sample Application](https://github.com/hectcastro/cf-riak-service-broker-sample-app) (to easily dump `VCAP_SERVICES`)

[Hector Castro](https://twitter.com/hectcastro) and [John Daily](https://twitter.com/macintux)
