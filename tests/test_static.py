"""Static analyzer smoke tests against the bundled vulnerable contract."""

from __future__ import annotations

import shutil
from pathlib import Path

from harness.static import StaticToolsConfig, run_aderyn, run_foundry, run_slither

FIXTURE = Path(__file__).parent / "fixtures" / "Vulnerable.sol"


def test_slither_detects_planted_bugs():
    cfg = StaticToolsConfig(target=FIXTURE.resolve(), target_kind="single-file")
    result = run_slither(cfg)
    assert result.succeeded, f"slither failed: {result.error}"
    checks = {d["check"] for d in result.output["detectors"]}
    assert "reentrancy-eth" in checks
    assert "tx-origin" in checks
    assert "suicidal" in checks


def test_aderyn_reports_missing_gracefully(tmp_path):
    # Verify the wrapper returns documented failure modes rather than raising.
    # Two valid outcomes depending on whether aderyn is installed:
    #   not installed -> "not on PATH"
    #   installed     -> runs against the empty dir, fails to produce JSON,
    #                    reports "did not produce JSON" or similar
    from harness.static import _which
    cfg = StaticToolsConfig(target=tmp_path, target_kind="directory")
    result = run_aderyn(cfg)
    assert result.tool == "aderyn"
    if _which("aderyn"):
        # Installed: should fail gracefully on an empty dir (no .sol files).
        assert not result.succeeded
        assert result.error  # something descriptive, not None
    else:
        assert not result.succeeded
        assert "not on PATH" in (result.error or "")


def test_foundry_reports_non_foundry_target_gracefully(tmp_path):
    cfg = StaticToolsConfig(target=tmp_path, target_kind="directory")
    result = run_foundry(cfg)
    assert not result.succeeded
    # Either forge missing or no foundry.toml — both are acceptable failure modes.
    assert result.error is not None
