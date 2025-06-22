---
sidebar_position: 204
title: How to Configure the Leveled Backend
sidebar_label: Leveled Backend
sidebar_custom_props:
  icon: settings
pagination_label: Configure Leveled
sidebar_class_name: kv-configure-guides-backends-leveled
---
import { ConfigReferenceProvider } from '@site/src/components/ConfigReference/ConfigReferenceContext';
import { ConfigListing }           from '@site/src/components/ConfigReference/ConfigListing';
import ChosenOS                    from '@site/src/components/OSSelection/ChosenOS';
import { ConfigDefaultValue }      from '@site/src/components/ConfigReference/ConfigDefaultValue';

<ConfigReferenceProvider configNamePattern='^(storage_backend|leveled\.|platform_data_dir).*'>

# How to Configure Leveled

## Recommended Configuration

The defaults for Leveled are designed for most use-cases. As such, you only need to set these two values:

```
storage_backend = leveled
leveled.data_root = "$(platform_data_dir)/leveled"
```

Note: `$(platform_data_dir)` will be replaced at run-time with the value for the configuration setting `platform_data_dir`. This varies by operating system. For <ChosenOS type="plaintext" /> the default is <ConfigDefaultValue name="platform_data_dir" hidePlatform="true" />.

## Quick Config Reference

The configuration options relating to the Leveled storage backend are listed below.

<ConfigListing />
</ConfigReferenceProvider>