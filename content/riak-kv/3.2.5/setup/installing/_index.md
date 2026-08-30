---
weight: 101
title: "Installing Riak KV"
description: ""
project: "riak_kv"
project_version: "3.2.5"
lastmod: 2025-03-24T00:00:00-00:00
sitemap:
  priority: 0.9
menu:
  riak_kv-3.2.5:
    name: "Installing"
    identifier: "installing"
    weight: 101
    parent: "setup_index"
    pre: cog
toc: true
aliases:
  - /riak/3.2.5/ops/building/installing
  - /riak/kv/3.2.5/ops/building/installing
  - /riak/3.2.5/installing/
  - /riak/kv/3.2.5/installing/
---

[install aws]: {{< product-version-root >}}setup/installing/amazon-web-services
[install alpine]: {{< product-version-root >}}setup/installing/alpine-linux
[install debian & ubuntu]: {{< product-version-root >}}setup/installing/debian-ubuntu
[install raspbian]: {{< product-version-root >}}setup/installing/debian-ubuntu/#raspbian-bullseye
[install rhel & centos]: {{< product-version-root >}}setup/installing/rhel-centos
[install oracle linux]: {{< product-version-root >}}setup/installing/oracle-linux
[install source index]: {{< product-version-root >}}setup/installing/source
[upgrade index]: {{< product-version-root >}}setup/upgrading

## Supported Platforms

Riak is supported on numerous popular operating systems and virtualized
environments. The following information will help you to
properly install or upgrade Riak in one of the supported environments:

  * [Amazon Web Services][install aws]
  * [Alpine Linux][install alpine]
  * [Debian & Ubuntu][install debian & ubuntu]
  * [Raspbian][install raspbian]
  * [Oracle Linux][install oracle linux]
  * [RHEL & CentOS][install rhel & centos]

## Building from Source

If your platform isn’t listed above, you may be able to build Riak from source. See [Installing Riak from Source][install source index] for instructions.

## Community Projects

Check out [Community Projects][community projects] for installing with tools such as [Chef](https://www.chef.io/chef/), [Ansible](http://www.ansible.com/), or [Cloudsoft](http://www.cloudsoftcorp.com/).

## Upgrading

For information on upgrading an existing cluster see [Upgrading Riak KV][upgrade index].

[community projects]: https://github.com/orgs/OpenRiak/discussions
