---
title: 'Conditional requests'
description: 'Explain how validators and conditional operations reduce races, bandwidth, and unnecessary object reads.'
weight: 5
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ObjectAPI.html#conditional-requests'
  - 'https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---if-none-match'
  - 'https://openriak.github.io/riak/ObjectAPI.html#use-of-request-header---x-riak-if-not-modified-non-standard-riak-header'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain how validators and conditional operations reduce races, bandwidth, and unnecessary object reads.

## Overview

### Conditional Requests

**Available from OpenRiak KV 3.4.0.**

Conditional updates are very useful when looking to prevent siblings.  By default, any concurrent updates will lead to sibling generation, and handling siblings within application code may be expensive (and in some cases may require user intervention).  This can be controlled by making PUT requests conditional, with configurable degrees of strictness on how the condition will be checked to prevent concurrent changes.

> Conditional updates allow for improved consistency, but not formal consistency.

There are four levels of strictness to the application of conditions:

- api_only;
  - this is the loosest check; in this case when the PUT request has been received and parsed by Riak, it will check that the object has not changed (if_not_modified) or does not exist (if_none_match).
  - there remains broad scope for parallel writes leading to siblings in this case.
- prefer_token and head_only;
  - in this form, the process controlling the PUT within Riak must first get a token for the object key from the token manager, and the token manager will only grant a token to one process at a time;
  - the granting of tokens is managed by the node at the head of the preflist, and only the node at the head of the preflist;
  - in a cluster without failure or administrative cluster changes this will prevent concurrent writes, with a minimal performance overhead.
- prefer_token and basic_consensus;
  - in this form, the process controlling the PUT within Riak must first get a token for the object key from the token manager, and the token manager will only grant a token to one process at a time;
  - the granting of tokens is managed by consensus between available unique nodes in the preflist (either primary or fallback);
  - in a cluster without failure or administrative cluster changes this will prevent concurrent writes;
  - tokens can still be granted in a wide range of failure scenarios safely, but with a risk of duplicate grants, in particular should a cluster be partitioned.
- prefer_token and primary_consensus;
  - in this form, the process controlling the PUT within Riak must first get a token for the object key from the token manager, and the token manager will only grant a token to one process at a time;
  - the granting of tokens is managed by consensus between 3 of 5 primary nodes in a preflist;
  - to use this node, the cluster must be built with a target_n_val of at least 5;
  - in a cluster without failure or administrative cluster changes this will prevent concurrent writes
  - the chance of duplicate grants in this scenario is very small, but non-zero;
  - there will be no failure to grant as long as there are no more than two nodes down or unreachable within the cluster.

The level of strictness is set for the entire cluster, using the `conditional_put_mode` and `token_request_mode` configuration items in `riak.conf`:

```console
riak admin describe conditional_put_mode
riak admin describe token_request_mode
```

A failure of a conditional request will result in a `412: Precondition Failed` response.  Note, that data is not secure at this point, and is vulnerable to the failure of the application, if it was not stored already in an OpenRiak cluster prior to making the conditional change (e.g. when using Riak in an Event Source / CQRS model).

Tests have verified that in non-exceptional scenarios, simple failure events and cluster administration changes will lead to the promise of consensus being upheld (with both basic and primary consensus). This however, is not equal to strong consistency by any formal definition.  There will be complex and potentially unexpected scenarios where the condition will not be applied in a serialised way.  Riak remains an eventually consistent store, to protect data in all scenarios still requires the setting of `allow_mult = true` and the potential return of multiple (sibling) content values to an object read request.

There are three scenarios where the conditional check will be weakened:

- The token granting system uses an internal queue method, and requests made whilst the token has been currently granted will be notified to re-request for a grant when it is their turn for the grant.  So sending multiple requests in parallel will generally result in one update succeeding, and then all other parallel requests failing due to the precondition check in rapid succession as they gain ownership of the token when the previous request releases.  There is though a timeout, beyond which a process will not wait, and on timeout a process will revert to an `api_only` check.
- The token granting system is enforced as **an honesty system**, it is the role of the application to ensure that all objects that require token protection have conditions added to update requests.  Updates without condition checks will be accepted in parallel to updates with condition checks, and there may be unresolved conflicts as a consequence.
- When using multi-data centre replication, there is no cross-checking between clusters before granting tokens.  If running multiple clusters in active/active mode, then token consensus offers no protection against parallel writes, unless there is natural isolation within the application (e.g. should objects have a natural association with a region that would make inter-cluster concurrent writes unexpected).

Stronger conditional updates can be made via either API through the use of "if-none-match" and the Riak-bespoke "if-not-modified" headers (or options in the case of the PB API).  Use of the HTTP-standard "if-unmodified-since" header or of the "if-match" header will result only in weak `api_only` checks, and is not fully supported.

#### Use of Request Header - If-None-Match

The use of if-none-match is tested on update operations only.  It uses the standard HTTP request header, but ignores the value - setting the request header to any content will be treated as `if-none-match: *`.  The purpose of if-none-match is simply to check that there is no object present before accepting the update.

#### Use of Request Header - X-Riak-If-Not-Modified (non-standard Riak header)

The use of `X-Riak-If-Not-Modified` varies from the standard behaviour of the `If-Unmodified-Since`/`If-Match` HTTP request.  For Riak the `X-Riak-If-Not-Modified` header should be used as a modification check, and the value of the header should be set to the encoded version vector that had been read prior to the update.  The PUT will then be conditional on the object being at this state before the change is applied.

For the standard HTTP headers, [`If-Unmodified-Since`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Unmodified-Since) checks on the last-modified date, but this is not a sufficiently accurate check in Riak.  This option may be ignored in future releases.  The [`If-Match`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Match) header matches against the ETag of an object, however in Riak due to siblings, an object may have multiple tags (ETag in HTTP is mapped to vtag in the Riak object space).  The use of `If-Match` is not recommended, and will be clarified in a future release.
