---
title: "Building Riak Clusters with AWS CloudFormation"
date: "2013-01-15T07:22:54+00:00"
author: "James S. Martin"
original_url: "http://basho.com/posts/technical/building-riak-clusters-with-aws-cloudformation/"
archive_url: "https://web.archive.org/web/20170206002729http://basho.com/posts/technical/building-riak-clusters-with-aws-cloudformation/"
categories:
  - "Cloud & Deployment"
---
*January 15, 2013*

Today we’re introducing an easier way to build Riak clusters on AWS using [CloudFormation](http://aws.amazon.com/cloudformation/).

The project, [cloudformation-riak](http://github.com/basho/cloudformation-riak), comes with three CloudFormation templates. These templates range from building a simple Riak cluster to building a [VPC-based](http://aws.amazon.com/vpc/) stack that includes: a front-end load balancer; a cluster of application servers with a Riak powered demo application; a backend load balancer; and a riak-cluster.

Head over to the [cloudformation-riak](http://github.com/basho/cloudformation-riak) repo to get started. We also put together a screencast (below) that shows things in action.

Enjoy.

[James](https://github.com/jsmartin)
