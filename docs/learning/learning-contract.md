# Learning contract

DurableFlow is successful only if the learner can direct, inspect, and operate the system without
depending on an AI agent to supply the reasoning.

## The learner owns

- requirements and non-goals;
- system boundaries and data ownership;
- invariants and legal state transitions;
- API and transaction semantics;
- concurrency and retry behaviour;
- authentication and authorization assumptions;
- testing strategy and acceptance criteria;
- deployment, recovery, and security decisions; and
- the explanation of observed production behaviour.

## AI may help with

- boilerplate and project scaffolding;
- repetitive models and endpoint wiring;
- migration drafts after the schema is approved;
- test scaffolding and fixture generation;
- Docker, CI, Terraform, and Kubernetes drafts;
- refactoring and mechanical documentation; and
- generating fault and load-test harnesses from a human-owned hypothesis.

## Mastery gate for every stage

Without reading the implementation, explain:

1. the user promise;
2. every component and responsibility;
3. the request and data flow;
4. authoritative, derived, cached, and ephemeral state;
5. all network boundaries;
6. the invariant and where it is enforced;
7. the predicted outcome when each component fails;
8. the chosen solution and two alternatives;
9. the reason the next popular technology is still refused; and
10. the test and telemetry evidence supporting the claim.

## Evidence record

Each stage should leave behind:

- a design or architecture document;
- an ADR;
- implementation and appropriate tests;
- a completed failure-lab report;
- a short learner-written explanation;
- relevant logs, traces, metrics, or query plans; and
- an atomic commit history linked to the issue.

