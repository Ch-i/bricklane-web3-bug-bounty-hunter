"""Tests for harness/doctor.py — environment health checks."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from harness import doctor


def test_check_tool_missing_returns_path_none():
    with patch("harness.doctor._which", return_value=None):
        path, version, error = doctor.check_tool("missing-tool", ["--version"])
    assert path is None
    assert version is None
    assert "not on PATH" in error


def test_check_tool_returns_version_first_line():
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = "foundryup 0.1.0\nsome other line"
    proc.stderr = ""
    with patch("harness.doctor._which", return_value="/usr/bin/forge"):
        with patch("harness.doctor.subprocess.run", return_value=proc):
            path, version, error = doctor.check_tool("forge", ["--version"])
    assert path == "/usr/bin/forge"
    assert version == "foundryup 0.1.0"
    assert error is None


def test_check_tool_truncates_long_version_to_60_chars():
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = "x" * 200
    proc.stderr = ""
    with patch("harness.doctor._which", return_value="/usr/bin/x"):
        with patch("harness.doctor.subprocess.run", return_value=proc):
            _, version, _ = doctor.check_tool("x", ["--version"])
    assert len(version) == 60


def test_check_tool_falls_back_to_stderr():
    """Some tools print version to stderr instead of stdout."""
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = ""
    proc.stderr = "tool v1.2.3"
    with patch("harness.doctor._which", return_value="/usr/bin/x"):
        with patch("harness.doctor.subprocess.run", return_value=proc):
            _, version, _ = doctor.check_tool("x", ["-V"])
    assert version == "tool v1.2.3"


def test_check_tool_handles_subprocess_timeout():
    with patch("harness.doctor._which", return_value="/usr/bin/x"):
        with patch("harness.doctor.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("x", 15)):
            _, version, error = doctor.check_tool("x", ["--version"])
    assert version is None
    assert "timed out" in error


def test_check_tool_handles_generic_exception():
    with patch("harness.doctor._which", return_value="/usr/bin/x"):
        with patch("harness.doctor.subprocess.run",
                   side_effect=PermissionError("nope")):
            _, version, error = doctor.check_tool("x", ["--version"])
    assert version is None
    assert "failed to invoke" in error


def test_check_claude_auth_missing_binary():
    with patch("harness.doctor._which", return_value=None):
        ok, msg = doctor.check_claude_auth()
    assert ok is False
    assert "not on PATH" in msg


def test_check_claude_auth_happy_path():
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = '{"result": "OK"}'
    proc.stderr = ""
    with patch("harness.doctor._which", return_value="/fake/claude"):
        with patch("harness.doctor.subprocess.run", return_value=proc):
            ok, msg = doctor.check_claude_auth()
    assert ok is True
    assert "auth ok" in msg


def test_check_claude_auth_detects_error_response():
    proc = MagicMock()
    proc.returncode = 0
    proc.stdout = '{"is_error":true,"message":"auth required"}'
    proc.stderr = ""
    with patch("harness.doctor._which", return_value="/fake/claude"):
        with patch("harness.doctor.subprocess.run", return_value=proc):
            ok, msg = doctor.check_claude_auth()
    assert ok is False


def test_check_claude_auth_handles_timeout():
    with patch("harness.doctor._which", return_value="/fake/claude"):
        with patch("harness.doctor.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("claude", 30)):
            ok, msg = doctor.check_claude_auth()
    assert ok is False
    assert "timed out" in msg


def test_check_codex_auth_missing_binary():
    with patch("harness.doctor._which", return_value=None):
        ok, msg = doctor.check_codex_auth()
    assert ok is False
    assert "not on PATH" in msg


def test_check_codex_auth_missing_auth_file(tmp_path, monkeypatch):
    """codex is on PATH but ~/.codex/auth.json doesn't exist."""
    monkeypatch.setenv("HOME", str(tmp_path))
    with patch("harness.doctor._which", return_value="/fake/codex"):
        ok, msg = doctor.check_codex_auth()
    assert ok is False
    assert "auth.json" in msg
    assert "codex login" in msg


def test_check_codex_auth_present(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    codex_dir = tmp_path / ".codex"
    codex_dir.mkdir()
    (codex_dir / "auth.json").write_text("{}")
    with patch("harness.doctor._which", return_value="/fake/codex"):
        ok, msg = doctor.check_codex_auth()
    assert ok is True
    assert "auth file present" in msg


def test_check_corpus_missing_corpus_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "REPO_ROOT", tmp_path)
    ok, msg = doctor.check_corpus()
    assert ok is False
    assert "no corpus/" in msg


def test_check_corpus_empty_corpus_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "REPO_ROOT", tmp_path)
    (tmp_path / "corpus").mkdir()
    ok, msg = doctor.check_corpus()
    assert ok is False
    assert "no markdown entries" in msg


def test_check_corpus_md_exist_but_no_db(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "REPO_ROOT", tmp_path)
    (tmp_path / "corpus").mkdir()
    (tmp_path / "corpus" / "x.md").write_text("---\ntitle: x\n---\nbody")
    ok, msg = doctor.check_corpus()
    assert ok is False
    assert "corpus.db is missing" in msg


def test_check_mcp_config_present(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "REPO_ROOT", tmp_path)
    (tmp_path / ".mcp.json").write_text("{}")
    ok, msg = doctor.check_mcp_config()
    assert ok is True


def test_check_mcp_config_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "REPO_ROOT", tmp_path)
    ok, msg = doctor.check_mcp_config()
    assert ok is False
    assert "no .mcp.json" in msg


def test_check_env_vars_returns_all_three(monkeypatch):
    monkeypatch.delenv("ETHERSCAN_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("W3S_CORPUS_EXCLUDE_IDS", raising=False)
    results = doctor.check_env_vars()
    names = [r[0] for r in results]
    assert "ETHERSCAN_API_KEY" in names
    assert "ANTHROPIC_API_KEY" in names
    assert "W3S_CORPUS_EXCLUDE_IDS" in names
    # All should be unset
    assert all(not r[2] for r in results)


def test_check_env_vars_reflects_set_state(monkeypatch):
    monkeypatch.setenv("ETHERSCAN_API_KEY", "fakekey")
    results = doctor.check_env_vars()
    etherscan = next(r for r in results if r[0] == "ETHERSCAN_API_KEY")
    assert etherscan[1] == "set"
    assert etherscan[2] is True
