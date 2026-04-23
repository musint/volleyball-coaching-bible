"""Unit tests for aoc_mcp.video helper functions."""
from aoc_mcp.video import _detect_provider, _vtt_to_plain_text


def test_detect_provider_vimeo():
    assert _detect_provider("https://player.vimeo.com/video/123456789?autoplay=1") == (
        "vimeo", "123456789"
    )


def test_detect_provider_wistia():
    assert _detect_provider("https://fast.wistia.net/embed/iframe/abcd1234") == (
        "wistia", "abcd1234"
    )


def test_detect_provider_unknown():
    assert _detect_provider("https://youtube.com/embed/xyz") is None


def test_vtt_to_plain_text_strips_timings_and_headers():
    vtt = (
        "WEBVTT\n\n"
        "1\n00:00:00.000 --> 00:00:02.500\nHello world\n\n"
        "2\n00:00:02.500 --> 00:00:05.000\nSecond cue\n"
    )
    assert _vtt_to_plain_text(vtt) == "Hello world\nSecond cue"
