---
title: 'Verify an OpenRiak installation'
description: 'Show operators how to verify an openriak installation and confirm that the installation is ready.'
weight: 9
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\verifying-installation.md'
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\verify.md'
migration_review:
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.0 packages.'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\setup\installing\verify.md'
  - 'Package, platform, installation, upgrade, or downgrade details require release-specific verification for OpenRiak KV 3.4.0.'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#local-release'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#starting-riak'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to verify an openriak installation and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

### Verifying an OpenRiak KV Installation

[client libraries]: {{< product-version-root >}}reference/client-libraries/
[perf open files]: {{< product-version-root >}}how-to/tune/set-open-files-limit/
[cluster ops bucket types]: {{< product-version-root >}}how-to/operate/manage-bucket-types/
[cluster ops inspect node]: {{< product-version-root >}}how-to/operate/inspect-node-and-cluster/

After you've installed OpenRiak KV, we recommend checking the liveness of
each node to ensure that requests are being properly served.

In this document, we cover ways of verifying that your Riak nodes are operating
correctly. After you've determined that your nodes are functioning and you're
ready to put OpenRiak KV to work, be sure to check out the resources in the
**Now What?** section below.

#### Starting an OpenRiak node

> **Note about source installations**
>
> To start an OpenRiak KV node that was installed by compiling the source code, you
can add the OpenRiak KV binary directory from the installation directory you've
chosen to your `PATH`.
>
> For example, if you compiled OpenRiak KV from source in
the `/home/riak` directory, then you can add the binary directory
(`/home/riak/rel/riak/bin`) to your `PATH` so that OpenRiak KV commands can be used in the same manner as with a packaged installation.

To start an OpenRiak node, use the `riak start` command:

```bash
riak start
```

A successful start will return no output. If there is a problem starting the
node, an error message is printed to standard error.

To run Riak with an attached interactive Erlang console:

```bash
riak console
```

A OpenRiak node is typically started in console mode as part of debugging or
troubleshooting to gather more detailed information from the Riak startup
sequence. Note that if you start an OpenRiak node in this manner, it is running as
a foreground process that will be exited when the console is closed.

You can close the console by issuing this command at the Erlang prompt:

```erlang
q().
```

Once your node has started, you can initially check that it is running with
the `riak ping` command:

```bash
riak ping
```

The command will respond with `pong` if the node is running or `Node <nodename>  not responding to pings` if it is not.

> **Open Files Limit**
>
> As you may have noticed, if you haven't adjusted your open files limit (`ulimit -n`), Riak will warn you at startup. You're advised
to increase the operating system default open files limit when running Riak.
You can read more about why in the [Open Files Limit][perf open files] documentation.

#### Does it work?

One convenient means of testing the readiness of an individual OpenRiak node and
its ability to read and write data is with the `riak admin test` command:

```bash
riak admin test
```

Successful output from `riak admin test` looks like this:

```text
Attempting to restart script through sudo -H -u riak
Successfully completed 1 read/write cycle to '<nodename>'
```

You can also test whether Riak is working by using the `curl` command-line
tool. When you have Riak running on a node, try this command to retrieve
the the properties associated with the [bucket type][cluster ops bucket types] `test`:

```bash
curl -v http://127.0.0.1:8098/types/default/props
```

Replace `127.0.0.1` in the example above with your OpenRiak node's IP address or
fully qualified domain name, and you should get a response that looks like this:

```
* About to connect() to 127.0.0.1 port 8098 (#0)
*   Trying 127.0.0.1... connected
* Connected to 127.0.0.1 (127.0.0.1) port 8098 (#0)
> GET /riak/test HTTP/1.1
> User-Agent: curl/7.21.6 (x86_64-pc-linux-gnu)
> Host: 127.0.0.1:8098
> Accept: */*
>
< HTTP/1.1 200 OK
< Vary: Accept-Encoding
< Server: MochiWeb/1.1 WebMachine/1.9.0 (someone had painted it blue)
< Date: Wed, 26 Dec 2012 15:50:20 GMT
< Content-Type: application/json
< Content-Length: 422
<
* Connection #0 to host 127.0.0.1 left intact
* Closing connection #0
{"props":{"name":"test","allow_mult":false,"basic_quorum":false,
 "big_vclock":50,"chash_keyfun":{"mod":"riak_core_util",
 "fun":"chash_std_keyfun"},"dw":"quorum","last_write_wins":false,
 "linkfun":{"mod":"riak_kv_wm_link_walker","fun":"mapreduce_linkfun"},
 "n_val":3,"notfound_ok":true,"old_vclock":86400,"postcommit":[],"pr":0,
 "precommit":[],"pw":0,"r":"quorum","rw":"quorum","small_vclock":50,
 "w":"quorum","young_vclock":20}}
```

The output above shows a successful response (`HTTP 200 OK`) and additional
details from the verbose option. The response also contains the bucket
properties for the `default` bucket type.

#### Riaknostic

It is a good idea to verify some basic configuration and general health
of the OpenRiak node after installation by using OpenRiak's built-in diagnostic
utility [Riaknostic](http://riaknostic.basho.com/).

To start up Riaknostic, ensure that Riak is running on the node and issue the following command:

```bash
riak admin diag
```

More extensive documentation for Riaknostic can be found in the [Inspecting a Node][cluster ops inspect node] guide.

#### riak chkconfig
It is good practice to run `riak chkconfig` before starting your node for the first time.

This command will determine whether the syntax in your configuration files is correct.

```
riak chkconfig
```

If your configuration files are syntactically sound, you should see the output `config is OK` followed by a listing of files that were checked. If, however, something is syntactically awry, you’ll see an error output that provides details about what is wrong.

The error message will specify which configurable parameters are syntactically unsound and attempt to provide an explanation why.

Please note that the chkconfig command only checks for syntax. It will not be able to discern if your configuration is otherwise unsound, e.g. if your configuration will cause problems on your operating system or doesn’t activate subsystems that you would like to use.

#### Now what?

You have a working OpenRiak node!

From here you might want to check out the following resources:

* [Client Libraries][client libraries] to use Riak with your favorite programming language

#### Local release

To create a local release, run `make rel`.  This will build a release of Riak in the `rel/riak` folder within the repository clone.  This can be configured, started and joined into a cluster as with any Riak node.

> [!WARNING]
> Migration review required: Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV {{< current-version >}} packages.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
