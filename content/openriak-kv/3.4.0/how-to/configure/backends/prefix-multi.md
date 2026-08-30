---
title: 'Configure the Prefix Multi backend'
description: 'Show operators how to configure the prefix multi backend without losing access to required data.'
weight: 8
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-prefix_multi.md'
migration_review:
  - 'Prefix multi inherits the OpenRiak KV 3.4 multi-backend deprecation and requires careful review.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to configure the prefix multi backend without losing access to required data.

## Before you begin

Administrative access to the nodes you will change; a copy of the current configuration; and a maintenance window if the setting requires a restart.

## Overview

> [!WARNING]
> Migration review required: Prefix multi inherits the OpenRiak KV 3.4 multi-backend deprecation and requires careful review.

## Verify the result

Confirm that the intended setting is active on every affected node, then check cluster health and the relevant logs for warnings.
