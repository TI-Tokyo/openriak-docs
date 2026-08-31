---
title: "Installing Riak KV"
description: ""
project: "riak_kv"
project_version: "2.9.10"
lastmod: 2021-10-06T00:00:00-00:00
sitemap:
  priority: 0.3
menu:
  riak_kv-2.9.10:
    name: "Installing"
    identifier: "installing"
    weight: 101
    parent: "setup_index"
    pre: cog
toc: true
aliases:
  - /riak/2.9.10/ops/building/installing
  - /openriak-kv/2.9.10/ops/building/installing
  - /riak/2.9.10/installing/
  - /openriak-kv/2.9.10/installing/
linkTitle: "Installing"
weight: 101
---

[install mac osx]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/mac-osx
[install aws]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/amazon-web-services
[install debian & ubuntu]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/debian-ubuntu
[install raspbian]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/debian-ubuntu/#raspbian-bullseye
[install freebsd]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/freebsd
[install oracle linux]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/oracle-linux
[install rhel & centos]: {{<baseurl>}}openriak-kv/2.9.10/setup/installing/rhel-centos
[upgrade index]: {{<baseurl>}}openriak-kv/2.9.10/setup/upgrading

## Supported Platforms

Riak is supported on numerous popular operating systems and virtualized
environments. The following information will help you to
properly install or upgrade Riak in one of the supported environments:

  * [Amazon Web Services][install aws]
  * [Debian & Ubuntu][install debian & ubuntu]
  * [FreeBSD][install freebsd]
  * [RHEL & CentOS][install rhel & centos]
  * [SUSE][install suse]
  * [Windows Azure][install windows azure]

## Building from Source

If your platform isn’t listed above, you may be able to build Riak from source. See [Installing Riak from Source][install source index] for instructions.

## Community Projects

Check out [Community Projects][community projects] for installing with tools such as [Chef](https://www.chef.io/chef/), [Ansible](http://www.ansible.com/), or [Cloudsoft](http://www.cloudsoftcorp.com/).

## Upgrading

For information on upgrading an existing cluster see [Upgrading Riak KV][upgrade index].

