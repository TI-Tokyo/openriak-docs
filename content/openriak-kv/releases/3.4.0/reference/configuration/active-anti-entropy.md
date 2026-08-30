---
title: 'Active anti-entropy configuration properties'
description: 'List active anti-entropy configuration properties with defaults, accepted values, units, dependencies, and version notes.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\active-anti-entropy.md'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

List active anti-entropy configuration properties with defaults, accepted values, units, dependencies, and version notes.

## Details

### Active Anti-Entropy

[config legacy]: {{< product-version-root >}}explanation/replication/legacy-aae/
[config tictac]: {{< product-version-root >}}explanation/replication/tictac-aae/
[config tictac-repl]: {{< product-version-root >}}reference/configuration/
[using aaefold]: {{< product-version-root >}}how-to/operate/aae-fold/
[learn aae]: {{< product-version-root >}}explanation/replication/active-anti-entropy/

OpenRiak's [active anti-entropy][learn aae] \(AAE) subsystem is a set of background processes that repair object inconsistencies stemming from missing or divergent object values across nodes. Riak operators can turn AAE on and off and configure and monitor its functioning.

Both Legacy and TicTac AAE systems can be used seperately or together.

If you are using the legacy AAE system, it is recommended that you migrate to the TicTac AAE system.

#### TicTac AAE system

The version of TicTac AAE included in 2.9 releases was a working prototype with limited testing.
TicTac AAE in KV 3.0.1+ is the release version, with full configuration options implemented.

TicTac Active Anti-Entropy makes two changes to the way Anti-Entropy has previously worked in Riak. The first change is to the way Merkle Trees are contructed so that they are built incrementally. The second change allows the underlying Anti-entropy key store to be key-ordered while still allowing faster access to keys via their Merkle tree location or the last modified date of the object.

##### [Configuring TicTac AAE][config tictac]

A guide covering commonly adjusted parameters for the TicTac AAE system.

[Learn More >>][config tictac]

###### [Configuring TicTac AAE's Next Gen Replication][config tictac-repl]

A guide covering commonly adjusted parameters for TicTac AAE's enhanced FullSync replication system.

[Learn More >>][config tictac-repl]

###### Other documentation

- [How to use `aae_fold`][using aaefold] to efficiently find, list and mangage keys.

#### Legacy AAE system

The legacy AAE system is still present, and works exactly as before.

##### [Configuring Legacy AAE][config legacy]

A guide covering commonly adjusted parameters for the legacy AAE system.

[Learn More >>][config legacy]
