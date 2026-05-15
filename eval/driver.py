"""Drive an audit non-interactively.

Two modes:
  * Single-model: spawn the Claude auditor only (cheap, fast).
  * Multi-model:  spawn Claude + Codex auditors in parallel, then a Claude
                  reconciler to merge. Slower, costs more, but surfaces
                  bugs one model missed and disagreements worth human review.

Used by ``eval/run.py`` to run the harness over a benchmark entry without
a human in the loop. The /audit skill drives the same path interactively.
"""

from __future__ import annotations

import concurrent.futures
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from harness.codex_audit import run_codex_audit
from harness.corpus import REPO_ROOT

JSON_FENCE = re.compile(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", re.DOTALL)


@dataclass
class DriveResult:
    run_dir: Path
    findings_path: Path        # the file `finalize` consumed
    raw_output: str            # last orchestrating CLI's stdout (for debug)
    parse_error: str | None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _auditor_brief(prep_meta: dict, exclude_ids: list[str]) -> str:
    """User message handed to the Claude web3-auditor subagent."""
    target_files = "\n".join(f"- {f}" for f in prep_meta["target_files"])
    exclude_note = (
        f"\nEVAL MODE: the following corpus entries have been filtered out "
        f"of search_corpus results for this run: {exclude_ids}. They are the "
        f"post-mortem of the bug you are evaluating, and excluding them is "
        f"how we test whether the harness can find the bug *without* reading "
        f"the answer. Reason normally; some grounding entries you might "
        f"expect will not appear.\n"
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


def _reconciler_brief(prep_meta: dict) -> str:
    return (
        f"You are reconciling two audit passes for the target below.\n\n"
        f"TARGET: {prep_meta['target']}\n"
        f"RUN DIR: {prep_meta['run_dir']}\n"
        f"CLAUDE FINDINGS: {prep_meta['run_dir']}/auditor-output.json\n"
        f"CODEX FINDINGS:  {prep_meta['run_dir']}/codex-output.json\n"
        f"STATIC TOOLS:    {prep_meta['static_tools_path']}\n\n"
        f"SOURCE FILES (re-read any you need to adjudicate):\n"
        + "\n".join(f"- {f}" for f in prep_meta["target_files"])
        + "\n\nFollow your system prompt. End your response with a single "
        f"fenced ```json block containing {{findings, model_disagreements, "
        f"notes}}. The /audit driver will extract it and write to "
        f"{prep_meta['run_dir']}/reconciled.json.\n"
    )


def _run_prep(
    target: str | Path,
    scope: str | Path | None,
    deep: bool,
) -> dict:
    cmd = [
        "uv", "run", "--quiet", "python", "-m", "harness.audit_runner", "prep",
        str(target),
    ]
    if scope:
        cmd += ["--scope", str(scope)]
    if deep:
        cmd += ["--deep"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT), check=True)
    return json.loads(proc.stdout.strip().splitlines()[-1])


def _claude_invoke(
    *,
    agent: str,
    brief: str,
    prep_meta: dict,
    exclude_ids: list[str],
    model: str,
    timeout_seconds: int,
) -> subprocess.CompletedProcess:
    """Headless `claude -p --agent <agent>` invocation."""
    claude_bin = shutil.which("claude")
    if not claude_bin:
        raise FileNotFoundError("claude CLI not on PATH")

    add_dirs = {str(REPO_ROOT.resolve())}
    target_resolved = Path(prep_meta["target"]).resolve()
    if REPO_ROOT.resolve() not in target_resolved.parents and target_resolved != REPO_ROOT.resolve():
        add_dirs.add(str(target_resolved))

    cmd = [claude_bin, "-p", "--agent", agent, "--model", model]
    for d in sorted(add_dirs):
        cmd += ["--add-dir", d]
    cmd += ["--output-format", "json", "--dangerously-skip-permissions", brief]

    env = os.environ.copy()
    if exclude_ids:
        env["W3S_CORPUS_EXCLUDE_IDS"] = ",".join(exclude_ids)

    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        timeout=timeout_seconds,
        check=False,
    )


