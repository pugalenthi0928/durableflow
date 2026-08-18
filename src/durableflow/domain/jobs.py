from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


class JobState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


TERMINAL_STATES = frozenset({JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED})

ALLOWED_TRANSITIONS: dict[JobState, frozenset[JobState]] = {
    JobState.QUEUED: frozenset({JobState.RUNNING, JobState.CANCELLED}),
    JobState.RUNNING: frozenset({JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}),
    JobState.SUCCEEDED: frozenset(),
    JobState.FAILED: frozenset(),
    JobState.CANCELLED: frozenset(),
}


class InvalidJobTransition(ValueError):
    """Raised when a job is moved through an illegal state transition."""


@dataclass(frozen=True, slots=True)
class JobResult:
    processor_version: str
    sha256: str
    byte_count: int
    word_count: int
    line_count: int


@dataclass(slots=True)
class Job:
    id: UUID
    filename: str
    state: JobState
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: JobResult | None = None
    failure_reason: str | None = None

    @classmethod
    def create(cls, filename: str, *, now: datetime | None = None) -> Job:
        return cls(
            id=uuid4(),
            filename=filename,
            state=JobState.QUEUED,
            created_at=now or datetime.now(UTC),
        )

    def transition_to(
        self,
        next_state: JobState,
        *,
        now: datetime | None = None,
        result: JobResult | None = None,
        failure_reason: str | None = None,
    ) -> None:
        if next_state not in ALLOWED_TRANSITIONS[self.state]:
            raise InvalidJobTransition(f"cannot transition job from {self.state} to {next_state}")

        changed_at = now or datetime.now(UTC)

        if next_state is JobState.RUNNING:
            self.started_at = changed_at
        elif next_state is JobState.SUCCEEDED:
            if result is None:
                raise InvalidJobTransition("a successful job requires a result")
            self.completed_at = changed_at
            self.result = result
        elif next_state is JobState.FAILED:
            if not failure_reason:
                raise InvalidJobTransition("a failed job requires a failure reason")
            self.completed_at = changed_at
            self.failure_reason = failure_reason
        elif next_state is JobState.CANCELLED:
            self.completed_at = changed_at

        self.state = next_state
