---
title: "Riak KV 3.0.15"
sidebar_position: 100
sidebar_label: Riak KV
pagination_label: "Riak KV 3.0.15"
hide_table_of_contents: true
slug: /
hide_title: true
last_update:
  author: RiakDocs
  date: 2023-02-15
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[aboutenterprise]: https://www.tiot.jp/en/about-us/contact-us/
[config index]: ./configuring
[downloads]: ./downloads
[install index]: ./setup/installing
[plan index]: ./setup/planning
[perf open files]: ./using/performance/open-files-limit
[install debian & ubuntu]: ./setup/installing/debian-ubuntu
[getting started]: ./developing/getting-started
[dev client libraries]: ./developing/client-libraries

Riak KV is a distributed NoSQL database designed to deliver maximum data availability by distributing data across multiple servers. As long as your Riak KV client can reach one Riak server, it should be able to write data.

This release is tested with OTP 22.

## Supported Operating Systems

- Alpine Linux 3.16
- Alpine Linux 3.18
- Alpine Linux 3.21
- Amazon Linux 2016.09 (AWS)
- Amazon Linux 2 (AWS)
- CentOS 7
- CentOS 8
- Debian 8.0 ("Jessie")
- Debian 9.0 ("Stretch")
- Debian 10.0 ("Buster")
- Oracle Linux 8
- Red Hat Enterprise Linux 7
- Red Hat Enterprise Linux 8
- Raspbian Buster
- Ubuntu 16.04 ("Xenial Xerus")
- Ubuntu 18.04 ("Bionic Beaver")
- Ubuntu 20.04.4 ("Focal Fossa")
- FreeBSD 10.4
- FreeBSD 11.1
- Mac OSX 10.11+ (development only)

## Getting Started

Are you brand new to Riak KV? Start by [downloading][downloads] Riak KV, and then follow the below pages to get started:

1. [Install Riak KV][install index]
2. [Plan your Riak KV setup][plan index]
3. [Configure Riak KV for your needs][config index]

<RiakDocsNote title="Developing with Riak KV">
If you are looking to integrate Riak KV with your existing tools, check out the [Developing with Riak KV](./developing) docs. They provide instructions and examples for languages such as: Java, Ruby, Python, Go, Haskell, NodeJS, Erlang, and more.
</RiakDocsNote>

## Popular Docs

1. [Open Files Limit][perf open files]
2. [Installing on Debian-Ubuntu][install debian & ubuntu]
3. [Developing with Riak KV: Getting Started][getting started]
4. [Developing with Riak KV: Client Libraries][dev client libraries]

