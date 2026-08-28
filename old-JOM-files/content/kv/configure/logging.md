---
title: Logging configuration
sidebar_label: "Logging"
date: 2026-06-17
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }             from '@site/src/components/ConfigReference/ConfigListing';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';
import InlineCodeWithCopy          from '@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy';

[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[reference]: #configuration-reference


>[!MEMO]Configuring logging
>Logging in Riak KV is handled by a Basho-made but OpenSource logging framework for Erlang called [lager](https://github.com/OpenRiak/lager) .
>This section provides the full list of configuration options and their functions

## Configuration Reference

<ConfigReferenceProvider sectionName="Section with loggingg">

<ConfigTable />

</ConfigReferenceProvider>