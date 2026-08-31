---
build:
  list: never
  render: never
---


# Riak KV 2.0.2 Reference Links List

## Common

[downloads]: {{<baseurl>}}openriak-kv/2.0.2/downloads/
[install index]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing
[upgrade index]: {{<baseurl>}}openriak-kv/2.0.2/upgrading
[plan index]: {{<baseurl>}}openriak-kv/2.0.2/planning
[config index]: {{<baseurl>}}openriak-kv/2.0.2/using/configuring/
[config reference]: {{<baseurl>}}openriak-kv/2.0.2/configuring/reference/
[manage index]: {{<baseurl>}}openriak-kv/2.0.2/using/managing
[performance index]: {{<baseurl>}}openriak-kv/2.0.2/using/performance
[glossary vnode]: {{<baseurl>}}openriak-kv/2.0.2/learn/glossary/#vnode
[contact basho]: http://basho.com/contact/

## Planning

[plan index]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning
[plan start]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/start
[plan backend]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/backend
[plan backend bitcask]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/backend/bitcask
[plan backend leveldb]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/backend/leveldb
[plan backend memory]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/backend/memory
[plan backend multi]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/backend/multi
[plan cluster capacity]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/cluster-capacity
[plan bitcask capacity]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/bitcask-capacity-calc
[plan best practices]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/best-practices
[plan future]: {{<baseurl>}}openriak-kv/2.0.2/setup/planning/future

## Installing

[install index]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing
[install aws]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/amazon-web-services
[install debian & ubuntu]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/debian-ubuntu
[install freebsd]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/freebsd
[install mac osx]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/mac-osx
[install rhel & centos]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/rhel-centos
[install smartos]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/smartos
[install solaris]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/solaris
[install suse]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/suse
[install windows azure]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/windows-azure

[install source index]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/source
[install source erlang]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/source/erlang
[install source jvm]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/source/jvm

[install verify]: {{<baseurl>}}openriak-kv/2.0.2/setup/installing/verify

## Upgrading

[upgrade index]: {{<baseurl>}}openriak-kv/2.0.2/setup/upgrading
[upgrade checklist]: {{<baseurl>}}openriak-kv/2.0.2/setup/upgrading/checklist
[upgrade version]: {{<baseurl>}}openriak-kv/2.0.2/setup/upgrading/version
[upgrade cluster]: {{<baseurl>}}openriak-kv/2.0.2/setup/upgrading/cluster
[upgrade mdc]: {{<baseurl>}}openriak-kv/2.0.2/setup/upgrading/multi-datacenter
[upgrade downgrade]: {{<baseurl>}}openriak-kv/2.0.2/setup/downgrade

## Configuring

[config index]: {{<baseurl>}}openriak-kv/2.0.2/configuring
[config basic]: {{<baseurl>}}openriak-kv/2.0.2/configuring/basic
[config backend]: {{<baseurl>}}openriak-kv/2.0.2/configuring/backend
[config manage]: {{<baseurl>}}openriak-kv/2.0.2/configuring/managing
[config reference]: {{<baseurl>}}openriak-kv/2.0.2/configuring/reference/
[config strong consistency]: {{<baseurl>}}openriak-kv/2.0.2/configuring/strong-consistency
[config load balance]: {{<baseurl>}}openriak-kv/2.0.2/configuring/load-balancing-proxy
[config mapreduce]: {{<baseurl>}}openriak-kv/2.0.2/configuring/mapreduce
[config search]: {{<baseurl>}}openriak-kv/2.0.2/configuring/search/

[config v3 mdc]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v3-multi-datacenter
[config v3 nat]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v3-multi-datacenter/nat
[config v3 quickstart]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v3-multi-datacenter/quick-start
[config v3 ssl]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v3-multi-datacenter/ssl

[config v2 mdc]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v2-multi-datacenter
[config v2 nat]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v2-multi-datacenter/nat
[config v2 quickstart]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v2-multi-datacenter/quick-start
[config v2 ssl]: {{<baseurl>}}openriak-kv/2.0.2/configuring/v2-multi-datacenter/ssl

## Using

[use index]: {{<baseurl>}}openriak-kv/2.0.2/using/
[use admin commands]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-admin-commands
[use running cluster]: {{<baseurl>}}openriak-kv/2.0.2/using/running-a-cluster

### Reference

[use ref custom code]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/custom-code
[use ref handoff]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/handoff
[use ref monitoring]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/statistics-monitoring
[use ref search]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/search
[use ref 2i]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/secondary-indexes
[use ref snmp]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/snmp
[use ref strong consistency]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/strong-consistency
[use ref jmx]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/jmx
[use ref obj del]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/object-deletion/
[use ref v3 mdc]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/v3-multi-datacenter
[use ref v2 mdc]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/v2-multi-datacenter

### Cluster Admin

[use admin index]: {{<baseurl>}}openriak-kv/2.0.2/using/admin/
[use admin commands]: {{<baseurl>}}openriak-kv/2.0.2/using/admin/commands/
[use admin riak cli]: {{<baseurl>}}openriak-kv/2.0.2/using/admin/riak-cli/
[use admin riak-admin]: {{<baseurl>}}openriak-kv/2.0.2/using/admin/riak-admin/
[use admin riak control]: {{<baseurl>}}openriak-kv/2.0.2/using/admin/riak-control/

### Cluster Operations

