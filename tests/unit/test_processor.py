import hashlib

from durableflow.application.processor import PROCESSOR_VERSION, process_text


def test_processor_is_deterministic() -> None:
    content = "hello durable world\nsecond line"

    first = process_text(content)
    second = process_text(content)

    assert first == second
    assert first.processor_version == PROCESSOR_VERSION
    assert first.sha256 == hashlib.sha256(content.encode("utf-8")).hexdigest()
    assert first.byte_count == len(content.encode("utf-8"))
    assert first.word_count == 5
    assert first.line_count == 2


def test_processor_counts_utf8_bytes_not_characters() -> None:
    result = process_text("café")

    assert result.byte_count == 5
    assert result.word_count == 1
    assert result.line_count == 1
