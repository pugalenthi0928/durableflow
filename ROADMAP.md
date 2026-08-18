# DurableFlow roadmap

Implementation and mastery are tracked separately. A checked implementation does not mean the
learner has passed the explanation and failure-experiment gate.

| Stage | Problem that earns the next mechanism | Implementation | Mastery |
|---:|---|---|---|
| 0 | The tool list has no concrete product promise | Prepared | Pending learner review |
| 1 | The product has no end-to-end proof | Prepared | Pending learner review |
| 2 | API semantics and errors are accidental | Next | Not started |
| 3 | Restart destroys authoritative state | Planned: PostgreSQL | Not started |
| 4 | Users can cross security boundaries | Planned: authentication/authorization | Not started |
| 5 | File bytes cannot live safely on API disk | Planned: object storage | Not started |
| 6 | Duplicate and conflicting writes break invariants | Planned: transactions/idempotency | Not started |
| 7 | A request takes 60 seconds | Planned: measure synchronous failure | Not started |
| 8 | Accepted in-process work dies with the API | Planned: background-task failure | Not started |
| 9 | Work needs durable ownership and recovery | Planned: PostgreSQL queue/workers | Not started |
| 10 | External APIs timeout or fail ambiguously | Planned: retry state machine | Not started |
| 11 | Users cannot observe durable progress | Planned: polling then SSE | Not started |
| 12 | Measured reads and abuse pressure the database | Planned: Redis/cache/rate limits | Not started |
| 13 | The local multi-process system is painful | Planned: Docker Compose | Not started |
| 14 | Happy-path tests miss real dependency behaviour | Planned: risk-shaped test portfolio | Not started |
| 15 | Changes lack reproducible delivery evidence | Planned: expanded CI/CD | Not started |
| 16 | A slow job cannot be explained | Planned: OpenTelemetry | Not started |
| 17 | Arrival rate exceeds service rate | Planned: load/backpressure | Not started |
| 18 | A laptop is not a production environment | Planned: first AWS deployment | Not started |
| 19 | API and worker resource profiles diverge | Planned: independently scaled roles | Not started |
| 20 | Replicas need reconciliation and rollout control | Planned: Kubernetes | Not started |
| 21 | Static capacity misses demand | Planned: HPA/custom metrics | Not started |
| 22 | Failures interact during real releases | Planned: reliability game day | Not started |

## AWS progression

AWS is introduced after local mechanisms are understood:

1. S3 for document bytes.
2. RDS PostgreSQL for authoritative state.
3. ECR and ECS Fargate for the first container deployment.
4. ALB, ACM, Route 53, VPC, security groups, IAM roles, Secrets Manager, and KMS.
5. ElastiCache only after Redis has a measured role.
6. CloudWatch plus OpenTelemetry for operating evidence.
7. SQS as a measured comparison with the PostgreSQL queue.
8. EKS only after local Kubernetes and independent API/worker scaling are understood.

## Refusal list

Do not add Kafka, microservices, a service mesh, GraphQL, Temporal, event sourcing, CRDTs,
multi-region active-active infrastructure, or GPU orchestration without a written observed
problem and a decision record.

