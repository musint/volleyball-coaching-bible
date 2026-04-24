"""Tests for tools/lint.py. Run: python -m pytest tools/test_lint.py -v"""
import os
import tempfile
import shutil
import subprocess
from pathlib import Path

LINT = Path(__file__).parent / "lint.py"

def _run(wiki_root, extra_args=None):
    args = ["python", str(LINT), "--wiki", str(wiki_root)]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def _scaffold(tmpdir, pages):
    """pages is {relative_path: content}"""
    for rel, content in pages.items():
        p = Path(tmpdir) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

def test_broken_wikilink_detected(tmp_path):
    _scaffold(tmp_path, {
        "wiki/hub.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# Hub\nLink to [[missing-page]].\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "missing-page" in out
    assert "broken wikilink" in out.lower()

def test_no_broken_wikilinks_passes(tmp_path):
    _scaffold(tmp_path, {
        "wiki/a.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# A\nLinks to [[b]].\n",
        "wiki/b.md": "---\ntype: hub\narea: y\nsubtopics: []\n---\n# B\n",
    })
    code, _, _ = _run(tmp_path)
    assert code == 0

def test_drill_must_have_source_and_technique(tmp_path):
    _scaffold(tmp_path, {
        "wiki/drills/bad.md": "---\ntype: drill\nname: Bad\nprimary-skill: passing\nphase: skill\nteam-size-min: 2\nteam-size-max: 4\nduration-min: 5\nlevels: [14u]\nequipment: []\ntechniques: []\nsources: []\n---\n# Bad\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "drill" in out.lower() and ("source" in out.lower() or "technique" in out.lower())

def test_coach_must_have_school_and_source(tmp_path):
    _scaffold(tmp_path, {
        "wiki/coaches/nobody.md": "---\ntype: coach\nname: Nobody\ncountry: USA\nera: modern\nroles: []\nschools: []\nsources: []\n---\n# Nobody\n",
    })
    code, out, _ = _run(tmp_path)
    assert code != 0
    assert "coach" in out.lower()

def test_report_file_written(tmp_path):
    _scaffold(tmp_path, {
        "wiki/a.md": "---\ntype: hub\narea: x\nsubtopics: []\n---\n# A\n",
    })
    _run(tmp_path, ["--report", str(tmp_path / "report.md")])
    assert (tmp_path / "report.md").exists()
