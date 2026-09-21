---
title: Configuration files, syntax, and precedence
weight: 80
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: OpenRiak uses `riak.conf` for schema-backed settings and `advanced.config` for Erlang application configuration
  that needs the advanced form. Paths and supported settings depend on the installed package.
related:
- reference/configuration/all-configuration-settings-and-defaults
- how-to/node-configuration/add-advanced-configuration
- how-to/node-configuration/inspect-and-manage-effective-configuration
- how-to/node-configuration/validate-configuration-before-startup
- foundations/data-and-consistency/bucket-types-and-data-policies
---

OpenRiak uses `riak.conf` for schema-backed settings and `advanced.config` for Erlang application configuration that needs the advanced form. Paths and supported settings depend on the installed package.

## riak.conf

Entries use `name = value`. The schema determines the accepted datatype, enum choices, units, and constraints. Names containing a placeholder such as `$name` describe a family of named entries; replace the placeholder with the intended entry name.

Commented examples do not set an effective value. An explicit value remains an override when a later package changes its default.

## advanced.config

The advanced file contains an Erlang term listing application configuration. It must be syntactically valid, including the terminating full stop. Values in advanced configuration can override schema-generated application values, so inspect both files when diagnosing an unexpected setting.

Keep a setting in one managed location where possible. The schema's public name and its internal application key need not be identical; the generated catalogue shows the mapping when available.

## Validation and activation

Use {{< cli key="shell:riak chkconfig" >}} before starting with changed configuration. A syntax check does not establish that a port is reachable, a certificate is trusted, or an existing backend is compatible with a new selection. Restart and runtime-change requirements depend on the setting and its supported command interface.
