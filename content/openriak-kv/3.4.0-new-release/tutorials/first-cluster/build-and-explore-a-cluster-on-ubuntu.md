---
title: Build and explore a cluster on Ubuntu
description: Build a small native-package cluster on three Ubuntu 24.04 virtual machines, then write through one
  node and read through another. Use disposable machines on a private network; this is a learning deployment.
weight: 20
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\quickstart\ubuntu.md
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/first-cluster/ubuntu.md
related:
- how-to/installation/install-on-debian-or-ubuntu
- how-to/node-configuration/configure-node-identity-directories-and-the-initial-ring
- how-to/cluster-lifecycle/add-nodes-to-a-cluster
- tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Build a small native-package cluster on three Ubuntu 24.04 virtual machines, then write through one node and read through another. Use disposable machines on a private network; this is a learning deployment.

## Prepare three machines

Use the same architecture on each machine and reserve enough memory and disk space for the lab. This example assigns private addresses `192.168.56.11`, `.12`, and `.13`; substitute your actual addresses throughout. Each machine must reach the others directly. Allow Erlang distribution traffic only between these machines, and HTTP only from your learning client. See [Restrict client, node, and administrative network access]({{< product-version-root >}}how-to/security/restrict-client-node-and-administrative-network-access/) for the port rules.

On each machine, confirm the OS and architecture:

```sh
cat /etc/os-release
dpkg --print-architecture
```

## Install matching packages

Select Ubuntu 24.04 and the machine's architecture in the package selector. Download the same release and OTP variant onto all three nodes. Use the exact filename downloaded in place of `PACKAGE.deb`:

{{< download-os-picker >}}
{{< package-downloads >}}

```sh
sudo apt-get update
sudo apt-get install ./PACKAGE.deb
```

If installation starts a service, stop it before editing the node identity:

{{< service-command action="stop" os="ubuntu" >}}

## Configure the first node

Open the installed `riak.conf` as root. Replace existing assignments rather than adding duplicates. These values are deliberate lab choices:

{{< settings-example >}}
nodename = riak@192.168.56.11
distributed_cookie = replace_with_one_shared_lab_cookie
storage_backend = leveled
listener.http.internal = 192.168.56.11:8098
listener.protobuf.internal = 192.168.56.11:8087
{{< /settings-example >}}

Generate the shared cookie once with `openssl rand -hex 24`, then copy that value to all three configurations. On nodes two and three, replace the address in the node name and listeners with `.12` and `.13`. Keep each machine's data local and empty. Use the same initial ring settings on all nodes; [Node identity, directories, and ring settings]({{< product-version-root >}}reference/configuration/node-identity-directories-and-ring-settings/) shows their current defaults.

## Validate and start each node

{{< cli-example key="shell:riak chkconfig" prefix="sudo" >}}
{{< service-command action="start" os="ubuntu" >}}
{{< cli-example key="shell:riak ping" prefix="sudo" >}}

Expect `pong`. If startup fails, read the service logs before joining any members.

## Join and commit

On node two and then node three:

{{< cli-example key="shell:riak admin cluster join" prefix="sudo" args="riak@192.168.56.11" >}}

On node one:

{{< cli-example key="shell:riak admin cluster plan" prefix="sudo" >}}

Check that the plan adds exactly the other two nodes. Then commit and wait:

{{< cli-example key="shell:riak admin cluster commit" prefix="sudo" >}}
{{< cli-example key="shell:riak admin member-status" prefix="sudo" >}}
{{< cli-example key="shell:riak admin transfers" prefix="sudo" >}}

Continue when all three members are valid and transfers have completed.

## Write through one node, read through another

From the client machine:

```sh
curl --fail -X PUT http://192.168.56.11:8098/buckets/learning/keys/greeting -H 'Content-Type: text/plain' --data-binary 'Hello native cluster'
curl --fail http://192.168.56.12:8098/buckets/learning/keys/greeting
```

Expect `Hello native cluster`. Keep the VMs for another lesson or stop their services and delete the disposable VMs and disks. Before deleting them, confirm that their addresses and disk names belong to this lab.
