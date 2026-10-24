---
title: 'Mermaid diagrams'
description: 'SVG diagram examples rendered locally with Pele.'
weight: 997
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'test-page'
draft: true
features: []
concepts: ['documentation']
---

Use a fenced code block labelled `mermaid` to render an SVG diagram with
[Pele](https://github.com/obsidianmd/pele). Open **Mermaid source** beneath a
diagram to see its input. These simplified examples illustrate diagram syntax,
rather than specifying protocol behavior.

Check these examples in light and dark themes and at a narrow window width.
The SVGs are generated during the build and remain visible with JavaScript disabled.

## Flowchart: replicated write

```mermaid
flowchart LR
    accTitle: Replicated write
    accDescr: A client sends a write to a coordinator, which forwards it to three replicas.
    Client --> Coordinator
    Coordinator --> A[Replica A]
    Coordinator --> B[Replica B]
    Coordinator --> C[Replica C]
```

## Sequence: quorum response

```mermaid
sequenceDiagram
    accTitle: Quorum response
    participant C as Client
    participant N as Coordinator
    participant A as Replica A
    participant B as Replica B
    C->>N: PUT bucket/key
    par Replicate
        N->>A: Store object
        A-->>N: Acknowledge
    and Replicate
        N->>B: Store object
        B-->>N: Acknowledge
    end
    N-->>C: Write accepted
```

## State diagram: membership planning

```mermaid
stateDiagram-v2
    accTitle: Membership planning
    [*] --> Staged
    Staged --> Planned: Review plan
    Planned --> Staged: Revise changes
    Planned --> Committed: Commit plan
    Committed --> Transferring: Begin handoff
    Transferring --> Ready: Handoff complete
    Ready --> [*]
```

## Entity relationship: stored objects

```mermaid
erDiagram
    BUCKET_TYPE ||--o{ BUCKET : configures
    BUCKET ||--o{ OBJECT : contains
    OBJECT {
        string key
        string value
        string context
    }
```
