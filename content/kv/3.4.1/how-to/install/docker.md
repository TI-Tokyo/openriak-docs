---
title: 'Run OpenRiak with Docker'
description: 'Show operators how to run openriak with docker and confirm that the installation is ready.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'proposed-kv'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\setup\install\docker\alpine-linux.md'
migration_review:
  - 'Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.1 and require technical verification.'
  - 'Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages.'
  - 'No matching OpenRiak KV 3.4.1 package was found in the official 3.4 package index for this platform.'
  - 'Legacy version text or MDX syntax remains and requires editorial review.'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to run openriak with docker and confirm that the installation is ready.

## Before you begin

A supported operating system and package source, verified backups, release notes for the exact target version, and a rolling-change plan for production clusters.

## Overview

> [!WARNING]
> Migration review required: Commands or links derived from the 3.2.5 documentation were version-normalized for 3.4.1 and require technical verification; Release-specific installation, upgrade, downgrade, or quick-start instructions require verification against OpenRiak KV 3.4.1 packages; No matching OpenRiak KV 3.4.1 package was found in the official 3.4 package index for this platform; Legacy version text or MDX syntax remains and requires editorial review.

## Verify the result

Confirm the installed version on every node, wait for services and transfers to settle, and run application smoke tests before proceeding.
