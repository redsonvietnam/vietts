# PCM ↔ PAIRFLOW Bridge

## Purpose

This document explains the relationship between PCM (Project Coordination Model) and PAIRFLOW (Pair-Flow Operational Profile). It is a reference bridge, not a replacement for either specification.

## Semantic Mapping

```text
PCM AUTHORITY          →  PAIRFLOW R1
PCM PROPOSER / OPERATOR →  PAIRFLOW execution roles (C1, C2, etc.)
PCM GATE               →  PAIRFLOW approval / decision gate
PCM HANDOFF            →  PAIRFLOW handoff-with-evidence
PCM WORKSTREAM / TASK  →  PAIRFLOW workstream/task execution structure
```

## Key Distinctions

- **PCM** defines the semantic coordination protocol: what WORKSTREAM, TASK, HANDOFF, and GATE mean.
- **PAIRFLOW** defines the operational profile: how roles (R1, C1, C2) execute work within PCM semantics.
- PCM is protocol. PAIRFLOW is tooling/implementation. Neither is the parent of the other.

## Authority

- PCM semantic authority is defined by `docs/PCM.md`.
- PAIRFLOW operational procedures are defined by `docs/pairflow/` (or `.agents/skills/pairflow/`).
- If this bridge conflicts with `docs/PCM.md`, follow `docs/PCM.md`.

## Usage

This bridge exists so that repositories adopting PAIRFLOW can reference PCM semantics without duplicating protocol definitions. Repositories should reference their local `docs/PCM.md` for canonical PCM rules and this bridge for the relationship mapping.
