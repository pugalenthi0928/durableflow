# ADR-0001: Start with one process and memory

- **Status:** accepted for Stage 1 only
- **Date:** 2026-08-18

## Context

DurableFlow must eventually teach persistence, asynchronous workers, distributed failure,
containers, AWS, and Kubernetes. Introducing them before a concrete failure would obscure the
product journey and make it difficult to know which mechanism solves which problem.

## Decision

Build the first vertical slice as one FastAPI process with:

- an in-memory repository;
- a deterministic processor;
- synchronous HTTP processing; and
- a framework-free browser page.

## Alternatives rejected for now

- **PostgreSQL:** correct eventual choice, but first we need to observe state loss.
- **Redis:** adds no authoritative capability required by Stage 1.
- **Celery/RabbitMQ/SQS:** hides durable handoff before the handoff problem is experienced.
- **React:** useful later for richer client state; plain browser APIs expose HTTP and JSON first.
- **Docker:** one Python process is not yet painful to install or run.
- **AWS/Kubernetes:** no legitimate deployment or orchestration problem exists.

## Consequences

The first version is easy to inspect and quick to change. It cannot uphold the future promise
that an accepted job survives restart. That failure is deliberate, documented, and tested.

## Removal criterion

Replace the memory repository when the learner has reproduced state loss, explained why process
memory is not authoritative storage, and designed the minimum PostgreSQL schema and transaction
boundary.

