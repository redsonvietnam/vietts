---
name: pcm-v1
description: Operate repository work under PCM v1 by treating docs/PCM.md as the semantic authority, selecting the shortest capable execution path, preserving authority boundaries, and producing transferable handoffs.
compatibility: opencode
---

# PCM v1 Operational Skill

## 1. PURPOSE

Operate repository work **under PCM v1**.

This skill is a procedure for applying PCM semantics during an OpenCode session. It is **not** a replacement, extension, or new authority layer for PCM.

### Semantic authority vs skill procedure

- **PCM semantics** are defined by `docs/PCM.md`.
- **This skill procedure** tells an OpenCode agent how to apply those semantics while executing a TASK.
- If this skill appears to conflict with `docs/PCM.md`, follow `docs/PCM.md` and escalate the conflict rather than inventing a new rule.

PCM's four primitives remain exactly:

```text
WORKSTREAM
TASK
HANDOFF
GATE
```

Do not introduce additional mandatory PCM primitives.

## 2. WHEN TO ACTIVATE

Activate this skill when repository work is being performed under PCM v1, especially when a TASK packet identifies a WORKSTREAM, TASK, role, Gate, or HANDOFF requirement.

If the repository does not contain `docs/PCM.md`, do not silently recreate PCM from memory. Report the missing canonical source and request the appropriate authority to establish or provide it.

## 3. CANONICAL SOURCE

Before beginning repository work:

1. Read `docs/PCM.md` directly from the current repository state.
2. Treat the repository state plus the applicable WORKSTREAM/TASK context as authoritative starting context.
3. Treat conversation memory, previous chat summaries, and assumptions as **non-canonical**.
4. Record the relevant PCM version when the TASK depends on a versioned constraint.
5. If the TASK packet supplies a canonical commit/ref, verify the repository state against it before editing when the environment permits.

Never use this skill as a substitute for reading `docs/PCM.md`.

## 4. ROLE IDENTIFICATION

Determine the actor's **contextual role for this TASK** from the assigned responsibility, permissions, tools, and execution environment.

PCM roles are not intelligence tiers and are not permanent identities:

- **AUTHORITY** — can approve a proposed state and cause it to become canonical at the applicable Gate.
- **PROPOSER** — can reason about and produce a proposed state transition but cannot approve its own output.
- **OPERATOR** — provides persistent/environment-heavy execution capability when that capability is needed.
- **OBSERVER** — verifies or observes state without owning implementation or gaining Gate authority.

Common mappings such as `R1 → AUTHORITY`, `CC → PROPOSER`, and `C1/C2 → OPERATOR` are contextual defaults, not PCM identity rules.

Do not infer authority from model capability, tool access, branch ownership, commit authorship, or successful execution.

## 5. TASK INTAKE

Before changing repository state, establish:

```text
WORKSTREAM
TASK
CONSTRAINT / CONTRACT VERSION (when applicable)
CONTEXTUAL ROLE
EXPECTED STATE CHANGE
REQUIRED VERIFICATION
APPLICABLE GATE / AUTHORITY
```

If the TASK is underspecified in a way that could change architecture, contract interpretation, scope, or authority, stop and route the ambiguity to the appropriate AUTHORITY before implementation.

If correct execution requires knowledge or a decision outside the current WORKSTREAM, involve the appropriate authority rather than guessing.

## 6. EXECUTOR SELECTION

Apply the PCM rule:

> **Prefer the shortest capable execution path.**

Choose the executor that can complete the TASK with the fewest unnecessary handoffs while satisfying reasoning, environment, verification, scope, and authority constraints.

Reason about TASK topology, not which AI is "smarter". Consider:

- reasoning and invariant complexity;
- environment dependence;
- need for a persistent feedback loop;
- execution duration;
- context scope;
- authority requirements.

Use these as qualitative considerations, not as a mandatory scoring formula.

Before adding another executor, ask:

```text
Does this executor provide a capability that the previous executor lacks?
```

If not, avoid the extra handoff.

Typical outcomes:

```text
Reasoning-heavy repository change
→ CC may be the shortest capable path.

Long-running local runtime/debugging
→ C1/C2 may be the shortest capable path.

Architecture or authority decision
→ route to AUTHORITY (commonly R1).
```

Do not introduce another agent merely because another capable agent exists.

## 7. STATE MODEL

Maintain the distinction:

```text
PROPOSED STATE
    ↓
GATE
    ↓
CANONICAL STATE
```

A working tree, commit, branch, pull request, or artifact may be a **proposed state**. Do not describe it as canonical merely because implementation or tests succeeded.

Repository state is the authoritative implementation state for the current work. Tooling such as Git or GitHub is an implementation mechanism, not PCM itself.

Branches and worktrees are not agent identities.

## 8. HANDOFF RULES

