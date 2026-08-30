# OpenRiak KV editorial rewrite report

Generated: 2026-08-28 (Asia/Tokyo)

## Result

The migration tree contains 776 cohesive Diátaxis documents. Source wrappers and migration warnings were removed, legacy content was retained ahead of supplementary QuickDocs material, equivalent sections and repeated blocks were consolidated, and category pages now list their immediate children.

- Substantive pages editorially rewritten: 649
- Missing pages expanded into content specifications: 127
- Publication status: all pages remain drafts until their technical claims are tested against the exact product version

## Versions

| Version | Pages |
|---|---:|
| 3.4.0 | 385 |
| 3.4.1 | 390 |
| all | 1 |

## Diátaxis types

| Type | Pages |
|---|---:|
| explanation | 149 |
| how-to | 313 |
| reference | 264 |
| tutorial | 50 |

## Editorial rules applied

- Tutorial pages establish an outcome, prerequisites, verification, and next steps.
- How-to pages identify prerequisites and add a concrete verification stage without turning into conceptual surveys.
- Reference pages preserve exact source detail and receive neutral structure when source content had no usable sections.
- Explanation pages retain concepts and rationale while source-specific migration wrappers are removed.
- Source-free stubs now describe the evidence, examples, failure handling, version notes, and cross-links required before publication.
- Provenance fields and source URLs remain in front matter so technical reviewers can trace inherited claims.

## Review boundary

This pass reviews editorial cohesion and site integration. It does not claim that inherited OpenRiak KV 3.2.5 commands, defaults, or operational recommendations have been experimentally verified against 3.4.0 or 3.4.1. Every page is therefore marked 	echnical_review: required and remains draft: true.