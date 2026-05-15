"""End-to-end audit orchestrator with a live rich display.

Wraps the prep -> auditor -> (codex auditor) -> (reconciler) -> finalize
pipeline and emits stage-by-stage progress to stdout via rich. Designed
to be the user-facing CLI surface; see ``w3s audit <target>``.

Two flavors:
  * ``Orchestrator(...).run_single()``    — one Claude auditor pass.
  * ``Orchestrator(...).run_multimodel()`` — Claude + Codex in parallel
                                              + reconciler merge.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from harness.corpus import REPO_ROOT
from harness.tui import _summary_row, render_status

console = Console()

JSON_FENCE = re.compile(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", re.DOTALL)


# ---------------------------------------------------------------------------
# Stage helpers — each prints a header line, runs work, prints a result line.
# ---------------------------------------------------------------------------


@dataclass
class StageResult:
    name: str
    ok: bool
    detail: str


def _stage_header(name: str, n: int, total: int) -> None:
    console.print(
        f"\n[bold cyan][{n}/{total}][/bold cyan] [bold]{name}[/bold]"
    )


def _stage_line(symbol: str, text: str, style: str = "") -> None:
    """Indented sub-line for stage progress."""
    if style:
        console.print(f"      [{style}]{symbol}[/{style}] {text}")
    else:
        console.print(f"      {symbol} {text}")


def _ok(text: str) -> None:
    _stage_line("✓", text, "green")


def _fail(text: str) -> None:
    _stage_line("✗", text, "red")


def _info(text: str) -> None:
    _stage_line("·", text, "dim")


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


@dataclass
class OrchestratorOptions:
    target: str
    chain: str = "mainnet"
    scope: str | None = None
    model: str = "opus"
    codex_model: str = "gpt-5.5"
    codex_reasoning_effort: str = "high"
    deep: bool = False
    with_pocs: bool = True
    verbose: bool = False
    auditor_timeout_s: int = 1800
    reconciler_timeout_s: int = 1800


class Orchestrator:
    def __init__(self, opts: OrchestratorOptions):
        self.opts = opts
        self.run_dir: Path | None = None
        self.prep_meta: dict = {}

    # --- prep -----------------------------------------------------------
    def _run_prep(self) -> StageResult:
        cmd = [
            "uv", "run", "--quiet", "python", "-m",
            "harness.audit_runner", "prep", self.opts.target,
            "--chain", self.opts.chain,
        ]
        if self.opts.scope:
            cmd += ["--scope", self.opts.scope]
        if self.opts.deep:
            cmd += ["--deep"]

        with console.status("[cyan]running static analyzers...[/cyan]", spinner="dots"):
            proc = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd=str(REPO_ROOT), check=False,
            )
        if proc.returncode != 0:
            _fail(f"prep failed (rc={proc.returncode})")
            _info((proc.stderr or proc.stdout)[-500:])
            return StageResult("prep", False, proc.stderr[-500:])

        try:
            self.prep_meta = json.loads(proc.stdout.strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            _fail("prep produced no parseable meta")
            return StageResult("prep", False, "no meta")
        self.run_dir = Path(self.prep_meta["run_dir"])
        _ok(f"target: {self.prep_meta['target']} ({self.prep_meta['target_kind']})")
        _ok(f"run dir: {self.run_dir.relative_to(REPO_ROOT) if self.run_dir.is_relative_to(REPO_ROOT) else self.run_dir}")
        for s in self.prep_meta.get("static_tools_summary", []):
            if s["succeeded"]:
                count = s.get("finding_count")
                detail = f"{s['tool']}: {count} findings" if count is not None else f"{s['tool']}: ok"
                _ok(detail)
            else:
                _info(f"{s['tool']}: skipped — {(s.get('error') or '')[:70]}")
        return StageResult("prep", True, str(self.run_dir))

    # --- claude auditor ------------------------------------------------
    def _claude_brief(self) -> str:
        target_files = "\n".join(f"- {f}" for f in self.prep_meta["target_files"])
        return (
            f"You are auditing the following target.\n\n"
            f"TARGET: {self.prep_meta['target']}\n"
            f"TARGET KIND: {self.prep_meta['target_kind']}\n"
            f"RUN DIR: {self.prep_meta['run_dir']}\n\n"
            f"SOURCE FILES TO AUDIT (read each one):\n{target_files}\n\n"
            f"STATIC ANALYZER RESULTS: {self.prep_meta['static_tools_path']}\n"
            f"(read this file with Read to see Slither / Aderyn / Foundry output)\n\n"
            f"Follow the workflow in your system prompt. Search the corpus to "
            f"ground your findings. Write the final JSON findings list to "
            f"{self.prep_meta['run_dir']}/auditor-output.json -- do NOT just paste it "
            f"into chat. Set 'discovered_by': 'claude' on every finding. For "
            f"Critical/High findings on Foundry-shaped targets, fill foundry_poc.\n"
        )

    def _run_claude_auditor(self) -> StageResult:
        claude_bin = shutil.which("claude")
        if not claude_bin:
            _fail("claude CLI not on PATH")
            return StageResult("claude-auditor", False, "missing CLI")

        add_dirs = {str(REPO_ROOT.resolve())}
        target_resolved = Path(self.prep_meta["target"]).resolve()
        if (
            REPO_ROOT.resolve() not in target_resolved.parents
            and target_resolved != REPO_ROOT.resolve()
        ):
            add_dirs.add(str(target_resolved))

        cmd = [claude_bin, "-p", "--agent", "web3-auditor", "--model", self.opts.model]
        for d in sorted(add_dirs):
            cmd += ["--add-dir", d]
        cmd += ["--output-format", "json", "--dangerously-skip-permissions", self._claude_brief()]

        return self._run_streaming(cmd, "claude-auditor", "auditor-output.json")

    def _run_reconciler(self) -> StageResult:
        claude_bin = shutil.which("claude")
        if not claude_bin:
            _fail("claude CLI not on PATH")
            return StageResult("reconciler", False, "missing CLI")

        brief = (
            f"You are reconciling two audit passes for the target below.\n\n"
            f"TARGET: {self.prep_meta['target']}\n"
            f"RUN DIR: {self.prep_meta['run_dir']}\n"
            f"CLAUDE FINDINGS: {self.prep_meta['run_dir']}/auditor-output.json\n"
            f"CODEX FINDINGS:  {self.prep_meta['run_dir']}/codex-output.json\n"
            f"STATIC TOOLS:    {self.prep_meta['static_tools_path']}\n\n"
            + "SOURCE FILES (re-read any you need to adjudicate):\n"
            + "\n".join(f"- {f}" for f in self.prep_meta["target_files"])
            + f"\n\nFollow your system prompt. End your response with a single "
            f"fenced ```json block containing {{findings, model_disagreements, "
            f"notes}}. The orchestrator will extract it and write to "
            f"{self.prep_meta['run_dir']}/reconciled.json.\n"
        )

        add_dirs = {str(REPO_ROOT.resolve())}
        target_resolved = Path(self.prep_meta["target"]).resolve()
        if REPO_ROOT.resolve() not in target_resolved.parents and target_resolved != REPO_ROOT.resolve():
            add_dirs.add(str(target_resolved))

        cmd = [claude_bin, "-p", "--agent", "web3-reconciler", "--model", self.opts.model]
        for d in sorted(add_dirs):
            cmd += ["--add-dir", d]
        cmd += ["--output-format", "json", "--dangerously-skip-permissions", brief]

        # Reconciler writes ```json``` fenced output to stdout; we extract.
        result = self._run_streaming(cmd, "reconciler", expected_output_file=None)
        if not result.ok:
            return result

        wrapper_path = self.run_dir / "reconciler-stdout.log"
        text = wrapper_path.read_text() if wrapper_path.exists() else ""
        try:
            wrapper = json.loads(text)
            assistant_msg = wrapper.get("result", "") if isinstance(wrapper, dict) else ""
        except json.JSONDecodeError:
            assistant_msg = text

        m = JSON_FENCE.search(assistant_msg)
        if not m:
            _fail("reconciler returned no fenced JSON")
            return StageResult("reconciler", False, "no fenced json")
        try:
            payload = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            _fail(f"reconciler JSON malformed: {e}")
            return StageResult("reconciler", False, str(e))
        (self.run_dir / "reconciled.json").write_text(json.dumps(payload, indent=2))
        n = len(payload.get("findings") or [])
        d = len(payload.get("model_disagreements") or [])
        _ok(f"merged: {n} findings, {d} disagreements")
        return StageResult("reconciler", True, f"{n} findings")

    def _run_streaming(
        self,
        cmd: list[str],
        stage_name: str,
        expected_output_file: str | None,
    ) -> StageResult:
        """Spawn a long-running command with a live spinner + activity tail."""
        env = os.environ.copy()
        # Persistent log
        stdout_log = self.run_dir / f"{stage_name.replace('-', '-')}-stdout.log"
        stderr_log = self.run_dir / f"{stage_name.replace('-', '-')}-stderr.log"

        # Use Popen so we can poll stderr lines for status hints.
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
        )

        out_chunks: list[str] = []
        err_chunks: list[str] = []
        latest_activity = ["(starting...)"]

        def _drain(stream, sink: list[str], is_stderr: bool):
            for line in stream:
                sink.append(line)
                if is_stderr and self.opts.verbose:
                    sys.stderr.write(line)
                if line.strip():
                    latest_activity[0] = line.strip()[:120]

        t_out = threading.Thread(target=_drain, args=(proc.stdout, out_chunks, False), daemon=True)
        t_err = threading.Thread(target=_drain, args=(proc.stderr, err_chunks, True), daemon=True)
        t_out.start()
        t_err.start()

        spinner_text = f"running {stage_name}..."
        start = time.monotonic()
        with console.status(f"[cyan]{spinner_text}[/cyan]", spinner="dots") as status:
            while proc.poll() is None:
                elapsed = int(time.monotonic() - start)
                status.update(
                    f"[cyan]{stage_name} · {elapsed}s elapsed[/cyan] "
                    f"[dim]· last: {latest_activity[0]}[/dim]"
                )
                time.sleep(0.4)
        t_out.join(timeout=2)
        t_err.join(timeout=2)

        stdout_log.write_text("".join(out_chunks))
        stderr_log.write_text("".join(err_chunks))

        rc = proc.returncode
        elapsed = int(time.monotonic() - start)
        if rc != 0:
            _fail(f"{stage_name} exited rc={rc} after {elapsed}s")
            _info(f"see {stderr_log.relative_to(REPO_ROOT)}")
            return StageResult(stage_name, False, str(rc))

        if expected_output_file and not (self.run_dir / expected_output_file).exists():
            # Try fenced-JSON extraction from stdout.
            try:
                wrapper = json.loads("".join(out_chunks))
                msg = wrapper.get("result", "") if isinstance(wrapper, dict) else ""
            except json.JSONDecodeError:
                msg = "".join(out_chunks)
            m = JSON_FENCE.search(msg)
            if m:
                try:
                    payload = json.loads(m.group(1))
                    (self.run_dir / expected_output_file).write_text(json.dumps(payload, indent=2))
                except json.JSONDecodeError:
                    pass

        if expected_output_file:
            if (self.run_dir / expected_output_file).exists():
                payload = json.loads((self.run_dir / expected_output_file).read_text())
                n = len(payload.get("findings") or [])
                _ok(f"{stage_name}: {n} findings emitted ({elapsed}s)")
            else:
                _fail(f"{stage_name}: no {expected_output_file} produced")
                return StageResult(stage_name, False, "missing output file")
        else:
            _ok(f"{stage_name} complete ({elapsed}s)")

        return StageResult(stage_name, True, str(rc))

    def _run_codex_auditor(self) -> StageResult:
        from harness.codex_audit import run_codex_audit

        with console.status("[cyan]running codex auditor...[/cyan]", spinner="dots"):
            try:
                result = run_codex_audit(
                    self.prep_meta,
                    model=self.opts.codex_model,
                    reasoning_effort=self.opts.codex_reasoning_effort,
                    timeout_seconds=self.opts.auditor_timeout_s,
                )
            except FileNotFoundError as e:
                _fail(f"codex skipped — {e}")
                return StageResult("codex-auditor", False, str(e))
        if result.error and not result.findings:
            _fail(f"codex error: {result.error[:120]}")
            return StageResult("codex-auditor", False, result.error or "")
        _ok(f"codex-auditor: {len(result.findings)} findings emitted")
        return StageResult("codex-auditor", True, f"{len(result.findings)} findings")

    def _run_finalize(self) -> StageResult:
        cmd = [
            "uv", "run", "--quiet", "python", "-m",
            "harness.audit_runner", "finalize",
            str(self.run_dir),
            "--findings",
            str(self.run_dir / ("reconciled.json" if (self.run_dir / "reconciled.json").exists() else "auditor-output.json")),
        ]
        if not self.opts.with_pocs:
            cmd.append("--no-pocs")

        msg = "[cyan]validating citations & rendering report"
        if self.opts.with_pocs:
            msg += " (scaffolding + running PoCs)"
        msg += "...[/cyan]"
        with console.status(msg, spinner="dots"):
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT), check=False)

        if proc.returncode != 0:
            _fail(f"finalize rc={proc.returncode}")
            _info((proc.stderr or proc.stdout)[-400:])
            return StageResult("finalize", False, proc.stderr[-200:])
        try:
            summary = json.loads(proc.stdout.strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            summary = {}
        _ok(f"report: {summary.get('report_path', '?')}")
        if summary.get("findings_accepted"):
            _info(
                f"findings accepted: {summary['findings_accepted']} "
                f"(rejected: {summary.get('findings_rejected', 0)})"
            )
        return StageResult("finalize", True, summary.get("report_path", ""))

    # --- entry points ---------------------------------------------------
    def _print_summary(self) -> None:
        if not self.run_dir:
            return
        s = _summary_row(self.run_dir)
        table = Table(show_header=False, box=None)
        table.add_column(style="dim")
        table.add_column()
        table.add_row("target", s["target"])
        table.add_row("findings", f"{s['n_findings']}")
        for sev, n in s["by_sev"].items():
            table.add_row(f"  {sev}", str(n))
        if s["by_poc"]:
            table.add_row("pocs", "")
            for status, n in s["by_poc"].items():
                table.add_row(f"  {status}", str(n))
        table.add_row("coverage", s["coverage"])
        table.add_row("report", str(self.run_dir / "report.md"))
        console.print()
        console.print(Panel(table, title=f"audit complete — {self.run_dir.name}", border_style="green"))

    def run_single(self) -> int:
        total = 3
        _stage_header("prep", 1, total)
        if not self._run_prep().ok:
            return 1
        _stage_header("claude-auditor", 2, total)
        if not self._run_claude_auditor().ok:
            return 1
        _stage_header("finalize", 3, total)
        if not self._run_finalize().ok:
            return 1
        self._print_summary()
        return 0

    def run_multimodel(self) -> int:
        total = 5
        _stage_header("prep", 1, total)
        if not self._run_prep().ok:
            return 1

        _stage_header("auditors (claude || codex in parallel)", 2, total)
        # Run both in parallel; both write their own output files.
        with ThreadPoolExecutor(max_workers=2) as pool:
            f_c = pool.submit(self._run_claude_auditor)
            f_x = pool.submit(self._run_codex_auditor)
            r_c = f_c.result()
            r_x = f_x.result()
        if not r_c.ok and not r_x.ok:
            _fail("both auditors failed; aborting")
            return 1

        _stage_header("reconciler", 3, total)
        if (self.run_dir / "auditor-output.json").exists() and (
            self.run_dir / "codex-output.json"
        ).exists():
            self._run_reconciler()
        else:
            _info("only one auditor produced output — falling back to that one")

        _stage_header("finalize", 4, total)
        if not self._run_finalize().ok:
            return 1

        _stage_header("done", 5, total)
        self._print_summary()
        return 0
