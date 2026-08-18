# Contributing and learning protocol

DurableFlow is both software and an engineering learning record. Changes should make the
reasoning easier to inspect, not merely increase the contribution graph.

## Before implementation

Create or update an issue containing:

- the user or operational problem;
- the current limitation;
- the predicted failure;
- the invariant involved;
- at least two possible solutions;
- what is explicitly out of scope; and
- measurable acceptance criteria.

## Definition of done

A change is complete only when the relevant items exist:

- implementation;
- automated tests at the appropriate fidelity;
- a deliberate failure experiment;
- structured evidence such as logs, metrics, traces, query plans, or screenshots;
- documentation of the design decision and rejected alternatives; and
- a learner explanation of data flow, state ownership, failure semantics, and rollback.

## Atomic commit policy

Use small, coherent commits that build toward one issue. Valid prefixes include:

```text
feat:       new user-visible behaviour
fix:        correction of a demonstrated defect
test:       executable evidence
docs:       reasoning, runbooks, diagrams, or experiment results
refactor:   structural change without intended behaviour change
perf:       measured performance improvement
security:   security-boundary improvement
ops:        deployment or operational behaviour
infra:      infrastructure definition
experiment: controlled failure or performance setup
chore:      necessary repository maintenance
```

Do not create empty commits, split one logical edit mechanically, commit generated caches, or
make cosmetic edits only to increase the count.

## AI-assisted changes

AI may draft boilerplate, tests, configuration, documentation, and bounded refactors. The
human author remains responsible for requirements, invariants, data ownership, transactions,
authorization, failure semantics, retry policy, security assumptions, testing strategy, and
operational acceptance.

Every AI-assisted change must be explainable without asking the agent.

