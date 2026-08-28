---
title: 'Repair secondary indexes'
description: 'Show practitioners how to repair secondary indexes from evidence gathering through verification.'
weight: 8
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\admin\2i.md'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\secondary-indexes.md'
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\repair-recovery\secondary-indexes.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show practitioners how to repair secondary indexes from evidence gathering through verification.

## Before you begin

The failing request or symptom, timestamps, relevant logs, and a recovery plan. Reproduce the issue safely before changing production state.

## Overview

### Secondary Indexes

#### Hanc capellae

Lorem markdownum Byblida. Modo **etiam** litora mittat vellera infelix caeli.
Studiosius forte, potuit pectore. Puer undas dignior iam turpe sorores abesse.
Deae Saturnia levius viribus membra.

#### Iussorum ad fronti rutilasque tenuit cursu quae

Nostros vovistis artes. **Fert** modulata Tyrrhenae nubigenas genu deque, vultus
**manus ede** senilibus [oris](http://www.youtube.com/watch?v=MghiBW3r65M)
transcurrere quem rarissima. Viderunt nutu quod, tumidaque, mihi mihi sacer pia.
Summis rediit pavidus tersere et at prosiluit natus Phaethon noxa. Singultibus
oblita **foedabis** orsa.

- Fecere aliis postquam inviti caliginis ab inque
- Voverat dividuae et tardus huc magna non
- Sex barba ipsaque Caucason corpora sono ecce
- Non esse
- Sibi atris regna licuit Antium carituraque nubes

#### Omni levare gelidumque minanti

Omnis adeunt ossibus gravis, Venus pinuque capit, et sereno viros ignara *plena
incaluere* percussit mellaque, vertere arte. Ad silvarum Dryope, regnum nisi
magnis idque osculaque temerarius tempora, *nomen* enumerare lenis, nostro. Ac
mutabit [arma](http://www.thesecretofinvisibility.com/) operiri saxum ratione,
crudelior feram, est usu tamen quod, hasta. Equos **sonant et deum**. Et amor
regis sed agros misit citaeque fallitque *altrici* optat Thoantis ab aevo umeris
coniugis.

#### Troiana quoque

Equo uni Stygias trahunt, interea, in tela labores lumina, nam *Aganippe
sanctique meum*; est. [Gente inimica
premeret](http://en.wikipedia.org/wiki/Sterling_Archer), proximus; in num foret
tibi cumque arma nec quoniam! Contribuere mollis, tu dum parem viscera, tamen
ante. Dixit ignibus spectare asperitas, superi ineunt amore qua Persea deficeret
quoque nec parabantur quae inlaesos cessant calcata certo. Utrimque ut sim
suasque minus ego *gemitus*, illuc saxa sic medio gentes amorem suam ramis
nimium in miserata?

1. `In naribus aequos aberant`
2. Naturae murmura te rimas suarum vulnus quod
3. Socios leto loquor timide
4. Ergo sub
5. Patrias mihi consumite breve

#### Ruit huic movit luminibus excubias arma

> Loco humo tecum gurgite timui. Peragant tu regia ut umbras premit condit. Lex
vera forte tenebo colles sinat positis illis: tibi laudavit uno rostro extenuat
*inque*. Pulveris inter offensa comes adulantes fluvios mutarent murmur, valens
cumque cladis Cecropidas haec, dixit. Lucus cognomine **Achilles**: pastor nec.

1. Hic causam et dilecte nudae nec corpus
2. Cor Si nive
3. Petis equos perosa tu perterrita exitus non
4. Per et et ire geminos parte
5. Aqua coniunx cecidisse sonum

```
Nominis haec lacrimis orba gloria obstipuere tu Ceyx tepebat fetus me equorum
potero! Iampridem illi; deducit [reor orbem](http://heeeeeeeey.com/), comes, et
nec rubebant pietas, ipsa.
```

### Repairing Secondary Indexes

The `riak admin repair-2i` command can be used to repair any stale or missing secondary indexes.  This command scans and repairs any mismatches between the secondary index data used for querying and the secondary index data stored in the Riak objects. It can be run on all partitions of a node or on a subset of them.  We recommend scheduling these repairs outside of peak load time.

#### Running a Repair

The secondary indexes of a single partition can be repaired by executing:

```bash
riak admin repair-2i <Partition_ID>
```

The secondary indexes of every partition can be repaired by executing the same command, without a partition ID:

```bash
riak admin repair-2i
```

Produces the following:

```
Will repair 2i data on 32 partitions
Watch the logs for 2i repair progress reports
ok
```

#### Monitoring a Repair

Repairs can be monitored using the below command:

```bash
riak admin repair-2i status
```

Produces the following if a repair is running:

```
2i repair status is running:
Total partitions: 1
Finished partitions: 0
Speed: 99
Total 2i items scanned: 1
Total tree objects: 100
Total objects fixed: 1
```

Produces the following if a repair is not running:

```
2i repair is not running
ok
```

#### Killing a Repair

In the event the secondary index repair operation needs to be halted, all repairs can be killed with:

```bash
riak admin repair-2i kill
```

----

If a replica loss has occurred, you need to run the repair command. This command repairs objects from a node's adjacent partitions on the ring.

This is done as efficiently as possible by generating a hash range for all the buckets and thus avoiding a preflist calculation for each key. Only a hash of each key is done, its range determined from a bucket&rarr;range map, and then the hash is checked against the range.

This code will force all keys in each partition on a node to be reread.

1. From a cluster node with Riak installed, attach to the Riak console:

```bash
    riak attach
    ```

You may have to hit enter again to get a console prompt.

2. Get a list of partitions owned by the node that needs repair:

```erlang
    {ok, Ring} = riak_core_ring_manager:get_my_ring().
    ```

You will get a lot of output with Ring record information. You can safely ignore it.

3. Then run the following code to get a list of partitions. Replace 'dev1@127.0.0.1' with the name of the node you need to repair.

```erlang
    Partitions = [P || {P, 'dev1@127.0.0.1'} <- riak_core_ring:all_owners(Ring)].
    ```

_Note: The above is an [Erlang list comprehension](http://www.erlang.org/doc/programming_examples/list_comprehensions.html), that loops over each `{Partition, Node}` tuple in the Ring, and extracts only the partitions that match the given node name, as a list._

4. Execute repair on all the partitions. Executing them all at once like this will cause a lot of `{shutdown,max_concurrency}` spam but it's not anything to worry about. That is just the transfers mechanism enforcing an upper limit on the number of concurrent transactions.

```erlang
    [riak_search_vnode:repair(P) || P <- Partitions].
    ```

5. When you're done, press `Ctrl-D` to disconnect the console. DO NOT RUN q() which will cause the running OpenRiak node to quit. Note that `Ctrl-D` merely disconnects the console from the service, it does not stop the code from running.

The above Repair command can be slow, so if you reattach to the console, you can run the repair_status function. You can use the `Partitions` variable defined above to get the status of every partition.

```erlang
[{P, riak_search_vnode:repair_status(P)} || P <- Partitions].
```

When you're done, press `Ctrl-D` to disconnect the console.

Currently there is no easy way to kill an individual repair.  The only
option is to kill all repairs targeting a given node.  This is done by
running `riak_core_vnode_manager:kill_repairs(Reason)` on the node
undergoing repair.  This means you'll either have to be attached to
that node's console or you can use the `rpc` module to make a remote
call.  Here is an example of killing all repairs targeting partitions
on the local node.

```erlang
riak_core_vnode_manager:kill_repairs(killed_by_user).
```

Log entries will reflect that repairs were killed manually, something akin to this:

```
2012-08-10 10:14:50.529 [warning] <0.154.0>@riak_core_vnode_manager:handle_cast:395 Killing all repairs: killed_by_user
```

Here is an example of executing the call remotely.

```erlang
rpc:call('dev1@127.0.0.1', riak_core_vnode_manager, kill_repairs, [killed_by_user]).
```

Repairs are not allowed to occur during ownership changes.  Since
ownership entails the moving of partition data it is safest to make
them mutually exclusive events.  If you join or remove a node all
repairs across the entire cluster will be killed.

>[!MEMO]Secondary Indexes (2i)
>Secondary indexes (2i) in Riak enable you to tag objects stored in Riak, at write time, with one or more queryable values. Those values can then be used to find multiple objects in Riak. If you’re storing user data, for example, you could tag each object associated with that user with a username or other unique marker. Once >tagged, you could find all objects in a Riak bucket sharing that tag. Secondary indexes can be either a binary or string, such as `sensor_1_data` or `admin_user` or `click_event`, or an integer, such as `99` or `141121`.

## Verify the result

Repeat the original check, confirm that the symptom has cleared, and watch logs and service metrics long enough to detect recurrence.
