"""Tests for `w3s latest` — print path to latest run dir."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pytest

from harness import tui


def _args(kind: str = "any") -> argparse.Namespace:
    return argparse.Namespace(kind=kind)


def test_latest_no_audits_dir_returns_1(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setattr(tui, "REPO_ROOT", tmp_path)
    rc = tui.cmd_latest(_args())
    assert rc == 1


def test_latest_picks_newest(tmp_path: Path, monkeypatch, capsys):
    audits = tmp_path / "audits"
    audits.mkdir()
    old = audits / "vulnerable-old"
    old.mkdir()
    (old / "prep.json").write_text("{}")
    new = audits / "vulnerable-new"
    new.mkdir()
    (new / "prep.json").write_text("{}")
    # Make `new` strictly newer
    now = old.stat().st_mtime + 5
    os.utime(new, (now, now))

    monkeypatch.setattr(tui, "REPO_ROOT", tmp_path)
    rc = tui.cmd_latest(_args())
    assert rc == 0
    captured = capsys.readouterr()
    assert "vulnerable-new" in captured.out


def test_latest_filters_by_kind_scrutinize(tmp_path: Path, monkeypatch, capsys):
    audits = tmp_path / "audits"
    audits.mkdir()
    a = audits / "audit-x"
    a.mkdir()
    (a / "prep.json").write_text("{}")
    s = audits / "scrutinize-Foo-20260518"
    s.mkdir()
    monkeypatch.setattr(tui, "REPO_ROOT", tmp_path)
    rc = tui.cmd_latest(_args(kind="scrutinize"))
    assert rc == 0
    captured = capsys.readouterr()
    assert "scrutinize-Foo-20260518" in captured.out
    assert "audit-x" not in captured.out


def test_latest_filters_by_kind_audit_requires_prep_json(tmp_path: Path, monkeypatch, capsys):
    audits = tmp_path / "audits"
    audits.mkdir()
    # Has prep.json — qualifies as audit
    audit_a = audits / "audit-good"
    audit_a.mkdir()
    (audit_a / "prep.json").write_text("{}")
    # No prep.json — not an audit
    audit_b = audits / "random-other"
    audit_b.mkdir()
    # A scrutinize dir without prep.json — should also be excluded under --kind=audit
    scrut = audits / "scrutinize-bar"
    scrut.mkdir()
    monkeypatch.setattr(tui, "REPO_ROOT", tmp_path)
    rc = tui.cmd_latest(_args(kind="audit"))
    assert rc == 0
    captured = capsys.readouterr()
    assert "audit-good" in captured.out


def test_latest_no_matching_kind_returns_1(tmp_path: Path, monkeypatch):
    audits = tmp_path / "audits"
    audits.mkdir()
    (audits / "audit-x").mkdir()
    (audits / "audit-x" / "prep.json").write_text("{}")
    monkeypatch.setattr(tui, "REPO_ROOT", tmp_path)
    rc = tui.cmd_latest(_args(kind="scrutinize"))
    assert rc == 1
