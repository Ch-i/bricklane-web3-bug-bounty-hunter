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
    # We don't expect aderyn to be installed in CI; just verify the wrapper
    # returns the documented failure mode rather than raising.
    cfg = StaticToolsConfig(target=tmp_path, target_kind="directory")
    result = run_aderyn(cfg)
    if shutil.which("aderyn"):
        # If it's actually installed, we accept either succeed or fail with a real error.
        assert result.tool == "aderyn"
    else:
        assert not result.succeeded
        assert "not on PATH" in (result.error or "")


def test_foundry_reports_non_foundry_target_gracefully(tmp_path):
    cfg = StaticToolsConfig(target=tmp_path, target_kind="directory")
    result = run_foundry(cfg)
    assert not result.succeeded
    # Either forge missing or no foundry.toml — both are acceptable failure modes.
    assert result.error is not None
