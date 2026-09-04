# PCM v1 — Project Coordination Model v1

## Purpose

PCM v1 is the repository workflow protocol for coordinating software work across sessions and executors. It preserves transferable work context and separates execution from authority.

Canonical flow:

```text
WORKSTREAM
    ↓
TASK
    ↓
EXECUTOR
    ↓
STATE CHANGE
    ↓
HANDOFF
    ↓
GATE
    ↓
CANONICAL STATE
```

The four core primitives are **WORKSTREAM**, **TASK**, **HANDOFF**, and **GATE**. No additional primitives are defined here.

## Core primitives

### WORKSTREAM

An ownership boundary. It groups related work under one scope and its relevant constraints.

### TASK

The atomic unit of execution within a WORKSTREAM. A TASK proposes one or more state changes.

### HANDOFF

A persistent bridge across sessions or executors. It allows a new session to continue without relying on the previous session's memory.

Minimum useful HANDOFF content:

```text
WORK STATE
CONSTRAINT / CONTRACT VERSION
EVIDENCE
OPEN RISK
NEXT ACTION
```

A HANDOFF does not necessarily mean that a TASK is complete.

### GATE

An authority checkpoint. A proposed state is not canonical until it passes the applicable Gate.

## Core invariants

```text
Agent ≠ Authority
Implementation ≠ Approval
Proposed State ≠ Canonical State
Context ≠ Canonical State
Protocol ≠ Tooling
```

Operational meaning:

- **Agent ≠ Authority:** performing work does not grant authority to approve it.
- **Implementation ≠ Approval:** completing a change and approving that change are separate responsibilities.
- **Proposed State ≠ Canonical State:** a working tree, commit, branch, PR, or artifact can represent a proposal; it becomes canonical only after the applicable Gate.
- **Context ≠ Canonical State:** conversation memory or session context is not authoritative project state.
- **Protocol ≠ Tooling:** PCM defines coordination rules independently of GitHub, Git, or any other tool.

## Executor model

### R1

Architecture, authority, review, and Gate role.

R1 may:

- define or change constraints;
- resolve cross-workstream decisions;
- review implementation;
- approve or reject the Gate.

### CC

**Reasoning-heavy executor.** Use CC when implementation must maintain multiple non-local invariants simultaneously across a change.

CC may inspect code, design implementation within the approved boundary, modify code, run tests, commit, and open a proposed change. CC does not self-approve its own result.

### C1 / C2

**Execution-heavy executors.** Use for bounded, local, mechanically verifiable, high-volume, or test-driven work. C1/C2 also do not self-approve their own changes.

### Human

Ultimate authority and override.

## Routing guideline

Do not use a scoring system.

**Question 1 — non-local invariants:** Does implementation require simultaneously preserving multiple non-local invariants throughout the diff?

- No → use an execution-heavy executor.
- Yes → use a reasoning-heavy executor (CC).

**Question 2 — external architecture knowledge:** Does correct execution require knowledge or an architecture decision outside the current WORKSTREAM?

- Yes → involve R1.
- No → remain within the current execution boundary.

A task that is not sufficiently specified should go to R1 before implementation.

## WORKSTREAM decomposition

Workstream decomposition matters more than maximizing the number of agents.

Prefer workstreams whose relevant contract/constraint surfaces are as disjoint as practical. Parallel execution is appropriate when affected surfaces are disjoint or explicitly coordinated.

PCM does not require a complex locking system.

## State model

```text
PROPOSED STATE
    ↓
GATE
    ↓
CANONICAL STATE
```

Examples of proposed state include:

```text
working tree
commit
branch
pull request
artifact
```

The exact mechanism is tooling-dependent. In this repository, Git/GitHub is the current implementation mechanism for source state and review. PCM does not assume GitHub is the only possible implementation.

## HANDOFF rule

AI context is not canonical. A new session reconstructs relevant state from:

```text
repository state
+
WORKSTREAM / TASK context
+
HANDOFF
```

A conversation transcript is not canonical state.

## GATE rules

A minimum Gate checks:

```text
1. Scope satisfied
2. Relevant constraints still valid
3. Required evidence present
4. Required verification performed
5. Authorized reviewer approves
```

An executor must not approve its own implementation.

Independent verification is risk-dependent, not universally mandatory. Changes involving important contracts, high-risk boundaries, or high blast radius should receive stronger independent verification.

## Contract / constraint versioning

A TASK that depends on a versioned constraint should record the relevant version at task start.

Before Gate, check whether the relevant constraint has changed. If it has, the TASK may require re-verification before acceptance.

Where a contract has independently versioned clauses, a TASK may reference only the clauses it depends on.

No database or elaborate contract-management system is required by PCM.

## GitHub / branch / worktree

```text
PCM protocol
    ≠
Git branch
    ≠
Git worktree
    ≠
AI identity
```

Branches and worktrees are implementation mechanisms. A branch is not an agent identity. CC may work on a dedicated branch for a TASK, but that branch represents proposed code state, not the permanent identity of CC.

## How PCM is currently used in this repository

- **R1** coordinates architecture and Gates.
- **CC** handles reasoning-heavy implementation when appropriate.
- **C1/C2** handle execution-heavy work.
- **GitHub** provides persistent repository state.
- **HANDOFF** keeps work transferable across sessions.
- Proposed changes become canonical only after the applicable Gate.

This is the repository's current operating model; it does not claim that every historical task in the repository followed PCM formally.
