---
sidebar_position: 1
title: Configuration Reference
sidebar_label: Config Reference
pagination_label: Configuration Reference
sidebar_class_name: kv-configure-reference
id: kv-configure-reference
---

import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigTable }             from '@site/src/components/ConfigReference/ConfigTable';

<ConfigReferenceProvider>

## Configuration Reference

This page lists all configuration options available to the application. These are all set in <i>riak.conf</i>, and require a restart of an OpenRiak KV node to take effect. 

Dynamic setting of run-time application settings is sometimes possible, and those options will be indicated. 

<ConfigTable />
</ConfigReferenceProvider>