AI session context is not canonical. A transferable HANDOFF must allow a new executor/session to reconstruct relevant state from:

```text
repository state
+
WORKSTREAM / TASK context
+
HANDOFF
```

When a HANDOFF is required, use the PCM minimum structure:

```text
WORK STATE
CONSTRAINT / CONTRACT VERSION
EVIDENCE
OPEN RISK
NEXT ACTION
```

A HANDOFF does not imply TASK completion. State what is actually true, what evidence exists, what remains risky, and what should happen next.

Do not hide unresolved uncertainty in a handoff.

## 9. GATE / AUTHORITY RULES

A successful implementation, passing tests, clean build, commit, or push is evidence about the proposed state. It is **not itself approval**.

Never self-approve.

Keep these distinctions explicit:

```text
Executor ≠ Approver
Implementation success ≠ Acceptance
Proposed State ≠ Canonical State
```

Before an applicable Gate, check at minimum:

```text
1. Scope satisfied
2. Relevant constraints still valid
3. Required evidence present
4. Required verification performed
5. Authorized reviewer approves
```

If a Gate is required and the current actor lacks authority, stop at the appropriate boundary and route the proposal to the AUTHORITY. Do not silently convert a successful implementation into canonical state.

Independent verification is risk-dependent. For important contracts, high-risk boundaries, or high-blast-radius changes, seek stronger independent verification as required by the applicable workflow.

## 10. MULTI-AGENT ROUTING

PCM does not require a fixed agent chain or multiple agents per TASK.

Prefer the minimum capable path, for example:

```text
AUTHORITY → PROPOSER → GATE
```

when the PROPOSER can perform the work without another executor capability.

Use an OPERATOR when persistent/local execution capability is genuinely required:

```text
AUTHORITY → OPERATOR → GATE
```

Use additional handoffs only when they add a capability, verification method, scope boundary, or authority boundary that the previous path lacks.

Do not make PF/PAIRFLOW the parent of PCM. PF/PAIRFLOW may be referenced as an optional workflow/tooling implementation, while PCM remains conceptually independent.

Do not create permanent specialist roles unless a genuinely distinct responsibility or authority boundary requires them.

## 11. FAILURE / ESCALATION

Stop and escalate rather than guessing when:

- `docs/PCM.md` is missing or materially ambiguous;
- the WORKSTREAM or TASK scope is unclear;
- a contract/constraint version has changed in a way that affects the TASK;
- an architecture or cross-WORKSTREAM decision is required outside the actor's authority;
- the actor lacks a required execution capability;
- required verification cannot be performed;
- a Gate is required but no authorized approver is available;
- proposed state and canonical state cannot be reliably distinguished.

When escalating, preserve the current repository state and provide a HANDOFF with concrete evidence and the smallest clear next action.

Do not silently modify architecture, contracts, PCM semantics, or authority boundaries to unblock yourself.

## 12. OUTPUT CONTRACT

At the end of a PCM-governed TASK or when transferring work, report the actual state using:

```text
WORK STATE

CONSTRAINT / CONTRACT VERSION

EVIDENCE

OPEN RISK

NEXT ACTION
```

When a proposal has been produced, also identify:

```text
PROPOSED STATE
```

Never label a proposal as canonical before the applicable Gate has passed.

When reporting a repository change, include concrete evidence such as changed paths, validation results, commit/ref, and branch where available. Do not fabricate command output that was not actually observed.

## 13. EXAMPLES

### Scenario A — reasoning-heavy repository change

A TASK requires a non-trivial repository refactor, but no persistent local runtime or long-running environment is needed.

```text
Role: PROPOSER
Executor: CC may be shortest capable path
State: proposed until Gate
Next: verification → authorized Gate
```

Do not add C1 merely to increase the number of agents.

### Scenario B — long-running local runtime/debugging

A TASK requires repeated local service startup, observation, modification, and long-running runtime checks.

```text
Role: OPERATOR
Executor: C1/C2 may be shortest capable path
State: proposed until Gate
Next: collect runtime evidence → authorized Gate
```

The reason for choosing C1/C2 is execution topology, not a claim of lower or higher intelligence.

### Scenario C — implementation complete and tested

A proposed implementation passes its required tests and has been committed.

```text
Implementation: successful
State: PROPOSED
Canonical: no
Next: applicable Gate / authorized approval
```

Passing tests does not grant the executor authority to approve its own work.

## FINAL OPERATING RULE

When operating under PCM v1:

```text
Read canonical PCM
        ↓
Identify WORKSTREAM / TASK
        ↓
Identify contextual role
        ↓
Choose shortest capable execution path
        ↓
Make and verify proposed state
        ↓
Preserve HANDOFF-ready evidence
        ↓
Stop at authority boundary
        ↓
GATE
        ↓
Only then CANONICAL STATE
```

The skill operationalizes PCM. It does not redefine PCM.
