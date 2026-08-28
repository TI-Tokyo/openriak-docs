---
title: "Riak KV 3.2.3"
sidebar_position: 100
sidebar_label: Riak KV
pagination_label: "Riak KV 3.2.3"
hide_table_of_contents: true
slug: /
hide_title: true
last_update:
  author: RiakDocs
  date: 2024-12-09
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

This release is tested with OTP 24 and OTP 25; but optimal performance is likely to be achieved when using OTP 25.

## Supported Operating Systems

- Alpine Linux 3.21
- Amazon Linux 2023
- CentOS 8
- Debian 10.0 ("Buster")
- Debian 11.0 ("Bullseye")
- Debian 12.0 ("Bookworm")
- Oracle Linux 8
- Red Hat Enterprise Linux 8
- Raspbian Bullseye
- Ubuntu 20.04.4 ("Focal Fossa")
- Ubuntu 22.04 ("Jammy Jellyfish")
- Ubuntu 24.04 ("Noble Numbat")

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

