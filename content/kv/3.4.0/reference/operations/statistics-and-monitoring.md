---
title: 'Statistics and monitoring metrics'
description: 'Define the names, fields, states, limits, and version applicability for statistics and monitoring metrics.'
weight: 10
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\multi-datacenter\monitoring.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\statistics-monitoring.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-statistics'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-aae---logs-and-statistics'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-operational-services'
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#riak-stats'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define the names, fields, states, limits, and version applicability for statistics and monitoring metrics.

## Details

### Multi-Datacenter Replication Reference: Monitoring

Monitoring OpenRiak's realtime replication allows you to identify trends and
to receive alerts during times when replication is halted or delayed.
Issues or delays in replication can be caused by:

* Sudden increases or spikes in write traffic
* Network connectivity issues or outages
* Errors experienced in Riak

Identification and trending of issues or delays in realtime replication
is important for identifying a root cause, while alerting is important
for addressing any SLA-impacting issues or delays. We recommend
combining the two approaches below when monitoring OpenRiak's realtime
replication:

* Monitor OpenRiak's replication status output, from either `riak repl
  status` or the HTTP `/riak repl/stats` endpoint
* Use canary (test) objects to test replication and establish trip times
  from source to sink clusters

**Note on querying and time windows**
OpenRiak's statistics are calculated over a sliding 60-second window. Each time
you query the stats interface, each sliding statistic shown is a sum or
histogram value calculated from the previous 60 seconds of data. Because of
this, the stats interface should not be queried more than once per minute.

#### Statistics

The following questions can be answered through the monitoring and
graphing of realtime replication statistics:

* Is the realtime replication queue backed up?
* Have any errors occurred on either the source or sink cluster?
* Have any objects been dropped from the realtime queue?

##### Is the realtime replication queue backed up?

Identifying times when the realtime replication queue experiences
increases in the number of `pending` objects can help identify problems
with realtime replication or identify times when replication becomes
overloaded due to increases in traffic. The `pending` statistic, found
under the `realtime_queue_stats` section of the replication status
output, should be monitored and graphed. Graphing this statistic allows
you to identify trends in the number of `pending` objects. Any repeating
or predictable trend in this statistic can be used to help identify a
need for tuning and capacity changes, while unexpected variation in this
statistic may indicate either sudden changes in load or errors at the
network, system, or Riak level.

###### Have any errors occurred on either the source or sink cluster?

Errors experienced on either the source or sink cluster can result in
failure to replicate object(s) via realtime replication. The top-level
`rt_dirty` statistic in `riak repl status` indicates whether such an
error has occurred and how many times. This statistic only tracks
errors and does not definitively indicate that an object was not
successfully replicated. For this reason, a fullsync should be performed
any time `rt_dirty` is non-zero. `rt_dirty` is then reset to zero once a
fullsync successfully completes.

The size of `rt_dirty` can quantify the number of errors that have
occurred and should be graphed. Since any non-zero value indicates an
error, an alert should be set so that a fullsync can be performed (if
not regularly scheduled). Like realtime queue back ups, trends in
`rt_dirty` can reveal problems with the network, system, or Riak.

###### Have any objects been dropped from the realtime queue?

The realtime replication queue will drop objects when the queue is full,
with the dropped object(s) being the last (oldest) in the queue. Each
time an object is dropped, the `drops` statistic, which can be found
under the `realtime_queue_stats` section of the replication status
output, is incremented. An object dropped from the queue has not been
replicated successfully, and a fullsync should be performed when a drop
occurs. A dropped object can indicate a halt or delay in replication or
indicate that the realtime queue is overloaded. In cases of high load,
increases to the maximum size of the queue (displayed in the
`realtime_queue_stats` section of the replication status output as
`max_bytes`) can be made to accommodate a usage pattern of expected high
load.

Although the above statistics have been highlighted to answer specific
questions, other statistics can also be helpful in diagnosing issues
with realtime replication. We recommend graphing any statistic that is
reported as a number. While their values and trends may not answer
common questions or those we've highlighted here, they may nonetheless
be important when investigating issues in the future. Other questions
that cannot be answered through statistics alone may be addressed
through the use of canary objects.

##### Canary Objects

Canary object testing is a technique that uses a test object stored in
your environment with your production data but not used or modified by
your application. This allows the test object to have predictable states
and to be used to answer questions about the functionality and duration
of realtime replication.

The general process for using canary objects to test realtime replication is:

* Perform a GET for your canary object on both your source and sink
  clusters, noting their states. The state of the object in each cluster
  can be referred to as state `S0`, or the object's initial state.
* PUT an update for your canary object to the source cluster, updating
  the state of the object to the next state, `S1`.
* Perform a GET for your canary on the sink cluster, comparing the state
  of the object on the source cluster to the state of the object on the
  sink cluster.

By expanding upon the general process above, the following questions can
be answered:

* Is a backed-up realtime replication queue still replicating objects
  within a defined SLA?
* How long is it taking for objects to be replicated from the source
  cluster to the sink cluster?

###### Is a backed-up realtime replication queue still replicating objects within a defined SLA?

Building on the final step of the general process, we can determine if
our objects are being replicated from the source cluster to the sink
cluster within a certain SLA time period by adding the following steps:

- If the state of the object on the source cluster is not equal to the
  state of the object on the sink cluster, repeat step 3 until an SLA
  time threshold is exceeded.
- If the SLA time threshold is exceeded, alert that replication is not
  meeting the necessary SLA.

###### How long is it taking for objects to be replicated from the source cluster to the sink cluster?

Getting a rough estimate of how long it takes an object PUT to a source
cluster to be replicated to a sink cluster get be done by either:

* Comparing the time the object was PUT to the source with the time the
  states of the object in the source and sink were equivalent
* Comparing the timestamps of the object on the source and sink when the
  states are equivalent

These are rough estimates, as neither method is 100% accurate. The first
method relies on a timestamp for a GET and subsequent successful
comparison, which means that the object was replicated prior to that
timestamp; the second method relies on the system clocks of two
different machines, which may not be in sync.

It's important to note that each node in a cluster has its own realtime
replication queue. The general process needs to be applied to every
node in the source cluster, with a variety of canary objects and states,
to get a complete picture of realtime replication between two clusters.

### Statistics & Monitoring Reference

Riak provides data related to current operating status, which includes
statistics in the form of counters and histograms. These statistics
are made available through the HTTP API via the [`/stats`]({{< baseurl >}}kv/3.4.0/reference/http-api/status/) endpoint, or through the [`riak admin`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/) interface, in particular the `stat` and `status` commands.

This page presents the most commonly monitored and gathered
statistics, as well as numerous solutions for monitoring and gathering
statistics that our customers and community report using successfully
in OpenRiak cluster environments. You can learn more about the specific
Riak statistics provided in the [Inspecting a Node]({{< baseurl >}}kv/3.4.0/how-to/operate/inspect-node-and-cluster/) and [HTTP Status]({{< baseurl >}}kv/3.4.0/reference/http-api/status/) documentation.

#### System Metrics To Graph

Graphing general system metrics of Riak nodes will help with
diagnostics and early warnings of potential problems, as well as help
guide provisioning and scaling decisions.

* CPU (user/system/wait/idle)
* Processor Load
* Available Memory
* Available disk space
* Used file descriptors
* Swap Usage
* IOWait
* Read operations
* Write operations
* Network throughput
* Network errors

We also recommend tracking your system's virtual and
writebacks. Things like massive flushes of dirty pages or steadily
climbing writeback volumes can indicate poor virtual memory tuning.
More information can be found [here][sysctl_vm_txt] and in our
documentation on [system tuning]({{< baseurl >}}kv/3.4.0/how-to/tune/#storage-and-file-system-tuning).

#### Riak Metrics to Graph

Riak metrics fall into several general categories:

1. Throughput metrics
2. Latency metrics
3. Erlang resource usage metrics
4. General Riak load/health metrics

If graphing all of the [available Riak metrics]({{< baseurl >}}kv/3.4.0/how-to/operate/inspect-node-and-cluster/) is
not practical, you should pick a minimum relevant subset from these
categories. Some of the most helpful metrics are discussed below.

##### Throughput Metrics

Graphing the throughput stats relevant to your use case is often
helpful for capacity planning and usage trend analysis. In addition,
it helps you establish an expected baseline -- that way, you can
investigate unexpected spikes or dips in the throughput.  The
following stats are recorded for operations that happened *during the
last minute*.

Metric | Relevance | Operations (for the last minute)
:--------|:--------|:--------------------------------
```node_gets``` | K/V | Reads coordinated by this node
```node_puts``` | K/V | Writes coordinated by this node
```vnode_counter_update``` | Data Types | Update [Counters][data_types_counters] operations coordinated by local vnodes
```vnode_set_update``` | Data Types | Update [Sets][data_types_sets] operations coordinated by local vnodes
```vnode_map_update``` | Data Types | Update [Maps][data_types_maps] operations coordinated by local vnodes
```consistent_gets``` | Strong Consistency | Consistent reads on this node
```consistent_puts``` | Strong Consistency | Consistent writes on this node
```vnode_index_reads``` | Secondary Indexes | Number of local replicas participating in secondary index reads

Note that there are no separate stats for updates to Flags or
Registers, as these are included in ```vnode_map_update```.

##### Latency Metrics

As with the throughput metrics, keeping an eye on average (and max)
latency times will help detect usage patterns, and provide advanced
warnings for potential problems.

**Note on FSM Time Stats**
FSM Time Stats represent the amount of time in microseconds required to
traverse the GET or PUT Finite State Machine code, offering a picture of
general node health. From your application's perspective, FSM Time effectively
represents experienced latency. Mean, Median, and 95th-, 99th-, and
100th-percentile (Max) counters are displayed. These are one-minute stats.

Metric | Also | Relevance | Latency (in microseconds)
:------|:-----|:----------|:-------------------------
```node_get_fsm_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | K/V | Time between reception of client read request and subsequent response to client
```node_put_fsm_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | K/V | Time between reception of client write request and subsequent response to client
```object_counter_merge_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100```  | Data Types | Time it takes to perform an Update Counter operation
```object_set_merge_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100```  | Data Types | Time it takes to perform an Update Set operation
```object_map_merge_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100```  | Data Types | Time it takes to perform an Update Map operation
```consistent_get_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | Strong Consistency | Strongly consistent read latency
```consistent_put_time_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | Strong Consistency | Strongly consistent write latency

##### Erlang Resource Usage Metrics

These are system metrics from the perspective of the Erlang VM,
measuring resources allocated and used by Erlang.

Metric | Notes
:------|:-------------------------
```sys_process_count``` | Number of processes currently running in the Erlang VM
```memory_processes``` | Total amount of memory allocated for Erlang processes (in bytes)
```memory_processes_used``` | Total amount of memory used by Erlang processes (in bytes)

##### General Riak Load/Health Metrics

These various stats give a picture of the general level of activity or
load on the OpenRiak node at any given moment.

Metric | Also | Notes
:------|:-----|:------------------
```node_get_fsm_siblings_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | Number of siblings encountered during all GET operations by this node within the last minute. Watch for abnormally high sibling counts, especially max ones.
```node_get_fsm_objsize_mean``` | ```_median```, ```_95```, ```_99```, ```_100``` | Object size encountered by this node within the last minute. Abnormally large objects (especially paired with high sibling counts) can indicate sibling explosion.
```pbc_active``` | | Number of currently active protocol buffer connections
```pbc_connects``` | | Number of new protocol buffer connections established during the last minute
```read_repairs``` | | Number of read repair operations this node has coordinated in the last minute (determine baseline, watch for abnormal spikes)
```list_fsm_active``` | | Number of List Keys FSMs currently active (should be 0)
```node_get_fsm_rejected``` | | Number of GET FSMs actively being rejected by Sidejob's overload protection
```node_put_fsm_rejected``` | | Number of PUT FSMs actively being rejected by Sidejob's overload protection

