"""Tests for harness/codex_audit.py — focusing on build_user_message + output parsing."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness import codex_audit


def _prep(tmp_path: Path) -> dict:
    run = tmp_path / "run"
    run.mkdir()
    return {
        "target": "src/Vault.sol",
        "target_kind": "single-file",
        "target_files": ["src/Vault.sol", "src/Library.sol"],
        "run_dir": str(run),
        "static_tools_path": str(run / "static-tools.json"),
    }


def test_build_user_message_includes_all_target_files():
    prep = {"target": "x", "target_kind": "single-file",
            "target_files": ["a.sol", "b.sol", "c.sol"],
            "run_dir": "/tmp/run", "static_tools_path": "/tmp/st.json"}
    msg = codex_audit.build_user_message(prep, exclude_ids=[])
    assert "a.sol" in msg and "b.sol" in msg and "c.sol" in msg
    assert "discovered_by" in msg
    assert "codex" in msg.lower()


def test_build_user_message_adds_eval_mode_note_when_excludes_set():
    prep = {"target": "x", "target_kind": "single-file",
            "target_files": ["a.sol"], "run_dir": "/x", "static_tools_path": "/x"}
    msg = codex_audit.build_user_message(prep, exclude_ids=["swc-107", "synthesis-x"])
    assert "EVAL MODE" in msg
    assert "swc-107" in msg
    assert "synthesis-x" in msg


def test_build_user_message_no_eval_note_when_excludes_empty():
    prep = {"target": "x", "target_kind": "single-file",
            "target_files": ["a.sol"], "run_dir": "/x", "static_tools_path": "/x"}
    msg = codex_audit.build_user_message(prep, exclude_ids=[])
    assert "EVAL MODE" not in msg


def test_run_codex_raises_without_codex_binary(tmp_path, monkeypatch):
    prep = _prep(tmp_path)
    # shutil.which returns None → falls back to npm-global path → doesn't exist
    monkeypatch.setenv("HOME", str(tmp_path))  # so ~/.npm-global/bin/codex doesn't exist
    with patch("harness.codex_audit.shutil.which", return_value=None):
        with pytest.raises(FileNotFoundError, match="codex CLI"):
            codex_audit.run_codex_audit(prep)


def test_run_codex_returns_timeout_result(tmp_path):
    prep = _prep(tmp_path)
    real_path = str(Path(__import__("sys").executable))
    with patch("harness.codex_audit.shutil.which", return_value=real_path):
        with patch("harness.codex_audit.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("codex", 60)):
            result = codex_audit.run_codex_audit(prep, timeout_seconds=60)
    assert result.error is not None
    assert "timed out" in result.error


def test_run_codex_parses_well_formed_output(tmp_path):
    prep = _prep(tmp_path)
    run_dir = Path(prep["run_dir"])

    findings_payload = {
        "findings": [
            {
                "title": "Reentrancy",
                "severity": "High",
                "location": [{"file": "Vault.sol", "line_start": 12}],
                "description": "d", "impact": "i", "recommendation": "r",
                "citations": ["swc-107"], "novel": False,
                "confidence": "high", "discovered_by": "codex",
            }
        ]
    }

    def fake_run(cmd, **kw):
        # Mock side-effect: write the last-message file
        last_msg = run_dir / "codex-last-message.json"
        last_msg.write_text(json.dumps(findings_payload))
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = "codex ok"
        proc.stderr = ""
        return proc

    # The codex_audit module checks Path(codex_bin).exists() — so we need a
    # real path that exists. Use the python binary as a stand-in.
    real_path = str(Path(__import__("sys").executable))
    with patch("harness.codex_audit.shutil.which", return_value=real_path):
        with patch("harness.codex_audit.subprocess.run", side_effect=fake_run):
            result = codex_audit.run_codex_audit(prep)

    assert result.error is None
    assert len(result.findings) == 1
    assert result.findings[0].title == "Reentrancy"
    assert result.findings[0].discovered_by == "codex"
    assert (run_dir / "codex-output.json").exists()


def test_run_codex_skips_invalid_findings_but_keeps_valid(tmp_path):
    """One bad finding shouldn't break the whole run."""
    prep = _prep(tmp_path)
    run_dir = Path(prep["run_dir"])

    findings_payload = {
        "findings": [
            {  # valid
                "title": "Good", "severity": "High",
                "location": [{"file": "x.sol", "line_start": 1}],
                "description": "d", "impact": "i", "recommendation": "r",
                "citations": ["swc-107"], "novel": False,
                "confidence": "high", "discovered_by": "codex",
            },
            {  # invalid — missing required fields
                "title": "Bad",
            },
        ]
    }

    def fake_run(cmd, **kw):
        (run_dir / "codex-last-message.json").write_text(json.dumps(findings_payload))
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = ""
        proc.stderr = ""
        return proc

    # The codex_audit module checks Path(codex_bin).exists() — so we need a
    # real path that exists. Use the python binary as a stand-in.
    real_path = str(Path(__import__("sys").executable))
    with patch("harness.codex_audit.shutil.which", return_value=real_path):
        with patch("harness.codex_audit.subprocess.run", side_effect=fake_run):
            result = codex_audit.run_codex_audit(prep)

    # 1 valid finding kept
    assert len(result.findings) == 1
    assert result.findings[0].title == "Good"
    # Error string mentions the invalid one
    assert result.error is not None
    assert "invalid" in result.error


def test_run_codex_handles_unparseable_output(tmp_path):
    prep = _prep(tmp_path)
    run_dir = Path(prep["run_dir"])

    def fake_run(cmd, **kw):
        (run_dir / "codex-last-message.json").write_text("not valid json {{{")
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = ""
        proc.stderr = ""
        return proc

    # The codex_audit module checks Path(codex_bin).exists() — so we need a
    # real path that exists. Use the python binary as a stand-in.
    real_path = str(Path(__import__("sys").executable))
    with patch("harness.codex_audit.shutil.which", return_value=real_path):
        with patch("harness.codex_audit.subprocess.run", side_effect=fake_run):
            result = codex_audit.run_codex_audit(prep)

    assert result.error is not None
    assert "not valid JSON" in result.error
    assert result.findings == []


def test_run_codex_passes_exclude_ids_via_env(tmp_path):
    prep = _prep(tmp_path)
    run_dir = Path(prep["run_dir"])
    captured_env: dict = {}

    def fake_run(cmd, **kw):
        captured_env.update(kw.get("env") or {})
        (run_dir / "codex-last-message.json").write_text(json.dumps({"findings": []}))
        proc = MagicMock()
        proc.returncode = 0
        proc.stdout = ""
        proc.stderr = ""
        return proc

    real_path = str(Path(__import__("sys").executable))
    with patch("harness.codex_audit.shutil.which", return_value=real_path):
        with patch("harness.codex_audit.subprocess.run", side_effect=fake_run):
            codex_audit.run_codex_audit(prep, exclude_ids=["swc-107", "synthesis-foo"])

    assert captured_env.get("W3S_CORPUS_EXCLUDE_IDS") == "swc-107,synthesis-foo"