def _extract_fenced_json(stdout: str) -> dict | None:
    """Best-effort JSON extraction from a `claude -p --output-format json` stdout.

    The wrapper looks like {result: "<assistant text>", ...}. The assistant
    text usually contains a ```json``` fenced block.
    """
    try:
        wrapper = json.loads(stdout)
        msg = wrapper.get("result", "") if isinstance(wrapper, dict) else ""
    except json.JSONDecodeError:
        msg = stdout
    m = JSON_FENCE.search(msg)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def _run_finalize(run_dir: Path, findings_path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [
            "uv", "run", "--quiet", "python", "-m", "harness.audit_runner",
            "finalize", str(run_dir), "--findings", str(findings_path),
        ],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    (run_dir / "finalize-stdout.log").write_text(proc.stdout)
    (run_dir / "finalize-stderr.log").write_text(proc.stderr)
    return proc.returncode, (proc.stderr or proc.stdout)[-500:]


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def drive_audit(
    target: str | Path,
    *,
    scope: str | Path | None = None,
    exclude_ids: list[str] | None = None,
    model: str = "opus",
    timeout_seconds: int = 1800,
    deep: bool = False,
) -> DriveResult:
    """Single-model audit: prep → Claude auditor → finalize."""
    exclude_ids = exclude_ids or []
    prep = _run_prep(target, scope, deep)
    run_dir = Path(prep["run_dir"])

    proc = _claude_invoke(
        agent="web3-auditor",
        brief=_auditor_brief(prep, exclude_ids),
        prep_meta=prep,
        exclude_ids=exclude_ids,
        model=model,
        timeout_seconds=timeout_seconds,
    )
    (run_dir / "claude-stdout.log").write_text(proc.stdout)
    (run_dir / "claude-stderr.log").write_text(proc.stderr)

    findings_path = run_dir / "auditor-output.json"
    parse_error: str | None = None
    if not findings_path.exists():
        payload = _extract_fenced_json(proc.stdout)
        if payload is not None:
            findings_path.write_text(json.dumps(payload, indent=2))
        else:
            parse_error = (
                f"no auditor-output.json written and no fenced JSON in stdout "
                f"(rc={proc.returncode}, stderr={proc.stderr[-300:]!r})"
            )

    if findings_path.exists():
        rc, tail = _run_finalize(run_dir, findings_path)
        if rc != 0 and not parse_error:
            parse_error = f"finalize exited {rc}: {tail}"

    return DriveResult(run_dir, findings_path, proc.stdout, parse_error)


def drive_audit_multimodel(
    target: str | Path,
    *,
    scope: str | Path | None = None,
    exclude_ids: list[str] | None = None,
    claude_model: str = "opus",
    codex_model: str = "gpt-5.5",
    codex_reasoning_effort: str = "high",
    timeout_seconds: int = 2400,
    deep: bool = False,
) -> DriveResult:
    """Multi-model: prep → (Claude || Codex) → reconciler → finalize.

    Runs both auditors in parallel via a thread pool. After both finish,
    invokes the web3-reconciler subagent (Claude) to merge their outputs
    and flag genuine disagreements. The reconciled list is the input to
    finalize, so report.md reflects the merged view.
    """
    exclude_ids = exclude_ids or []
    prep = _run_prep(target, scope, deep)
    run_dir = Path(prep["run_dir"])

    # --- two parallel audit passes -------------------------------------
    def _claude() -> tuple[str, str | None]:
        proc = _claude_invoke(
            agent="web3-auditor",
            brief=_auditor_brief(prep, exclude_ids),
            prep_meta=prep,
            exclude_ids=exclude_ids,
            model=claude_model,
            timeout_seconds=timeout_seconds,
        )
        (run_dir / "claude-stdout.log").write_text(proc.stdout)
        (run_dir / "claude-stderr.log").write_text(proc.stderr)

        out_path = run_dir / "auditor-output.json"
        if not out_path.exists():
            payload = _extract_fenced_json(proc.stdout)
            if payload is not None:
                out_path.write_text(json.dumps(payload, indent=2))
                return "ok", None
            return "missing", (
                f"no auditor-output.json and no fenced JSON in stdout "
                f"(rc={proc.returncode})"
            )
        return "ok", None

    def _codex() -> tuple[str, str | None]:
        try:
            result = run_codex_audit(
                prep,
                exclude_ids=exclude_ids,
                model=codex_model,
                reasoning_effort=codex_reasoning_effort,
                timeout_seconds=timeout_seconds,
            )
        except FileNotFoundError as e:
            return "missing", str(e)
        if result.error:
            return "partial", result.error
        return "ok", None

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f_claude = pool.submit(_claude)
        f_codex = pool.submit(_codex)
        claude_status, claude_err = f_claude.result()
        codex_status, codex_err = f_codex.result()

    parse_error: str | None = None
    if claude_status != "ok":
        parse_error = f"claude auditor: {claude_err}"
    if codex_status != "ok":
        # Codex is graceful — partial outputs are still useful as input to
        # the reconciler. We continue, but log.
        (run_dir / "codex-error.log").write_text(codex_err or "")
        if claude_status != "ok":
            return DriveResult(run_dir, run_dir / "reconciled.json", "", parse_error)

    # --- reconciler pass -----------------------------------------------
    claude_out = run_dir / "auditor-output.json"
    codex_out = run_dir / "codex-output.json"
    if not claude_out.exists() and not codex_out.exists():
        return DriveResult(
            run_dir,
            run_dir / "reconciled.json",
            "",
            "neither claude-output nor codex-output is present — cannot reconcile",
        )

    rec_proc = _claude_invoke(
        agent="web3-reconciler",
        brief=_reconciler_brief(prep),
        prep_meta=prep,
        exclude_ids=exclude_ids,  # reconciler uses corpus too, same exclusions apply
        model=claude_model,
        timeout_seconds=timeout_seconds,
    )
    (run_dir / "reconciler-stdout.log").write_text(rec_proc.stdout)
    (run_dir / "reconciler-stderr.log").write_text(rec_proc.stderr)

    reconciled_path = run_dir / "reconciled.json"
    if not reconciled_path.exists():
        payload = _extract_fenced_json(rec_proc.stdout)
        if payload is not None:
            reconciled_path.write_text(json.dumps(payload, indent=2))
        else:
            # Reconciler failed — fall back to the Claude-only output so we
            # still get a report rather than nothing.
            if claude_out.exists():
                reconciled_path.write_text(claude_out.read_text())
                parse_error = (
                    (parse_error + " | " if parse_error else "")
                    + f"reconciler returned no JSON (rc={rec_proc.returncode}); "
                    f"fell back to claude-only findings"
                )
            else:
                return DriveResult(
                    run_dir,
                    reconciled_path,
                    rec_proc.stdout,
                    "reconciler returned no JSON and no fallback available",
                )

    rc, tail = _run_finalize(run_dir, reconciled_path)
    if rc != 0:
        parse_error = (
            (parse_error + " | " if parse_error else "") + f"finalize exited {rc}: {tail}"
        )

    return DriveResult(run_dir, reconciled_path, rec_proc.stdout, parse_error)