#### Command-line Interface

The [`riak admin`]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/) tool provides two
interfaces for retrieving statistics and other information: `status`
and `stat`.

##### status

Running the `riak admin status` command will return all of the
currently available information from a running node.

```bash
riak admin status
```

This will return a list of over 300 key/value pairs, like this:

```
1-minute stats for 'dev1@127.0.0.1'
-------------------------------------------
connected_nodes : ['dev2@127.0.0.1','dev3@127.0.0.1']
consistent_get_objsize_100 : 0
consistent_get_objsize_195 : 0
... etc ...
```

A comprehensive list of available stats can be found in the
[Inspecting a Node]({{< baseurl >}}kv/3.4.0/how-to/operate/inspect-node-and-cluster/#riak admin-status) document.

##### stat

The `riak admin stat` command is related to the `riak admin status`
command but provides a more fine-grained interface for interacting with
stats and information. Full documentation of this command can be found
in the [Inspecting a Node]({{< baseurl >}}kv/3.4.0/reference/commands/riak-admin/#stat) document.

#### Statistics and Monitoring Tools

There are many open source, self-hosted, and service-based solutions for
aggregating and analyzing statistics and log data for the purposes of
monitoring, alerting, and trend analysis on an OpenRiak cluster. Some
solutions provide Riak-specific modules or plugins as noted.

The following are solutions which customers and community members have
reported success with when used for monitoring the operational status of
their Riak clusters. Community and open source projects are presented
along with commercial and hosted services.

**Note on Riak 2.x Statistics Support**
Many of the below tools were either created by third-parties or Basho
engineers for general usage, and have been passed to the community for further
updates. As such, many of the below only aggregate the statistics and messages
that were output by Riak 1.4.x.

Like all code under [Basho Labs](https://github.com/basho-labs/), the below
tools are "best effort" and have no dedicated Basho support. We both
appreciate and need your contribution to keep these tools stable and up to
date. Please open up a GitHub issue on the repository if you'd like to be a
maintainer.

Look for banners calling out the tools we've verified that support the latest
Riak 2.x statistics!

##### Self-Hosted Monitoring Tools

###### Riaknostic

[Riaknostic](http://riaknostic.basho.com) is a growing suite of
diagnostic checks that can be run against your OpenRiak node to discover
common problems and recommend how to resolve them. These checks are
derived from the experience of the Basho Client Services Team as well as
numerous public discussions on the mailing list, IRC room, and other
online media.

Riaknostic integrates into the `riak admin` command via a `diag`
subcommand, and is a great first step in the process of diagnosing and
troubleshooting issues on Riak nodes.

###### Riak Control

[Riak Control]({{< baseurl >}}kv/3.4.0/reference/commands/riak-control/) is Basho's REST-driven user-interface for managing Riak
clusters. It is designed to give you quick insight into the health of
your cluster and allow for easy management of nodes.

While Riak Control does not currently offer specific monitoring and
statistics aggregation or analysis functionality, it does offer features
which provide immediate insight into overall cluster health, node
status, and handoff operations.

###### collectd

[collectd](http://collectd.org) gathers statistics about the system it
is running on and stores them. The statistics are then typically graphed
to find current performance bottlenecks, predict system load, and
analyze trends.

###### Ganglia

[Ganglia](http://ganglia.info) is a monitoring system specifically
designed for large, high-performance groups of computers, such as
clusters and grids. Customers and community members using Riak have
reported success in using Ganglia to monitor Riak clusters.

A [Riak Ganglia module][riak_ganglia] for collecting statistics from
the Riak HTTP [`/stats`]({{< baseurl >}}kv/3.4.0/reference/http-api/status/) endpoint is also available.

###### Nagios

**Note:**
**Tested and Verified Support for Riak 2.x.**

[Nagios](http://www.nagios.org) is a monitoring and alerting solution
that can provide information on the status of OpenRiak cluster nodes, in
addition to various types of alerting when particular events occur.
Nagios also offers logging and reporting of events and can be used for
identifying trends and capacity planning.

A collection of [reusable Riak-specific scripts][riak_nagios] are
available to the community for use with Nagios.

###### OpenTSDB

[OpenTSDB](http://opentsdb.net) is a distributed, scalable Time Series Database
(TSDB) used to store, index, and serve metrics from various sources. It can
collect data at a large scale and graph these metrics on the fly.

A [Riak collector for OpenTSDB][tcollector_riak_plugin] is available as part of
the [tcollector framework][tcollector].

###### Riemann

[Riemann](http://github.com/riemann/riemann/) uses a powerful stream
processing language to aggregate events from client agents running on
Riak nodes, and can help track trends or report on events as they occur.
Statistics can be gathered from your nodes and forwarded to a solution
such as Graphite for producing related graphs.

A [Riemann Tools](https://github.com/aphyr/riemann.git) project
consisting of small programs for sending data to Riemann provides a
module specifically designed to read Riak statistics.

###### Zabbix

**Note:**
**Tested and Verified Support for Riak 2.x Stats.**

[Zabbix](http://www.zabbix.com) is an open-source performance monitoring,
alerting, and graphing solution that can provide information on the state of
OpenRiak cluster nodes.

A [Zabbix plugin for Riak][riak_zabbix] is available to get you started
monitoring Riak using Zabbix.

##### Hosted Service Monitoring Tools

The following are some commercial tools which Basho customers have
reported successfully using for statistics gathering and monitoring
within their Riak clusters.

###### Circonus

[Circonus](http://circonus.com) provides organization-wide monitoring,
trend analysis, alerting, notifications, and dashboards. It can been
used to provide trend analysis and help with troubleshooting and
capacity planning in an OpenRiak cluster environment.

###### New Relic

[New Relic](http://newrelic.com) is a data analytics and visualization platform
that can provide information on the current and past states of Riak nodes and
visualizations of machine generated data such as log files.

A [Riak New Relic Agent][riak_new_relic] for collecting statistics from the Riak HTTP [`/stats`]({{< baseurl >}}kv/3.4.0/reference/http-api/status/) endpoint is also available.

###### Splunk

[Splunk](http://www.splunk.com) is available as downloadable software or
as a service, and provides tools for visualization of machine generated
data such as log files. It can be connected to OpenRiak's HTTP statistics
[`/stats`]({{< baseurl >}}kv/3.4.0/reference/http-api/status/) endpoint.

Splunk can be used to aggregate all OpenRiak cluster node operational log
files, including operating system and Riak-specific logs and Riak
statistics data. These data are then available for real time graphing,
search, and other visualization ideal for troubleshooting complex issues
and spotting trends.

#### Summary

Riak exposes numerous forms of vital statistic information which can be
aggregated, monitored, analyzed, graphed, and reported on in a variety
of ways using numerous open source and commercial solutions.

If you use a solution not listed here with Riak and would like to
include it (or would otherwise like to update the information on this
page), feel free to fork the docs, add it in the appropriate section,
and send a pull request to the [Riak
Docs](https://github.com/basho/basho_docs).

#### References

* [Inspecting a Node]({{< baseurl >}}kv/3.4.0/how-to/operate/inspect-node-and-cluster/)
* [Riaknostic](http://riaknostic.basho.com)
* [Riak Control]({{< baseurl >}}kv/3.4.0/reference/commands/riak-control/)
* [collectd](http://collectd.org)
* [Ganglia](http://ganglia.info)
* [Nagios](http://www.nagios.org)
* [OpenTSDB](http://opentsdb.net)
* [tcollector framework][tcollector]
* [Riemann](http://github.com/riemann/riemann/)
* [Riemann Github](https://github.com/aphyr/riemann)
* [Zabbix](http://www.zabbix.com)
* [Circonus](http://circonus.com)
* [New Relic](http://newrelic.com)
* [Splunk](http://www.splunk.com)
* [Riak Docs on Github](https://github.com/basho/basho_docs)

[sysctl_vm_txt]: https://www.kernel.org/doc/Documentation/sysctl/vm.txt
[data_types_counters]: {{< baseurl >}}riak/kv/latest/developing/data-types/counters/
[data_types_sets]: {{< baseurl >}}riak/kv/latest/developing/data-types/sets/
[data_types_maps]: {{< baseurl >}}riak/kv/latest/developing/data-types/maps/
[riak_nagios]: https://github.com/basho/riak_nagios
[tcollector]: https://github.com/stumbleupon/tcollector
[tcollector_riak_plugin]: https://github.com/stumbleupon/tcollector/blob/master/collectors/0/riak.py
[riak_zabbix]: https://github.com/basho/riak-zabbix
[riak_new_relic]: https://github.com/basho/riak_newrelic
[riak_ganglia]: https://github.com/jnewland/gmond_python_modules/tree/master/riak/

#### Riak Stats

Riak collates statistics.  Stats include total counts over all time, counts in the last 60 seconds, and mean, median and approximate percentile response times measured over the previous 60s.  The stats are available via the CLI `riak admin status` or via a http GET request to the `/stats` endpoint.

Riak does not retain history of stats, so to track the change of stats over time it is necessary to request the stats at regular intervals, and index the stats in some other monitoring tool.  Other than the `_total` stats, the stats will always reflect the last 60s, regardless of how frequently the stats are requested (returning stats does not reset any values).  The stats process maintains a rolling view of the last 60 seconds.

All timings are internal timings, and not necessarily fully representative of external application experience.

The stats represent the statistics on the node from which they were requested.  The stats are not cluster-wide, they are always node aggregates e.g. the vnode stats are accumulated over every vnode on the node.

#### Monitoring AAE - Logs and Statistics

When Tictac AAE is enabled, each vnode has a queue of exchanges related to that vnode's supported partitions, and the vnode will loop through that queue, prompting a new exchange every `exchangetick`.  If the `n_val` is 3 this will require 5 exchanges, and exchanges are required for every `n_val` configured in the cluster.

The result of each individual exchange is not logged by `riak_kv `unless it shows a discrepancy, although the details of each exchange can be found in the AAE logs with the tag `log_ref=ex*`.  A summary log is produced every loop from the `riak_kv_vnode` ("Tictac AAE loop completed"), giving the statistics for that loop.

Statistics on Tictac AAE exchanges are also available via [riak stats]({{< baseurl >}}kv/3.4.0/reference/operations/statistics-and-monitoring/):

- `tictacaae_queue_microsec__max`, `tictacaae_queue_microsec_mean`.
  - The time spent by the vnode waiting for the controller to respond to an update (prompted by a PUT on the vnode).
  - May give an indication that the vnode is being delayed due to the overhead of maintaining a parallel-mode AAE store.
- `tictacaae_root_compare`, `tictacaae_branch_compare`, `tictacaae_clock_compare`, `tictacaae_error`, `tictacaae_timeout`, `tictacaae_notsupported`.
  - Counts of the exchanges by the closing status of the exchange.
    - Intra-cluster exchanges follow [the same process as inter-cluster reconciliation exchanges]({{< baseurl >}}kv/3.4.0/how-to/configure/replication/configure-fullsync/).
    - `root_compare` or `branch_compare` indicate no deltas were discovered.
  - Because of the infrequency of exchanges, tracking the `*_total` statistics is normally required to gain understanding of trends in AAE activity.

> Additional logging will be generated if significant deltas are discovered, and the AAE process enters into a repair loop: a process through which repairs are accelerated by using information about the deltas being discovered (i.e. any pattern of buckets and modified date ranges discovered in deltas).

AAE will prompt the repair of delta using read repairs, so the [monitoring of read repairs]({{< baseurl >}}kv/3.4.0/how-to/operate/monitor-read-repairs/) provides further information.
