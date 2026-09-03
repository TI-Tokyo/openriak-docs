---
title: 'Configuration reference table test'
description: 'Exercise configuration table filtering, datatype rendering, copy controls, and operating-system-specific defaults.'
weight: 999
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'test-page'
draft: true
audience:
  - 'operators'
  - 'developers'
source_material:
  - 'generated-configuration-metadata'
tags: ['kv', 'reference', 'configuration', 'test']
editorial_review: 'not-required'
technical_review: 'required'
last_reviewed: '2026-09-02'
review_scope: 'shortcode-integration'
related:
  - page: 'reference/configuration'
    reason: 'Understand the configuration files and their precedence.'
  - page: 'reference/faq'
    title: 'Frequently asked questions'
---

Use this draft page to exercise the configuration reference table. Change the selected operating system and verify that defaults and OS badges update without reloading the page. The copy buttons should copy the mapping name, internal name, or currently displayed default.

## Multiple additive filters

Each non-empty shortcode body line is an independent regular expression. Matching settings from every line are added to the table. The first expression deliberately contains a comma to confirm that commas remain part of a regular expression rather than acting as separators.

{{< configuration-reference-table >}}
^bitcask\.(data_root|io_mode|sync\.strategy)(?:,legacy)?$
^backend_pause_ms$
^platform_lib_dir$
{{< /configuration-reference-table >}}

## Single configuration item

This renders one exact configuration key as a compact detail table and follows the currently selected operating system when displaying its default.

{{< configuration-reference-item config-name="mdc.fullsync_interval.$cluster_name" >}}

### Enum-valued item

This second example exercises the per-value copy controls for an enum.

{{< configuration-reference-item config-name="anti_entropy" >}}

## Repository area and filters

The `area` parameter limits matches to settings defined by the `riak_repl` repository. The body expressions are still additive within that area.

{{< configuration-reference-table area="riak_repl" >}}
^mdc\.fullsync\.stat_refresh_interval$
^mdc\.fullsync_(on_connect|interval\.\$cluster_name)$
{{< /configuration-reference-table >}}

# single item detail

{{< configuration-reference-item config-name="mdc.fullsync_interval.$cluster_name" >}}