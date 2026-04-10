---
sidebar_position: 201
title: TicTac Active Anti-Entropy
sidebar_label: TicTac Active Anti-Entropy
sidebar_custom_props:
  icon: settings
pagination_label: Configure Leveled
sidebar_class_name: kv-configure-backends-leveled
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]

> [!IDEA]Overview
> TicTac Active Anti-Entropy makes two changes to the way Anti-Entropy has previously worked in Riak. The first change is to the way Merkle Trees are contructed so that they are built incrementally. The second change allows the underlying Anti-entropy key store to be key-ordered while still allowing faster access to keys via 
their Merkle tree location or the last modified date of the object.

