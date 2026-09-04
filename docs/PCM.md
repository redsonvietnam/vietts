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

## Role and execution model

PCM roles are defined by **responsibility and execution topology**, not by model intelligence.

### AUTHORITY

An actor whose approval can cause a proposed state to become canonical.

Typical examples:

```text
R1
Human
```

Responsibilities include architecture decisions, cross-workstream decisions, contract/constraint decisions, review, Gate approval, and final override.

### PROPOSER

An actor that can reason about and produce a proposed state transition, but does not have authority to approve its own output.

Typical example:

```text
CC
```

CC may inspect the repository, reason about implementation, modify code, run tests/commands, commit, push, and propose a change. CC is not defined as a lower-intelligence role than R1; R1 and CC may use the same underlying model and have comparable reasoning capability. Their distinction is primarily authority, scope, context, and responsibility.

### OPERATOR

An actor with a persistent execution environment that is well suited to environment-heavy or long-running work.

Typical examples:

```text
C1
C2
```

Typical strengths include local filesystem and terminal access, local services, persistent environment state, long-running tasks, repeated run → observe → modify loops, and build/runtime/benchmark work. Operator is not a lower-intelligence role; an Operator may use a very strong reasoning model.

### OBSERVER

An actor that observes or verifies state without owning the implementation.

Typical examples:

```text
CI
automated checks
benchmark runners
static analysis
```

An Observer produces information or evidence for the applicable workflow. It does not gain merge or Gate authority merely because a check succeeds.

### Contextual role assignment

An actor's role is contextual, not necessarily a permanent identity. The same underlying model may act as a PROPOSER, OPERATOR, or OBSERVER depending on the tools, permissions, and execution environment assigned to the TASK.

The current common mappings of CC to PROPOSER and C1/C2 to OPERATOR are practical defaults, not universal PCM rules.

## Executor selection

**Prefer the shortest capable execution path.**

Use the executor that can complete the TASK with the fewest unnecessary handoffs while still satisfying the required reasoning, environment, verification, and authority constraints.

Examples:

```text
Reasoning-heavy repository code change
→ CC may be the shortest capable path.

Local runtime/debugging issue
→ C1/C2 may be the shortest capable path.

Long-running terminal/build/benchmark operation
→ C1/C2 may be the shortest capable path.

Architecture or authority decision
→ R1.

Cross-workstream decision
→ R1.
```

Executor selection is based primarily on TASK topology, not on the question "Which AI is smarter?" Useful characteristics include reasoning/invariant complexity, environment dependence, feedback-loop persistence, execution duration, context scope, and authority requirement. These characteristics are not a scoring formula.

If correct execution requires knowledge or an architecture decision outside the current WORKSTREAM, involve R1. A task that is not sufficiently specified should go to R1 before implementation.

## WORKSTREAM decomposition

Workstream decomposition matters more than maximizing the number of agents.

Prefer workstreams whose relevant contract/constraint surfaces are as disjoint as practical. Parallel execution is appropriate when affected surfaces are disjoint or explicitly coordinated.

PCM does not require a complex locking system.

## Multi-agent principle

Adding another capable executor is not automatically beneficial. Before introducing another execution hop, ask:

```text
Does this executor provide a capability that the previous executor lacks?
```

If not, the additional handoff is probably unnecessary.

Prefer:

```text
R1 → CC → GATE
```

over:

```text
R1 → CC → C1 → GATE
```

when C1 adds no required capability. Prefer:

```text
R1 → C1 → GATE
```

when the TASK genuinely depends on C1's persistent/local execution environment.

PCM does not require separate permanent roles such as security reviewer, performance reviewer, test agent, integrator, or release agent. A specialized role should exist only when it owns a genuinely distinct responsibility or authority boundary. Specialized verification can normally remain a TASK/executor assignment.

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

```text
Executor
    ≠
Approver
```

```text
Implementation success
    ≠
Acceptance
```

An executor must not approve its own implementation. This is a PCM rule; the repository should not be assumed to machine-enforce identity separation unless such enforcement is explicitly configured.

Independent verification is risk-dependent, not universally mandatory. Different identity or session alone does not guarantee meaningful independent verification. Strong verification may instead require a different method, evidence source, or failure model. Changes involving important contracts, high-risk boundaries, or high blast radius should receive stronger independent verification.

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
- **CC** commonly acts as a PROPOSER for reasoning-heavy implementation when appropriate.
- **C1/C2** commonly act as OPERATORS for execution-heavy work when their environment is the shortest capable path.
- Any of these actors may take another contextual role when the TASK, tools, permissions, and environment require it.
- **GitHub** provides persistent repository state.
- **HANDOFF** keeps work transferable across sessions.
- Proposed changes become canonical only after the applicable Gate.

This is the repository's current operating model; it does not claim that every historical task in the repository followed PCM formally.
