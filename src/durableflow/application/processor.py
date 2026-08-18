from __future__ import annotations

import hashlib
import re

from durableflow.domain.jobs import JobResult

PROCESSOR_VERSION = "text-statistics-v1"
WORD_PATTERN = re.compile(r"\S+")


def process_text(content: str) -> JobResult:
    encoded = content.encode("utf-8")
    return JobResult(
        processor_version=PROCESSOR_VERSION,
        sha256=hashlib.sha256(encoded).hexdigest(),
        byte_count=len(encoded),
        word_count=len(WORD_PATTERN.findall(content)),
        line_count=len(content.splitlines()) if content else 0,
    )
