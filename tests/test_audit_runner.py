"""End-to-end test of the audit runner: prep -> synthesize findings -> finalize."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "Vulnerable.sol"


def test_prep_and_finalize_pipeline(monkeypatch, tmp_path):
    """prep runs slither + writes prep.json; finalize validates citations,
    renders report.md, and writes rejected.md for the invalid finding."""

    # Run prep in a clean working directory to isolate crytic-export side effects.
    work = tmp_path
    shutil.copytree(REPO / "tests" / "fixtures", work / "fixtures")
    target = work / "fixtures" / "Vulnerable.sol"

    prep = subprocess.run(
        [sys.executable, "-m", "harness.audit_runner", "prep", str(target)],
        capture_output=True,
        text=True,
        cwd=str(REPO),
        check=True,
    )
    # Last stdout line is the JSON meta blob.
    meta = json.loads(prep.stdout.strip().splitlines()[-1])
    run_dir = Path(meta["run_dir"])
    assert run_dir.exists()
    assert (run_dir / "prep.json").exists()
    assert (run_dir / "static-tools.json").exists()

    # Build a findings file: one cited (valid), one novel, one invalid citation.
    findings = {
        "findings": [
            {
                "title": "Reentrancy in withdraw",
                "severity": "High",
                "location": [{"file": "Vulnerable.sol", "line_start": 12, "line_end": 17}],
                "description": "...",
                "impact": "...",
                "recommendation": "...",
                "citations": ["swc-107"],
                "novel": False,
                "confidence": "high",
                "discovered_by": "claude",
            },
            {
                "title": "Suspicious storage pattern (no clear precedent)",
                "severity": "Low",
                "location": [{"file": "Vulnerable.sol", "line_start": 1}],
                "description": "...",
                "impact": "...",
                "recommendation": "...",
                "citations": [],
                "novel": True,
                "confidence": "low",
                "discovered_by": "claude",
            },
            {
                "title": "Bogus finding with invalid citation",
                "severity": "Low",
                "location": [{"file": "Vulnerable.sol", "line_start": 1}],
                "description": "...",
                "impact": "...",
                "recommendation": "...",
                "citations": ["swc-99999"],
                "novel": False,
                "confidence": "low",
                "discovered_by": "claude",
            },
        ]
    }
    findings_path = run_dir / "auditor-output.json"
    findings_path.write_text(json.dumps(findings))

    fin = subprocess.run(
        [
            sys.executable,
            "-m",
            "harness.audit_runner",
            "finalize",
            str(run_dir),
            "--findings",
            str(findings_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO),
        check=True,
    )
    summary = json.loads(fin.stdout.strip().splitlines()[-1])
    assert summary["findings_accepted"] == 2
    assert summary["findings_rejected"] == 1
    assert summary["parse_errors"] == 0

    report = (run_dir / "report.md").read_text()
    assert "[High] Reentrancy in withdraw" in report
    assert "[novel]" in report
    assert "swc-99999" not in report  # rejected; should not appear in report

    rejected = (run_dir / "rejected.md").read_text()
    assert "swc-99999" in rejected

    # Cleanup audit run dir created in repo
    shutil.rmtree(run_dir, ignore_errors=True)
