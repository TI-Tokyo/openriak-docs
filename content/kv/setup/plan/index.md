---
sidebar_position: 1
title: Planning your OpenRiak KV cluster
sidebar_label: Plan
sidebar_custom_props:
  icon: todo-list
pagination_label: Planning
sidebar_class_name: kv-setup-plan
date: 2025-09-16
---

# Planning your OpenRiak KV cluster

You should decide in advance some important settings that are hard to change once your cluster is up.

- hardware type (arm/intel)
- physical layout (multi-rack, multi-availability-zone, multi-vm-on-box)
- how many copies of your data you want (3 is recommended and the default)
- what type of backend, and where should it store your data
