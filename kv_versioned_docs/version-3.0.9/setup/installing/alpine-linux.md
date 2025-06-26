---
title: "Alpine Linux"
sidebar_position: 301
sidebar_label: Alpine Linux
pagination_label: "Alpine Linux"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2021-11-12
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[security index]: ./../../../using/security
[install source erlang]: ./../source/erlang
[install verify]: ./../verify

Riak KV can be installed on Alpine Linux using a binary
package from the Riak repository.

The following steps have been tested to work with Riak KV on:

* Alpine Linux 3.16 using x86_64
* Alpine Linux 3.16 using aarch64

## Riak 64-bit Installation

To install Riak on Alpine Linux:

1. Add the Riak repository:
   * Run `sudo echo "https://files.tiot.jp/alpine/v3.16/main" >> /etc/apk/repositories`
2. Change directory to place the repository key:
   * Run `cd  /etc/apk/keys/`
3.  Download and install the Riak repository public key:
   * Run `sudo curl http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O`
4. Update your list of packages:
   * Run `apk update`
5. Install Riak:
   * For the latest version, run `apk add riak`
   * For a specific version, run `apk add riak=3.0.9-r1`

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].
