"""Post-pass that turns deep-dive `poc_sketch` strings into runnable Foundry tests.

Deep-dive emits structured candidate_vulnerabilities, each with a `poc_sketch`
field that's free-form pseudocode. This module promotes High/Critical
candidates into the existing `harness.poc.foundry_poc` shape and runs
`forge test`, so the deep-dive report ends with reproducibility status per
candidate — the same AFL-crash-file analog the audit pipeline already has.

Cost: 1 Opus call per High/Critical candidate to convert the sketch into
structured foundry_poc fields, then 1 forge test execution. ~5-15 messages
total per deep-dive run depending on candidate count.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from harness.corpus import REPO_ROOT
from harness.poc import attempt_all as attempt_pocs
from harness.schema import Finding, FindingLocation, FoundryPoc

CONVERT_SYSTEM = """\
You are converting a free-form Solidity PoC sketch into a STRUCTURED
foundry_poc JSON object that a scaffolder can wrap into a runnable
forge test file.

Output exactly this JSON (no markdown, no preamble):

{
  "test_name": "test_<descriptive_camelCase>",
  "setup": "<Solidity for the test's setUp() body — deploy, deal, approve, etc>",
  "exploit": "<Solidity for the test function's body — the attack sequence>",
  "assertion": "<Solidity assertion that PASSES when the bug is reproduced>",
  "imports": ["<sol path>", "<sol path>"],
  "notes": "<caveats; null is fine>"
}

Conventions:
  * test_name MUST start with `test_` and be a valid identifier.
  * setUp deploys the target, helper contracts, funds attacker/victim accounts.
  * exploit is the attacker's call sequence.
  * assertion uses assertGt / assertEq / vm.expectRevert. The assertion
    PASSES if the bug is reproduced — a passing test = bug exists.
  * imports must be Solidity-importable relative paths (e.g.
    "../../src/Vault.sol"). The generated test will live at
    <target>/test/__web3sentinel_pocs__/<contract>.t.sol.
  * If the sketch is too vague to make compilable, set fields to your
    best guess but flag in notes "PoC sketch was incomplete; manual
    completion required". Don't refuse.
  * Helper contracts (e.g. an Attacker) can be declared inline INSIDE
    the setUp body or BEFORE the test contract — both are fine; the
    scaffolder will pass through the Solidity unchanged.

