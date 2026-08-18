from __future__ import annotations

from uuid import UUID

from durableflow.domain.jobs import Job


class DuplicateJobError(ValueError):
    """Raised if a repository receives the same job identifier twice."""


class InMemoryJobRepository:
    """A deliberately non-durable repository scoped to one Python process."""

    def __init__(self) -> None:
        self._jobs: dict[UUID, Job] = {}

    def add(self, job: Job) -> None:
        if job.id in self._jobs:
            raise DuplicateJobError(f"job {job.id} already exists")
        self._jobs[job.id] = job

    def save(self, job: Job) -> None:
        if job.id not in self._jobs:
            raise KeyError(f"job {job.id} does not exist")
        self._jobs[job.id] = job

    def get(self, job_id: UUID) -> Job | None:
        return self._jobs.get(job_id)
