---
title: 'To Do'
description: 'Review pages, documentation recommendations, and tests for OpenRiak KV 3.4.0.'
weight: -100
product: 'OpenRiak KV'
product_version: '3.4.0'
draft: true
hide_provenance: true
cascade:
  draft: true
  hide_provenance: true
---

Review work and recommendations for the OpenRiak KV 3.4.0 documentation. Start with [For Review](for-review/) to filter pages by their review metadata, or open [Tests](tests/) to check the site's rendering and shortcodes.

## Proposed documentation structure

The four proposal pages define the full intended site structure for Foundations, How-to, Reference, and Tutorials. They include existing pages worth retaining, pages to reorganise, and new coverage. Each table row names a proposed page and explains its scope.

- [Foundations](foundations/): 40 explanation pages in eight subsections.
- [How-to](how-to/): 148 task guides in 15 subsections.
- [Reference](reference/): 136 lookup pages in 13 subsections.
- [Tutorials](tutorials/): 39 guided learning pages in seven subsections.

Each proposed subsection also has a short landing page. These inventories describe the intended documentation; the actual reorganisation and page writing can be reviewed separately.

## Conventions across all four areas

- Use the defaults-table component for every product reference table. Use `configuration-reference-table` for configuration settings and `configuration-reference-item` for one setting; extend the component's columns and data sources for other reference schemas as described in the Reference proposal.
- Use the value shortcode (`load-value`) wherever a default value is stated, so the displayed value follows the documentation version and selected operating system. Add missing values to the authoritative metadata instead of copying defaults into prose.
- Label deliberate example values and overrides clearly, so readers can distinguish them from defaults.
- Keep explanations, task instructions, lookup details, and guided lessons in their respective areas, with links between them.

The Section / Name / Explanation tables on these proposal pages are editorial inventories of the intended site. Product reference tables in the resulting documentation should use the defaults-table component.