Output ONLY the JSON object.
"""


def _claude_bin() -> str | None:
    return shutil.which("claude")


def _convert_sketch(
    candidate: dict,
    fn_id: str,
    *,
    model: str = "opus",
    timeout_seconds: int = 300,
) -> FoundryPoc | None:
    sketch = candidate.get("poc_sketch") or ""
    if not sketch or len(sketch.strip()) < 20:
        return None
    cl = _claude_bin()
    if not cl:
        return None
    brief = (
        f"# Candidate vulnerability to convert\n\n"
        f"**Function:** {fn_id}\n"
        f"**Title:** {candidate.get('title', '')}\n"
        f"**Severity:** {candidate.get('severity', '?')}\n"
        f"**Precondition:** {candidate.get('precondition', '?')}\n"
        f"**Impact:** {candidate.get('impact', '?')}\n\n"
        f"## PoC sketch (free-form):\n```\n{sketch}\n```\n\n"
        f"Convert into the foundry_poc JSON shape per your system prompt."
    )
    try:
        proc = subprocess.run(
            [
                cl, "-p", "--model", model,
                "--system-prompt", CONVERT_SYSTEM,
                "--dangerously-skip-permissions",
                "--output-format", "json",
                brief,
            ],
            capture_output=True, text=True, timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    except Exception:  # noqa: BLE001
        return None

    if proc.returncode != 0:
        return None
    try:
        wrapper = json.loads(proc.stdout)
        text_out = wrapper.get("result", "") if isinstance(wrapper, dict) else proc.stdout
    except json.JSONDecodeError:
        text_out = proc.stdout
    m = re.search(r"\{.*\}", text_out, re.DOTALL)
    if not m:
        return None
    try:
        payload = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    try:
        return FoundryPoc.model_validate(payload)
    except Exception:  # noqa: BLE001
        return None


def materialize_for_run(
    deep_dive_run_dir: Path,
    target_root: Path,
    *,
    min_severity: Literal["Critical", "High", "Medium"] = "High",
    model: str = "opus",
    progress_callback=None,
) -> Path:
    """Read per-function.jsonl, materialize PoCs for promising candidates,
    run forge tests, write the verified-findings file.

    Returns the path to the new `materialized-findings.json`.
    """
    pf_path = deep_dive_run_dir / "per-function.jsonl"
    if not pf_path.exists():
        raise FileNotFoundError(f"no per-function.jsonl in {deep_dive_run_dir}")

    sev_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4, "Informational": 4}
    min_rank = sev_rank.get(min_severity, 1)

    promoted: list[Finding] = []
    candidate_count = 0
    for line in pf_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            fn = json.loads(line)
        except json.JSONDecodeError:
            continue
        fn_id = fn.get("function_id", "?")
        for i, vuln in enumerate(fn.get("candidate_vulnerabilities") or []):
            sev = vuln.get("severity")
            if sev_rank.get(sev, 99) > min_rank:
                continue
            if not vuln.get("poc_sketch"):
                continue
            candidate_count += 1
            if progress_callback:
                progress_callback("convert", candidate_count, "?", f"converting: {fn_id} :: {vuln.get('title')}")

            foundry_poc = _convert_sketch(vuln, fn_id, model=model)
            if foundry_poc is None:
                continue

            # Build a Finding-shaped object so attempt_all_pocs can scaffold it
            file_path = fn_id.split("::")[0]
            try:
                finding = Finding(
                    title=str(vuln.get("title", "?"))[:200],
                    severity=sev,
                    location=[FindingLocation(file=file_path, line_start=1)],
                    description=str(vuln.get("description") or vuln.get("title", "?"))[:2000],
                    impact=str(vuln.get("impact", "?"))[:1500],
                    recommendation="(see deep-dive report)",
                    citations=[],  # deep-dive doesn't cite individual entries
                    novel=True,    # deep-dive findings are pre-corpus by definition
                    confidence={"high": "high", "medium": "medium", "low": "low", "speculative": "low"}.get(
                        vuln.get("confidence", "medium"), "medium",
                    ),
                    discovered_by="claude",
                    foundry_poc=foundry_poc,
                )
                promoted.append(finding)
            except Exception:  # noqa: BLE001
                continue

    if not promoted:
        # Write an empty manifest so callers can detect "nothing materialized"
        out_path = deep_dive_run_dir / "materialized-findings.json"
        out_path.write_text(json.dumps([]))
        return out_path

    # Try to find a Foundry root above target_root
    project_root = target_root
    if not (project_root / "foundry.toml").exists():
        for parent in target_root.parents:
            if (parent / "foundry.toml").exists():
                project_root = parent
                break

    if progress_callback:
        progress_callback("forge", 0, len(promoted), f"running forge test on {len(promoted)} PoCs")

    attempt_pocs(
        promoted,
        run_dir=deep_dive_run_dir,
        project_root=project_root,
        progress=lambda i, total, f, phase: (
            progress_callback("forge", i + 1, total, f"{phase}: {f.title[:60]}") if progress_callback else None
        ),
    )

    out_path = deep_dive_run_dir / "materialized-findings.json"
    out_path.write_text(json.dumps([f.model_dump() for f in promoted], indent=2))

    return out_path


def render_materialization_summary(materialized_path: Path) -> str:
    if not materialized_path.exists():
        return "(no materialized findings)"
    data = json.loads(materialized_path.read_text())
    if not data:
        return "(no candidates above threshold or no PoC sketches)"
    by_status: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for f in data:
        by_status[f.get("poc_status", "not-attempted")] = by_status.get(f.get("poc_status", "not-attempted"), 0) + 1
        by_sev[f.get("severity", "?")] = by_sev.get(f.get("severity", "?"), 0) + 1
    return (
        f"PoCs materialized: {len(data)}\n"
        f"  by severity: {', '.join(f'{k}={v}' for k,v in by_sev.items())}\n"
        f"  by status: {', '.join(f'{k}={v}' for k,v in by_status.items())}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", help="A deep-dive run dir containing per-function.jsonl.")
    parser.add_argument("--target", required=True, help="Source root of the analyzed target.")
    parser.add_argument("--min-severity", default="High", choices=["Critical", "High", "Medium"])
    parser.add_argument("--model", default="opus")
    args = parser.parse_args(argv)

    rd = Path(args.run_dir).expanduser().resolve()
    tr = Path(args.target).expanduser().resolve()

    def progress(phase, idx, total, msg):
        print(f"[{phase} {idx}/{total}] {msg}")

    out_path = materialize_for_run(
        rd, tr,
        min_severity=args.min_severity,
        model=args.model,
        progress_callback=progress,
    )
    print(f"\nMaterialized → {out_path}")
    print(render_materialization_summary(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
