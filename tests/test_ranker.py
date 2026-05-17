"""Unit tests for harness.ranker — output parsing only (no claude calls)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from harness.ranker import FileRank, rank_file


def _fake_proc(text: str, rc: int = 0):
    proc = MagicMock()
    proc.returncode = rc
    proc.stdout = json.dumps({"result": text})
    proc.stderr = ""
    return proc


def test_rank_file_parses_well_formed_output(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo { function f() public {} }")
    with patch("harness.ranker.subprocess.run", return_value=_fake_proc("RANK: 4 :: Funds-touching entry point with custom math")):
        r = rank_file(src)
    assert r.rank == 4
    assert "Funds-touching" in r.rationale
    assert r.error is None


def test_rank_file_clamps_out_of_range(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    with patch("harness.ranker.subprocess.run", return_value=_fake_proc("RANK: 9 :: too high")):
        r = rank_file(src)
    assert r.rank == 5  # clamped to upper bound


def test_rank_file_returns_zero_on_unparseable_output(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    with patch("harness.ranker.subprocess.run", return_value=_fake_proc("I think this file is fine")):
        r = rank_file(src)
    assert r.rank == 0
    assert "unparseable" in r.rationale


def test_rank_file_handles_nonzero_rc(tmp_path):
    src = tmp_path / "Foo.sol"
    src.write_text("contract Foo {}")
    with patch("harness.ranker.subprocess.run", return_value=_fake_proc("", rc=1)):
        r = rank_file(src)
    assert r.rank == 0
    assert "rc != 0" in r.rationale


def test_rank_file_truncates_large_input(tmp_path, monkeypatch):
    # Build a file >600 lines so the trimming branch runs.
    big = tmp_path / "Big.sol"
    big.write_text("\n".join([f"// line {i}" for i in range(800)]))

    captured = {}
    def _spy_run(*args, **kwargs):
        captured["argv"] = args[0] if args else kwargs.get("args")
        return _fake_proc("RANK: 3 :: ok")

    with patch("harness.ranker.subprocess.run", side_effect=_spy_run):
        r = rank_file(big)
    assert r.rank == 3
    # The user message includes the elision marker for trimmed files.
    user_msg = captured["argv"][-1]
    assert "middle elided" in user_msg


def test_rank_project_skips_lib_and_test(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "Foo.sol").write_text("contract Foo {}")
    (tmp_path / "lib" / "openzeppelin").mkdir(parents=True)
    (tmp_path / "lib" / "openzeppelin" / "Owned.sol").write_text("contract Owned {}")
    (tmp_path / "test").mkdir()
    (tmp_path / "test" / "FooTest.sol").write_text("contract T {}")

    from harness.ranker import rank_project
    with patch("harness.ranker.rank_file", return_value=FileRank("x", 3, "ok", 1)):
        ranks = rank_project(tmp_path)
    # Only src/Foo.sol should have been ranked; lib + test are skipped.
    assert len(ranks) == 1
