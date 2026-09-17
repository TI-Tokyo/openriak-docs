---
title: 'OpenRiak KV 3.4.0 release notes'
linkTitle: 'Release Notes'
description: 'Summarize the changes introduced in OpenRiak KV 3.4.0, such as new features, operational improvements, supported Erlang releases, and deprecations.'
weight: -20
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
audience:
  - 'all-readers'
tags: ['diataxis', 'kv', 'reference', 'release-notes']

draft: true
status: 'needs-review'
review_scope:
  - 'link-checking'
  - 'content'
editorial_review: 'content needs cleaning up'
technical_review: 'done'
last_reviewed: '2026-09-17'
review-by: 'TI Tokyo/JOM'
---

[WhatsChanged]: ../whats-changed
[ReleaseNotes326]: ../../3.2.5/release-notes

> [!Caution] Editiorial Notes
> The links in this section need to be updated to point to the current docs.
>
> 2026-09-17 PJAC 

## Riak KV 3.4.0 Release Notes

This release supports two major additional features, not available in Riak 3.2.6:

- [A new Query API](https://openriak.github.io/riak/QueryAPI.html) that offers improved support for conjunction queries; either through the application of filter expressions to projected attributes appended to sort keys, or through set expressions to combine the results of different range queries.  Support is also added for different accumulation options; so that queries can return counts and counts by specific attributes as well as lists of keys and keys/terms.
- [Extending conditional PUT logic to have token-based consensus on conditional checks](https://openriak.github.io/riak/ObjectAPI.html#conditional-requests); allowing for the stronger application of conditions on PUTs, to significantly reduce the probability of siblings resulting from concurrent updates within a cluster.

There are a number of other improvements in the release:

- [Improved configurability of logging](https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging); allowing for logs of different types to be split between different handlers, and the addition of support for logging in a json format.
- [Monitoring facilities for Tictac-based AAE via a Command Line Interface](https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-and-controlling-aae---command-line); allowing for the prompting of tree rebuilds via the command-line, and a view of the current status of the anti-entropy system.
- [Improved efficiency of node repairs through the `double_pair` and `repair_deferred` configuration option](https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#completing-a-repair); improving the efficiency of repairs under application load when using the leveled backend.
- [The prompting of AAE folds via a Command Line Interface](https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-the-command-line); with the capability to prompt long-running folds to have results written to disk on completion.
- [The addition of a new bucket property `aae_tree_exclude`](https://openriak.github.io/riak/InstallAndStartGuide.html#property---aae_tree_exclude); whereby buckets with temporary data not intended to be replicated can be excluded from cached AAE trees.

The release can be used with either OTP 24 or OTP 26; with improved performance expected when choosing OTP 26, in particular when using the leveled backend and the HTTP API.

To reduce maintenance overheads going forward, the release deprecates the following functionality:

- Use of the `eleveldb` backend; with improvements planned to make the `bitcask` backend support `HEAD` requests efficiently, to align with the `leveled` backend.
- Use of the `memory` backend; with future improvements planned for vnode-level caching, configurable via bucket properties.
- Use of `multi` backends; except where all backends are `bitcask` backends.
- Use of `map/reduce` querying of Riak stores; with further extensions planned for the Query API, in particular the ability to publish objects from query results to a queue, to be consumed in parallel by multiple external processes.
- Use of `riak_ensemble` backed strong consistency; with the preference to use the support for conditional PUT requests with token-based consensus, provided in this release, for tuning consistency.
- Support for `dtrace` within Riak; with a preference to support internal Erlang tooling for debugging and monitoring in the future.
- Use of `v1.4 counters` and `link-walking`; which have been deprecated since Riak 2.0.

There is ongoing work for the Riak 4.0 release to provide a more flexible capability to merge objects, and this may change the future support status of CRDT data-types within Riak: although the aim will be to make any new feature sufficiently extensible to support backwards compatibility with existing CRDTs.

The NextGen replication functionality and the related Tictac-form of AAE are now considered to be stable and feature-complete; and so support for maintenance of legacy replication and anti-entropy mechanisms is not currently guaranteed for future releases.

Should the retirement of features in Riak 4.0 prove to be problematic for Riak users, the preference of the OpenRiak community is to seek support to prolong the availability of features by providing an OTP28 compatible Riak KV 3.6 release, rather than maintaining those features within Riak 4.0.  Decisions on retirement and support in releases will continue to be considered via [OpenRiak discussions](https://github.com/orgs/OpenRiak/discussions), while being constrained by the level of support provided to the community by user groups and their associates.

## Riak KV 3.4.0 RC0 Release Notes

This release is a release candidate for the OpenRiak release of Riak 3.4.0.  It contains the two major features planned for Riak 3.4.0:

- A new Query API; [draft documentation available here](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/docs/QueryAPI.md).
- The addition of consensus supported conditional PUT logic; [draft documentation available here](https://github.com/OpenRiak/riak_kv/blob/openriak-3.4/docs/ObjectAPI.md#conditional-requests).

There are further updates planned prior to the formal release of Riak 3.4.0, but no other major features.  Additional updates will be focused on operational improvements.

The Riak 3.4.0 release is planned to support OTP 26, and OTP 24 initially, but for performance reasons the use of OTP 26 is recommended.

## Previous Release Notes

The Riak 3.2.6 release notes are [here][ReleaseNotes326]

## What's Changed in the Documentation

Please see [What's Changed][WhatsChanged].
