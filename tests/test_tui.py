"""Tests for harness.tui — render helpers (no subprocess / no live mode)."""

from __future__ import annotations

import json
from pathlib import Path

from harness.tui import (
    _coverage_pct,
    _list_run_dirs,
    _load_findings,
    _summary_row,
    render_findings_table,
    render_list,
    render_show,
    render_status,
)


def _make_run(tmp_path: Path, name: str, *, findings: list[dict] = None, static: list[dict] = None):
    run = tmp_path / name
    run.mkdir(parents=True, exist_ok=True)
    (run / "prep.json").write_text(
        json.dumps(
            {
                "run_dir": str(run),
                "target": "tests/fixtures/Vulnerable.sol",
                "target_kind": "single-file",
                "timestamp": "2026-05-15T13:00:00+00:00",
                "static_tools_path": str(run / "static-tools.json"),
                "target_files": ["tests/fixtures/Vulnerable.sol"],
                "corpus_snapshot": "abc123",
            }
        )
    )
    (run / "static-tools.json").write_text(json.dumps(static or []))
    if findings is not None:
        (run / "findings.json").write_text(json.dumps(findings))
    return run


def test_list_run_dirs_returns_most_recent_first(tmp_path):
    older = _make_run(tmp_path, "older")
    newer = _make_run(tmp_path, "newer")
    # Force mtimes
    import os
    os.utime(older, (1000, 1000))
    os.utime(newer, (2000, 2000))
    runs = _list_run_dirs(tmp_path)
    assert runs == [newer, older]


def test_summary_row_aggregates_severities_and_pocs(tmp_path):
    run = _make_run(
        tmp_path,
        "run1",
        findings=[
            {"severity": "Critical", "poc_status": "reproduced", "title": "a"},
            {"severity": "High", "poc_status": "unconfirmed", "title": "b"},
            {"severity": "Low", "poc_status": "not-applicable", "title": "c"},
        ],
    )
    s = _summary_row(run)
    assert s["n_findings"] == 3
    assert s["by_sev"]["Critical"] == 1
    assert s["by_sev"]["High"] == 1
    assert s["by_poc"]["reproduced"] == 1


def test_coverage_pct_extracts_from_foundry_static(tmp_path):
    run = _make_run(
        tmp_path,
        "with_cov",
        static=[
            {
                "tool": "foundry",
                "succeeded": True,
                "output": {
                    "build_ok": True,
                    "coverage": {
                        "status": "ok",
                        "function_pct": 42.5,
                        "line_pct": 67.3,
                    },
                },
            }
        ],
    )
    static = json.loads((run / "static-tools.json").read_text())
    txt = _coverage_pct(static)
    assert "42" in txt
    assert "67" in txt


def test_coverage_pct_returns_dash_when_unavailable(tmp_path):
    run = _make_run(
        tmp_path,
        "no_cov",
        static=[{"tool": "foundry", "succeeded": True, "output": {"build_ok": False}}],
    )
    static = json.loads((run / "static-tools.json").read_text())
    assert _coverage_pct(static) == "—"


def test_renderers_dont_crash_on_minimal_run(tmp_path):
    run = _make_run(tmp_path, "minimal", findings=[], static=[])
    # All renderers should produce something without raising.
    assert render_list(tmp_path) is not None
    assert render_show(run) is not None
    assert render_findings_table(run) is not None
    assert render_status(run) is not None
