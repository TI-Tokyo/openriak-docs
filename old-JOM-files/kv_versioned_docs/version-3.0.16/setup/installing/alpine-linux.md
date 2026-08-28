---
title: "Alpine Linux"
sidebar_position: 301
sidebar_label: Alpine Linux
pagination_label: "Alpine Linux"
hide_table_of_contents: true
last_update:
  author: RiakDocs
  date: 2023-06-23
---
import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';


[security index]: ./../../../using/security
[install source erlang]: ./../source/erlang
[install verify]: ./../verify

Riak KV can be installed on Alpine Linux using a binary
package from the Riak repository.

The following steps have been tested to work with Riak KV on:

* Alpine Linux 3.18 using x86_64
* Alpine Linux 3.18 using aarch64
* Alpine Linux 3.21 using x86_64
* Alpine Linux 3.21 using aarch64

## Riak 64-bit Installation

To install Riak on Alpine Linux:

1. Add the Riak repository:
   * For Apline Linux 3.18 Run `sudo echo "https://files.tiot.jp/alpine/v3.18/main" >> /etc/apk/repositories`
   * For Apline Linux 3.21 Run `sudo echo "https://files.tiot.jp/alpine/v3.21/main" >> /etc/apk/repositories`
2. Download and install the Riak repository public key:
   * Run `wget http://files.tiot.jp/alpine/alpine@tiot.jp.rsa.pub -O /etc/apk/keys/alpine@tiot.jp.rsa.pub`
3. Update your list of packages:
   * Run `apk update`
4. Install Riak:
   * For the latest version, run `apk add riak`
   * For a specific version, run `apk add riak=3.0.16-r0`

## Next Steps

Now that Riak is installed, check out [Verifying a Riak Installation][install verify].