[cluster ops add remove node]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/adding-removing-nodes
[cluster ops inspect node]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/inspecting-node
[cluster ops change info]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/changing-cluster-info
[cluster ops load balance]: {{<baseurl>}}openriak-kv/2.0.2/configuring/load-balancing-proxy
[cluster ops bucket types]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/bucket-types
[cluster ops handoff]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/handoff
[cluster ops log]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/logging
[cluster ops obj del]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/object-deletion
[cluster ops backup]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/backing-up
[cluster ops mdc]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/v3-multi-datacenter
[cluster ops strong consistency]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/strong-consistency
[cluster ops 2i]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/secondary-indexes
[cluster ops v3 mdc]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/v3-multi-datacenter
[cluster ops v2 mdc]: {{<baseurl>}}openriak-kv/2.0.2/using/cluster-operations/v2-multi-datacenter

### Repair/Recover

[repair recover index]: {{<baseurl>}}openriak-kv/2.0.2/using/repair-recovery
[repair recover index]: {{<baseurl>}}openriak-kv/2.0.2/using/repair-recovery/failure-recovery/

### Security

[security index]: {{<baseurl>}}openriak-kv/2.0.2/using/security/
[security basics]: {{<baseurl>}}openriak-kv/2.0.2/using/security/basics
[security managing]: {{<baseurl>}}openriak-kv/2.0.2/using/security/managing-sources/

### Performance

[perf index]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/
[perf benchmark]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/benchmarking
[perf open files]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/open-files-limit/
[perf erlang]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/erlang
[perf aws]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/amazon-web-services
[perf latency checklist]: {{<baseurl>}}openriak-kv/2.0.2/using/performance/latency-reduction

### Troubleshooting

[troubleshoot http]: {{<baseurl>}}openriak-kv/2.0.2/using/troubleshooting/http-204

## Developing

[dev index]: {{<baseurl>}}openriak-kv/2.0.2/developing
[dev client libraries]: {{<baseurl>}}openriak-kv/2.0.2/developing/client-libraries
[dev data model]: {{<baseurl>}}openriak-kv/2.0.2/developing/data-modeling
[dev data types]: {{<baseurl>}}openriak-kv/2.0.2/developing/data-types
[dev kv model]: {{<baseurl>}}openriak-kv/2.0.2/developing/key-value-modeling

### Getting Started

[getting started]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started
[getting started java]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/java
[getting started ruby]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/ruby
[getting started python]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/python
[getting started php]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/php
[getting started csharp]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/csharp
[getting started nodejs]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/nodejs
[getting started erlang]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/erlang
[getting started golang]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/golang

[obj model java]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/java/object-modeling
[obj model ruby]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/ruby/object-modeling
[obj model python]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/python/object-modeling
[obj model csharp]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/csharp/object-modeling
[obj model nodejs]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/nodejs/object-modeling
[obj model erlang]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/erlang/object-modeling
[obj model golang]: {{<baseurl>}}openriak-kv/2.0.2/developing/getting-started/golang/object-modeling

### Usage

[usage index]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage
[usage bucket types]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/bucket-types
[usage commit hooks]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/commit-hooks
[usage conflict resolution]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/conflict-resolution
[usage content types]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/content-types
[usage create objects]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/creating-objects
[usage custom extractors]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/custom-extractors
[usage delete objects]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/deleting-objects
[usage mapreduce]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/mapreduce
[usage search]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/search
[usage search schema]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/search-schemas
[usage search data types]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/searching-data-types
[usage 2i]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/secondary-indexes
[usage update objects]: {{<baseurl>}}openriak-kv/2.0.2/developing/usage/updating-objects

### App Guide

[apps mapreduce]: {{<baseurl>}}openriak-kv/2.0.2/developing/app-guide/advanced-mapreduce
[apps replication properties]: {{<baseurl>}}openriak-kv/2.0.2/developing/app-guide/replication-properties
[apps strong consistency]: {{<baseurl>}}openriak-kv/2.0.2/developing/app-guide/strong-consistency

### API

[dev api backend]: {{<baseurl>}}openriak-kv/2.0.2/developing/api/backend
[dev api http]: {{<baseurl>}}openriak-kv/2.0.2/developing/api/http
[dev api http status]: {{<baseurl>}}openriak-kv/2.0.2/developing/api/http/status
[dev api pbc]: {{<baseurl>}}openriak-kv/2.0.2/developing/api/protocol-buffers/

## Learn

[learn new nosql]: {{<baseurl>}}riak/kv/learn/new-to-nosql
[learn use cases]: {{<baseurl>}}riak/kv/learn/use-cases
[learn why riak]: {{<baseurl>}}riak/kv/learn/why-riak-kv

[glossary]: {{<baseurl>}}openriak-kv/2.0.2/learn/glossary/
[glossary aae]: {{<baseurl>}}openriak-kv/2.0.2/learn/glossary/#active-anti-entropy-aae
[glossary read rep]: {{<baseurl>}}openriak-kv/2.0.2/learn/glossary/#read-repair
[glossary vnode]: {{<baseurl>}}openriak-kv/2.0.2/learn/glossary/#vnode

[concept aae]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/active-anti-entropy/
[concept buckets]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/buckets
[concept cap neg]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/capability-negotiation
[concept causal context]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/causal-context
[concept clusters]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/clusters/
[concept crdts]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/crdts
[concept eventual consistency]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/eventual-consistency
[concept keys objects]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/keys-and-objects
[concept replication]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/replication
[concept strong consistency]: {{<baseurl>}}openriak-kv/2.0.2/using/reference/strong-consistency
[concept vnodes]: {{<baseurl>}}openriak-kv/2.0.2/learn/concepts/vnodes

## Community

[community]: {{<baseurl>}}community
[community projects]: {{<baseurl>}}community/projects
[reporting bugs]: {{<baseurl>}}community/reporting-bugs
[taishi]: {{<baseurl>}}community/taishi

