from datetime import UTC, datetime, timedelta

import pytest

from durableflow.domain.jobs import InvalidJobTransition, Job, JobResult, JobState


def result() -> JobResult:
    return JobResult(
        processor_version="test-v1",
        sha256="a" * 64,
        byte_count=4,
        word_count=1,
        line_count=1,
    )


def test_job_moves_from_queued_to_running_to_succeeded() -> None:
    created = datetime(2026, 8, 18, tzinfo=UTC)
    started = created + timedelta(seconds=1)
    completed = started + timedelta(seconds=2)
    job = Job.create("input.txt", now=created)

    job.transition_to(JobState.RUNNING, now=started)
    job.transition_to(JobState.SUCCEEDED, now=completed, result=result())

    assert job.state is JobState.SUCCEEDED
    assert job.started_at == started
    assert job.completed_at == completed
    assert job.result == result()


def test_terminal_job_cannot_transition_again() -> None:
    job = Job.create("input.txt")
    job.transition_to(JobState.RUNNING)
    job.transition_to(JobState.SUCCEEDED, result=result())

    with pytest.raises(InvalidJobTransition, match="cannot transition"):
        job.transition_to(JobState.RUNNING)


def test_success_requires_result() -> None:
    job = Job.create("input.txt")
    job.transition_to(JobState.RUNNING)

    with pytest.raises(InvalidJobTransition, match="requires a result"):
        job.transition_to(JobState.SUCCEEDED)


def test_failure_requires_reason() -> None:
    job = Job.create("input.txt")
    job.transition_to(JobState.RUNNING)

    with pytest.raises(InvalidJobTransition, match="requires a failure reason"):
        job.transition_to(JobState.FAILED)
