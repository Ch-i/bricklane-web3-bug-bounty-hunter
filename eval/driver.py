"""Drive a single audit non-interactively via `claude -p --agent web3-auditor`.

Used by ``eval/run.py`` to run the harness over a benchmark entry without
a human in the loop. The same code path can later be reused for batch
audits of multiple targets.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from harness.audit_runner import resolve_target, slugify
from harness.corpus import REPO_ROOT

JSON_FENCE = re.compile(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", re.DOTALL)


@dataclass
class DriveResult:
    run_dir: Path
    findings_path: Path
    raw_output: str
    parse_error: str | None


def _agent_brief(prep_meta: dict, exclude_ids: list[str]) -> str:
    """User message handed to the web3-auditor subagent.

    The agent's system prompt comes from .claude/agents/web3-auditor.md;
    this is just the per-target context.
    """
    target_files = "\n".join(f"- {f}" for f in prep_meta["target_files"])
    exclude_note = (
        f"\nEVAL MODE: the following corpus entries have been filtered out "
        f"of search_corpus results for this run: {exclude_ids}. They are the "
        f"post-mortem of the bug you are evaluating, and excluding them is "
        f"how we test whether the harness can find the bug *without* reading "
        f"the answer. Do not let this change how you reason; just be aware "
        f"that some grounding entries you might expect will not appear.\n"
        if exclude_ids
        else ""
    )

    return (
        f"You are auditing the following target.\n\n"
        f"TARGET: {prep_meta['target']}\n"
        f"TARGET KIND: {prep_meta['target_kind']}\n"
        f"RUN DIR: {prep_meta['run_dir']}\n\n"
        f"SOURCE FILES TO AUDIT (read each one):\n{target_files}\n\n"
        f"STATIC ANALYZER RESULTS: {prep_meta['static_tools_path']}\n"
        f"(read this file with Read to see Slither / Aderyn / Foundry output)\n"
        f"{exclude_note}\n"
        f"Follow the workflow in your system prompt. Search the corpus to "
        f"ground your findings. Write the final JSON findings list to "
        f"{prep_meta['run_dir']}/auditor-output.json -- do NOT just paste it "
        f"into chat. Set 'discovered_by': 'claude' on every finding.\n"
    )


def drive_audit(
    target: str | Path,
    *,
    scope: str | Path | None = None,
    exclude_ids: list[str] | None = None,
    model: str = "opus",
    timeout_seconds: int = 1800,
    deep: bool = False,
) -> DriveResult:
    """End-to-end: prep -> claude -p subagent -> finalize. Returns the run dir.

    Caller is responsible for running ``eval/scoring.score_entry`` on the
    resulting ``findings.json``.
    """
    exclude_ids = exclude_ids or []
    claude_bin = shutil.which("claude")
    if not claude_bin:
        raise FileNotFoundError("claude CLI not on PATH")

    # --- prep -----------------------------------------------------------
    prep_cmd = [
        "uv",
        "run",
        "--quiet",
        "python",
        "-m",
        "harness.audit_runner",
        "prep",
        str(target),
    ]
    if scope:
        prep_cmd += ["--scope", str(scope)]
    if deep:
        prep_cmd += ["--deep"]
    prep = subprocess.run(
        prep_cmd, capture_output=True, text=True, cwd=str(REPO_ROOT), check=True
    )
    prep_meta = json.loads(prep.stdout.strip().splitlines()[-1])
    run_dir = Path(prep_meta["run_dir"])

    # --- subagent invocation --------------------------------------------
    env = os.environ.copy()
    if exclude_ids:
        env["W3S_CORPUS_EXCLUDE_IDS"] = ",".join(exclude_ids)

    brief = _agent_brief(prep_meta, exclude_ids)

    # `--agent web3-auditor` loads .claude/agents/web3-auditor.md (system
    # prompt + tool allowlist). `--dangerously-skip-permissions` avoids
    # the interactive permission prompts that would otherwise hang a
    # headless run. `--output-format json` gives a parseable wrapper
    # around the assistant's final message.
    # Build the command, dedup --add-dir entries.
    add_dirs = {str(REPO_ROOT.resolve())}
    target_resolved = Path(prep_meta["target"]).resolve()
    if REPO_ROOT.resolve() not in target_resolved.parents and target_resolved != REPO_ROOT.resolve():
        add_dirs.add(str(target_resolved))

    claude_cmd = [claude_bin, "-p", "--agent", "web3-auditor", "--model", model]
    for d in sorted(add_dirs):
        claude_cmd += ["--add-dir", d]
    claude_cmd += ["--output-format", "json", "--dangerously-skip-permissions", brief]

    claude_run = subprocess.run(
        claude_cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        timeout=timeout_seconds,
        check=False,
    )

    (run_dir / "claude-stdout.log").write_text(claude_run.stdout)
    (run_dir / "claude-stderr.log").write_text(claude_run.stderr)

    # Prefer the file the agent wrote itself; fall back to parsing stdout.
    findings_path = run_dir / "auditor-output.json"
    parse_error = None
    if not findings_path.exists():
        # Try to extract JSON from the assistant's final message in the
        # claude --output-format json wrapper.
        try:
            wrapper = json.loads(claude_run.stdout)
            assistant_msg = wrapper.get("result", "") if isinstance(wrapper, dict) else ""
        except json.JSONDecodeError:
            assistant_msg = claude_run.stdout
        match = JSON_FENCE.search(assistant_msg)
        if match:
            try:
                payload = json.loads(match.group(1))
                findings_path.write_text(json.dumps(payload, indent=2))
            except json.JSONDecodeError as e:
                parse_error = f"could not decode fenced JSON: {e}"
        else:
            parse_error = (
                f"no auditor-output.json was written, and no fenced JSON "
                f"block found in claude stdout (rc={claude_run.returncode}, "
                f"stderr={claude_run.stderr[-500:]!r})"
            )

    # --- finalize -------------------------------------------------------
    if findings_path.exists():
        fin = subprocess.run(
            [
                "uv",
                "run",
                "--quiet",
                "python",
                "-m",
                "harness.audit_runner",
                "finalize",
                str(run_dir),
                "--findings",
                str(findings_path),
            ],
            cwd=str(REPO_ROOT),
            check=False,
            capture_output=True,
            text=True,
        )
        (run_dir / "finalize-stdout.log").write_text(fin.stdout)
        (run_dir / "finalize-stderr.log").write_text(fin.stderr)
        if fin.returncode != 0 and not parse_error:
            parse_error = (
                f"finalize exited {fin.returncode}: "
                f"{(fin.stderr or fin.stdout)[-500:]}"
            )

    return DriveResult(
        run_dir=run_dir,
        findings_path=findings_path,
        raw_output=claude_run.stdout,
        parse_error=parse_error,
    )
