---
title: Build a learning cluster with Vagrant
description: 'Create a disposable Ubuntu VM with Vagrant, run the Docker learning cluster inside it, and remove
  the VM when finished. This isolates the exercise from your host''s services while keeping the database lesson
  identical to '
weight: 40
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
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\quickstart\vagrant.md
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/first-cluster/vagrant.md
related:
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- tutorials/first-cluster/build-and-explore-a-cluster-on-ubuntu
- how-to/installation/run-openriak-with-persistent-docker-storage
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Create a disposable Ubuntu VM with Vagrant, run the Docker learning cluster inside it, and remove the VM when finished. This isolates the exercise from your host's services while keeping the database lesson identical to [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/).

## Prepare the host

Install Vagrant and a compatible VirtualBox provider. Reserve at least 4 CPUs, 12 GiB RAM, and enough host disk space for the VM and five container data directories. Use an x86_64 host for this example. The [Vagrant setup tutorial](https://developer.hashicorp.com/vagrant/tutorials/get-started/setup-project) uses the Bento Ubuntu 24.04 box.

Create an empty directory and save this as `Vagrantfile`:

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.hostname = "openriak-learning"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 12288
    vb.cpus = 4
  end
end
```

Run:

```sh
vagrant up --provider=virtualbox
vagrant box list
vagrant ssh
```

Record the installed box version from `vagrant box list` and set `config.vm.box_version` to that version before sharing or repeating the lab. Box versions vary by provider and architecture; do not assume an ARM box can run on an x86 host.

## Prepare the guest

Inside the VM, install Docker Engine and Compose using [Docker's Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/). Verify `docker compose version`. Create the lab under the guest's home directory, not the `/vagrant` shared filesystem, so database files use the guest's native filesystem.

Follow [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/) inside the VM. Keep the lab listeners bound to loopback until the first local write and read succeeds.

## Test from the host

Vagrant's ordinary port forward reaches the guest network interface, not its loopback-bound container port. Keep the database private and use an SSH tunnel instead. In a host terminal:

```sh
vagrant ssh -- -N -L 18098:127.0.0.1:18098
```

In a second host terminal, request `http://127.0.0.1:18098/ping` and the greeting key using the Docker lesson's curl commands. Expect `OK` and `Hello OpenRiak`.

## Stop and remove the environment

Stop the cluster with `docker compose down` inside the VM. Exit the guest shell and close the tunnel. From the host's Vagrant directory, run `vagrant halt` to retain the VM, or `vagrant destroy` to discard this VM and its guest data. The downloaded box remains cached; remove its specific version with `vagrant box remove` only if no other lab needs it.
