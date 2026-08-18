from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from durableflow.application.jobs import JobRepository, JobService
from durableflow.domain.jobs import Job, JobResult, JobState
from durableflow.infrastructure.memory_jobs import InMemoryJobRepository
from durableflow.logging import configure_logging

WEB_ROOT = Path(__file__).parent / "web"
MAX_TEXT_CHARACTERS = 100_000


class JobCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=MAX_TEXT_CHARACTERS)


class JobResultRead(BaseModel):
    processor_version: str
    sha256: str
    byte_count: int
    word_count: int
    line_count: int

    @classmethod
    def from_domain(cls, result: JobResult) -> JobResultRead:
        return cls(
            processor_version=result.processor_version,
            sha256=result.sha256,
            byte_count=result.byte_count,
            word_count=result.word_count,
            line_count=result.line_count,
        )


class JobRead(BaseModel):
    id: UUID
    filename: str
    state: JobState
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    result: JobResultRead | None
    failure_reason: str | None

    @classmethod
    def from_domain(cls, job: Job) -> JobRead:
        return cls(
            id=job.id,
            filename=job.filename,
            state=job.state,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            result=JobResultRead.from_domain(job.result) if job.result else None,
            failure_reason=job.failure_reason,
        )


class HealthRead(BaseModel):
    status: str
    storage: str


def _processing_delay_seconds() -> float:
    raw_value = os.getenv("DURABLEFLOW_PROCESSING_DELAY_MS", "0")
    try:
        delay_ms = int(raw_value)
    except ValueError as error:
        raise ValueError("DURABLEFLOW_PROCESSING_DELAY_MS must be an integer") from error
    if delay_ms < 0 or delay_ms > 300_000:
        raise ValueError("DURABLEFLOW_PROCESSING_DELAY_MS must be between 0 and 300000")
    return delay_ms / 1000


def create_app(repository: JobRepository | None = None) -> FastAPI:
    configure_logging()
    logger = logging.getLogger("durableflow.http")
    job_repository = repository or InMemoryJobRepository()
    service = JobService(
        job_repository,
        processing_delay_seconds=_processing_delay_seconds(),
    )

    app = FastAPI(
        title="DurableFlow",
        version="0.1.0",
        description="Stage 1: a deliberately non-durable, synchronous document processor.",
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = request.headers.get("x-request-id") or str(uuid4())
        started = time.perf_counter()
        response: Response
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.exception(
                "request_failed",
                extra={
                    "event_fields": {
                        "event": "http_request",
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "duration_ms": duration_ms,
                        "outcome": "unhandled_error",
                    }
                },
            )
            raise

        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["x-request-id"] = request_id
        logger.info(
            "request_complete",
            extra={
                "event_fields": {
                    "event": "http_request",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "outcome": "success"
                    if response.status_code < 400
                    else "client_or_server_error",
                }
            },
        )
        return response

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(WEB_ROOT / "index.html")

    @app.get("/healthz", response_model=HealthRead)
    def health() -> HealthRead:
        return HealthRead(status="ok", storage="memory")

    @app.post("/v1/jobs", response_model=JobRead, status_code=status.HTTP_201_CREATED)
    def create_job(payload: JobCreate) -> JobRead:
        job = service.create_and_process(filename=payload.filename, content=payload.content)
        return JobRead.from_domain(job)

    @app.get("/v1/jobs/{job_id}", response_model=JobRead)
    def get_job(job_id: UUID) -> JobRead:
        job = service.get(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job_not_found")
        return JobRead.from_domain(job)

    return app


app = create_app()
