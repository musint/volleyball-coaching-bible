"""Tests for auth.py — specifically the non-interactive cookie import paths."""
import json
from pathlib import Path

from aoc_mcp.auth import run_import_from_cookie_header
from aoc_mcp import config


def test_cookie_header_parses_multiple_pairs(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    hdr = "wordpress_logged_in_abc=xyz123; PHPSESSID=foo; other=bar"
    input_file = tmp_path / "hdr.txt"
    input_file.write_text(hdr)

    rc = run_import_from_cookie_header(str(input_file))
    assert rc == 0

    saved = json.loads(config.SESSION_FILE.read_text())
    names = [c["name"] for c in saved["cookies"]]
    assert "wordpress_logged_in_abc" in names
    assert "PHPSESSID" in names
    assert "other" in names
    # All cookies tagged for the AOC domain
    for c in saved["cookies"]:
        assert c["domain"] == ".theartofcoachingvolleyball.com"
        assert c["path"] == "/"


def test_cookie_header_strips_cookie_prefix(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    hdr = "Cookie: wordpress_logged_in_abc=xyz; foo=bar"
    input_file = tmp_path / "hdr.txt"
    input_file.write_text(hdr)

    rc = run_import_from_cookie_header(str(input_file))
    assert rc == 0

    saved = json.loads(config.SESSION_FILE.read_text())
    names = [c["name"] for c in saved["cookies"]]
    assert "wordpress_logged_in_abc" in names
    # Make sure the "Cookie" literal didn't become a cookie itself
    assert "Cookie" not in names


def test_cookie_header_empty_input_returns_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    input_file = tmp_path / "hdr.txt"
    input_file.write_text("   \n  ")

    rc = run_import_from_cookie_header(str(input_file))
    assert rc == 1
    captured = capsys.readouterr()
    assert "empty" in captured.err.lower()


def test_cookie_header_missing_file_returns_error(tmp_path, capsys):
    rc = run_import_from_cookie_header(str(tmp_path / "nope.txt"))
    assert rc == 1
    captured = capsys.readouterr()
    assert "could not read" in captured.err.lower()


def test_cookie_header_warns_on_no_wp_login(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    hdr = "random=value; foo=bar"
    input_file = tmp_path / "hdr.txt"
    input_file.write_text(hdr)

    rc = run_import_from_cookie_header(str(input_file))
    assert rc == 0
    captured = capsys.readouterr()
    assert "wordpress_logged_in_" in captured.err
