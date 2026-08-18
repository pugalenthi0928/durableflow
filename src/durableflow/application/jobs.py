from __future__ import annotations

import time
from typing import Protocol
from uuid import UUID

from durableflow.application.processor import process_text
from durableflow.domain.jobs import Job, JobState


class JobRepository(Protocol):
    def add(self, job: Job) -> None: ...

    def save(self, job: Job) -> None: ...

    def get(self, job_id: UUID) -> Job | None: ...


class JobService:
    def __init__(self, repository: JobRepository, *, processing_delay_seconds: float = 0) -> None:
        self._repository = repository
        self._processing_delay_seconds = processing_delay_seconds

    def create_and_process(self, *, filename: str, content: str) -> Job:
        job = Job.create(filename)
        self._repository.add(job)

        job.transition_to(JobState.RUNNING)
        self._repository.save(job)

        if self._processing_delay_seconds:
            time.sleep(self._processing_delay_seconds)

        result = process_text(content)
        job.transition_to(JobState.SUCCEEDED, result=result)
        self._repository.save(job)
        return job

    def get(self, job_id: UUID) -> Job | None:
        return self._repository.get(job_id)
