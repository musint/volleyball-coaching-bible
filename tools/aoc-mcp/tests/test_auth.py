"""Tests for auth.py — specifically the non-interactive cookie import paths."""
import json
from pathlib import Path

from aoc_mcp.auth import run_import_from_cookie_header, run_import_from_cookie_editor_json
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


def test_cookie_editor_json_parses_valid_export(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    export = [
        {
            "domain": ".theartofcoachingvolleyball.com",
            "expirationDate": 1767225600,
            "httpOnly": True,
            "name": "wordpress_logged_in_abc",
            "path": "/",
            "sameSite": "lax",
            "secure": True,
            "session": False,
            "value": "SECRET",
        },
        {
            "domain": ".theartofcoachingvolleyball.com",
            "httpOnly": False,
            "name": "PHPSESSID",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": True,
            "value": "abc123",
        },
    ]
    input_file = tmp_path / "cookies.json"
    input_file.write_text(json.dumps(export))

    rc = run_import_from_cookie_editor_json(str(input_file))
    assert rc == 0

    saved = json.loads(config.SESSION_FILE.read_text())
    names_values = {c["name"]: c["value"] for c in saved["cookies"]}
    assert names_values["wordpress_logged_in_abc"] == "SECRET"
    assert names_values["PHPSESSID"] == "abc123"


def test_cookie_editor_json_sameSite_mapping(tmp_path, monkeypatch):
    """no_restriction -> None, lax -> Lax, strict -> Strict."""
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    export = [
        {"name": "a", "value": "1", "sameSite": "no_restriction"},
        {"name": "b", "value": "2", "sameSite": "lax"},
        {"name": "c", "value": "3", "sameSite": "strict"},
        {"name": "d", "value": "4", "sameSite": "unspecified"},
    ]
    input_file = tmp_path / "cookies.json"
    input_file.write_text(json.dumps(export))

    rc = run_import_from_cookie_editor_json(str(input_file))
    assert rc == 0

    saved = json.loads(config.SESSION_FILE.read_text())
    ss = {c["name"]: c["sameSite"] for c in saved["cookies"]}
    assert ss["a"] == "None"
    assert ss["b"] == "Lax"
    assert ss["c"] == "Strict"
    assert ss["d"] == "Lax"


def test_cookie_editor_json_session_expires_is_negative_one(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    export = [
        {"name": "persistent", "value": "x", "expirationDate": 1767225600, "session": False},
        {"name": "session", "value": "y", "session": True},
    ]
    input_file = tmp_path / "cookies.json"
    input_file.write_text(json.dumps(export))

    rc = run_import_from_cookie_editor_json(str(input_file))
    assert rc == 0

    saved = json.loads(config.SESSION_FILE.read_text())
    expires_by_name = {c["name"]: c["expires"] for c in saved["cookies"]}
    assert expires_by_name["persistent"] == 1767225600
    assert expires_by_name["session"] == -1


def test_cookie_editor_json_invalid_json_returns_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    input_file = tmp_path / "bad.json"
    input_file.write_text("{not valid json")

    rc = run_import_from_cookie_editor_json(str(input_file))
    assert rc == 1
    err = capsys.readouterr().err
    assert "invalid json" in err.lower()


def test_cookie_editor_json_non_array_returns_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "SESSION_FILE", tmp_path / "session.json")
    input_file = tmp_path / "obj.json"
    input_file.write_text('{"cookies": []}')

    rc = run_import_from_cookie_editor_json(str(input_file))
    assert rc == 1
    err = capsys.readouterr().err
    assert "array" in err.lower()
