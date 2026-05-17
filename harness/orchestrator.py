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
    dry_run: bool = False
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
    def _stage1_suspects_block(self) -> str:
        """If the target is a known candidate with Stage 1 results, surface its
        top_suspects so the auditor focuses there first (slice 11 v1)."""
        try:
            from harness import candidates as cand_store
            cand = cand_store.find_by_local_path(self.prep_meta["target"])
        except Exception:  # noqa: BLE001
            return ""
        if not cand or not cand.triage_top_suspects:
            return ""
        suspects_md = "\n".join(
            f"  - `{s.get('file', '?')}::{s.get('function', '?')}` — {s.get('why', '')}"
            for s in cand.triage_top_suspects
        )
        rationale = cand.triage_rationale or "(no rationale)"
        return (
            f"\n\nSTAGE-1 PRIOR ANALYSIS — these surfaces were pre-flagged by "
            f"an Opus pre-screen (score={cand.triage_score}/10):\n"
            f"  rationale: {rationale}\n"
            f"  suspects:\n{suspects_md}\n\n"
            f"Start your hunt at these surfaces but DO NOT be limited to them. "
            f"If you find that one of these is a false positive, say so in your "
            f"notes; if you find a bug elsewhere, that's still a valid finding."
        )

    def _claude_brief(self) -> str:
        target_files = "\n".join(f"- {f}" for f in self.prep_meta["target_files"])
        return (
            f"You are auditing the following target.\n\n"
            f"TARGET: {self.prep_meta['target']}\n"
            f"TARGET KIND: {self.prep_meta['target_kind']}\n"
            f"RUN DIR: {self.prep_meta['run_dir']}\n\n"
            f"SOURCE FILES TO AUDIT (read each one):\n{target_files}\n\n"
            f"STATIC ANALYZER RESULTS: {self.prep_meta['static_tools_path']}\n"
            f"(read this file with Read to see Slither / Aderyn / Foundry output)"
            f"{self._stage1_suspects_block()}\n\n"
            f"Follow the workflow in your system prompt. Search the corpus to "
            f"ground your findings. Write the final JSON findings list to "
            f"{self.prep_meta['run_dir']}/auditor-output.json -- do NOT just paste it "
            f"into chat. Set 'discovered_by': 'claude' on every finding. For "
            f"Critical/High findings on Foundry-shaped targets, fill foundry_poc.\n"
        )

    def _run_claude_auditor(self) -> StageResult:
        return self._run_claude_agent(
            agent="web3-auditor",
            brief=self._claude_brief(),
            stage_name="claude-auditor",
            expected_output_file="auditor-output.json",
        )

    def _run_claude_agent(
        self,
        *,
        agent: str,
        brief: str,
        stage_name: str,
        expected_output_file: str | None,
    ) -> StageResult:
        """Spawn claude -p in stream-json mode and surface tool-uses live."""
        claude_bin = shutil.which("claude")
        if not claude_bin:
            _fail("claude CLI not on PATH")
            return StageResult(stage_name, False, "missing CLI")

        add_dirs = {str(REPO_ROOT.resolve())}
        target_resolved = Path(self.prep_meta["target"]).resolve()
        if (
            REPO_ROOT.resolve() not in target_resolved.parents
            and target_resolved != REPO_ROOT.resolve()
        ):
            add_dirs.add(str(target_resolved))

        cmd = [claude_bin, "-p", "--agent", agent, "--model", self.opts.model]
        for d in sorted(add_dirs):
            cmd += ["--add-dir", d]
        cmd += [
            "--output-format", "stream-json",
            "--verbose",  # stream-json requires --verbose
            "--dangerously-skip-permissions",
            brief,
        ]

        return self._run_claude_stream(cmd, stage_name, expected_output_file)

    def _run_reconciler(self) -> StageResult:
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

        result = self._run_claude_agent(
            agent="web3-reconciler",
            brief=brief,
            stage_name="reconciler",
            expected_output_file=None,
        )
        if not result.ok:
            return result

        # Reconciler writes the fenced JSON in its FINAL assistant message;
        # _run_claude_stream stashes that in <stage>-final-message.txt.
        final = self.run_dir / "reconciler-final-message.txt"
        text = final.read_text() if final.exists() else ""
        m = JSON_FENCE.search(text)
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

    def _run_claude_stream(
        self,
        cmd: list[str],
        stage_name: str,
        expected_output_file: str | None,
    ) -> StageResult:
        """Spawn `claude -p --output-format stream-json` and surface tool-uses
        and assistant turns live as the agent works. Each JSONL event from
        stdout is parsed; the spinner text shows the most recent meaningful
        activity (tool call name, search query, file read, etc.).
        """
        env = os.environ.copy()
        stdout_log = self.run_dir / f"{stage_name}-stdout.log"
        stderr_log = self.run_dir / f"{stage_name}-stderr.log"
        events_log = self.run_dir / f"{stage_name}-events.jsonl"

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
            bufsize=1,
        )

        out_lines: list[str] = []
        err_lines: list[str] = []
        events: list[dict] = []
        latest_activity = ["(launching agent...)"]
        # Per-event-type counts we expose in the spinner.
        tool_counts: dict[str, int] = {}
        final_assistant_text = [""]

        def _summarize_event(ev: dict) -> str | None:
            """Return a human-readable one-liner for this event, or None to skip."""
            etype = ev.get("type")
            if etype == "system":
                sub = ev.get("subtype", "")
                if sub == "init":
                    return "agent initialized"
            elif etype == "assistant":
                msg = ev.get("message") or {}
                content = msg.get("content") or []
                if not isinstance(content, list):
                    return None
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    bt = block.get("type")
                    if bt == "tool_use":
                        name = block.get("name", "?")
                        tool_counts[name] = tool_counts.get(name, 0) + 1
                        inp = block.get("input") or {}
                        # Best-effort short summary of the call args.
                        if isinstance(inp, dict):
                            if "query" in inp:
                                arg = f'"{str(inp["query"])[:60]}"'
                            elif "file_path" in inp:
                                arg = Path(str(inp["file_path"])).name
                            elif "pattern" in inp:
                                arg = f'pattern={str(inp["pattern"])[:50]}'
                            elif "entry_id" in inp:
                                arg = str(inp["entry_id"])
                            elif "command" in inp:
                                arg = str(inp["command"])[:60]
                            else:
                                arg = ""
                        else:
                            arg = ""
                        return f"tool {name}({arg})"
                    if bt == "text":
                        text = (block.get("text") or "").strip()
                        if text:
                            final_assistant_text[0] = text
                            return f'…"{text[:80]}"'
            elif etype == "user":
                # Echoes of tool_result content arriving back to the agent.
                msg = ev.get("message") or {}
                content = msg.get("content") or []
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_result":
                            return None  # too noisy; counts already incremented on tool_use
            elif etype == "result":
                # Final result envelope; contains cost + usage. We capture but
                # don't surface as activity.
                return None
            return None

        def _drain_stdout():
            for line in proc.stdout:
                out_lines.append(line)
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                try:
                    ev = json.loads(line_stripped)
                except json.JSONDecodeError:
                    continue
                events.append(ev)
                summary = _summarize_event(ev)
                if summary:
                    latest_activity[0] = summary[:140]
                # Save final assistant text whenever we see it.

        def _drain_stderr():
            for line in proc.stderr:
                err_lines.append(line)
                if self.opts.verbose:
                    sys.stderr.write(line)

        t_out = threading.Thread(target=_drain_stdout, daemon=True)
        t_err = threading.Thread(target=_drain_stderr, daemon=True)
        t_out.start()
        t_err.start()

        start = time.monotonic()
        with console.status(
            f"[cyan]{stage_name} starting…[/cyan]", spinner="dots"
        ) as status:
            while proc.poll() is None:
                elapsed = int(time.monotonic() - start)
                tc_str = " ".join(f"{n}{k[0].lower()}" for k, n in tool_counts.items()) or "—"
                status.update(
                    f"[cyan]{stage_name} · {elapsed}s · tools[{tc_str}][/cyan] "
                    f"[dim]· {latest_activity[0]}[/dim]"
                )
                time.sleep(0.3)
        t_out.join(timeout=3)
        t_err.join(timeout=3)

        stdout_log.write_text("".join(out_lines))
        stderr_log.write_text("".join(err_lines))
        events_log.write_text("\n".join(json.dumps(e) for e in events))

        rc = proc.returncode
        elapsed = int(time.monotonic() - start)

        # Save the final assistant message separately so reconciler can fence-extract.
        if final_assistant_text[0]:
            (self.run_dir / f"{stage_name}-final-message.txt").write_text(final_assistant_text[0])

        if rc != 0:
            _fail(f"{stage_name} exited rc={rc} after {elapsed}s")
            tail = "".join(err_lines)[-500:]
            if tail.strip():
                _info(f"stderr tail: {tail.strip()[:300]}")
            _info(f"full logs: {stderr_log.relative_to(REPO_ROOT)} {events_log.relative_to(REPO_ROOT)}")
            return StageResult(stage_name, False, str(rc))

        # If we expected a JSON file but the agent emitted it inline instead,
        # extract from the final assistant message.
        if expected_output_file and not (self.run_dir / expected_output_file).exists():
            m = JSON_FENCE.search(final_assistant_text[0])
            if m:
                try:
                    payload = json.loads(m.group(1))
                    (self.run_dir / expected_output_file).write_text(json.dumps(payload, indent=2))
                except json.JSONDecodeError:
                    pass

        # Surface tool-use summary so the user sees what was done.
        if tool_counts:
            tc_pretty = ", ".join(f"{n}× {k}" for k, n in sorted(tool_counts.items(), key=lambda x: -x[1]))
            _info(f"tool use: {tc_pretty}")

        if expected_output_file:
            if (self.run_dir / expected_output_file).exists():
                try:
                    payload = json.loads((self.run_dir / expected_output_file).read_text())
                    n = len(payload.get("findings") or []) if isinstance(payload, dict) else 0
                    _ok(f"{stage_name}: {n} findings emitted ({elapsed}s)")
                except json.JSONDecodeError:
                    _ok(f"{stage_name} complete ({elapsed}s) — output not parseable")
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

        # Stream stderr so per-PoC progress (printed by audit_runner.cmd_finalize)
        # surfaces in the spinner. stdout is buffered; we parse its final JSON line.
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(REPO_ROOT),
            bufsize=1,
        )

        out_lines: list[str] = []
        err_lines: list[str] = []
        latest_activity = ["starting..."]
        poc_done_count = [0]

        def _drain(stream, sink, is_stderr: bool) -> None:
            for line in stream:
                sink.append(line)
                stripped = line.strip()
                if not stripped:
                    continue
                if is_stderr:
                    if stripped.startswith("poc ["):
                        latest_activity[0] = stripped[:140]
                        if "done:" in stripped:
                            poc_done_count[0] += 1
                    elif self.opts.verbose:
                        sys.stderr.write(line)

        t_out = threading.Thread(target=_drain, args=(proc.stdout, out_lines, False), daemon=True)
        t_err = threading.Thread(target=_drain, args=(proc.stderr, err_lines, True), daemon=True)
        t_out.start()
        t_err.start()

        spinner_prefix = (
            "[cyan]validating citations & rendering report"
            + (" (scaffolding + running PoCs)" if self.opts.with_pocs else "")
            + "...[/cyan]"
        )
        start = time.monotonic()
        with console.status(spinner_prefix, spinner="dots") as status:
            while proc.poll() is None:
                elapsed = int(time.monotonic() - start)
                status.update(
                    f"[cyan]finalize · {elapsed}s · pocs done {poc_done_count[0]}[/cyan] "
                    f"[dim]· {latest_activity[0]}[/dim]"
                )
                time.sleep(0.3)
        t_out.join(timeout=3)
        t_err.join(timeout=3)

        # Persist logs for post-hoc inspection.
        (self.run_dir / "finalize-stdout.log").write_text("".join(out_lines))
        (self.run_dir / "finalize-stderr.log").write_text("".join(err_lines))

        if proc.returncode != 0:
            _fail(f"finalize rc={proc.returncode}")
            _info(("".join(err_lines) or "".join(out_lines))[-400:])
            return StageResult("finalize", False, "".join(err_lines)[-200:])

        try:
            summary = json.loads("".join(out_lines).strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            summary = {}

        # Surface per-PoC outcomes inline so the user sees what was reproduced.
        poc_status_lines = [l for l in err_lines if "poc [" in l and "done:" in l]
        for line in poc_status_lines:
            stripped = line.strip()
            # poc [N/T] done:reproduced: <title>
            if "done:reproduced" in stripped:
                _stage_line("✓", stripped, "bold green")
            elif "done:unconfirmed" in stripped:
                _stage_line("?", stripped, "yellow")
            elif "done:compile-error" in stripped:
                _stage_line("!", stripped, "red")
            else:
                _stage_line("·", stripped, "dim")

        _ok(f"report: {summary.get('report_path', '?')}")
        if summary.get("findings_accepted") is not None:
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
        total = 2 if self.opts.dry_run else 3
        _stage_header("prep", 1, total)
        if not self._run_prep().ok:
            return 1
        if self.opts.dry_run:
            _stage_header("dry-run summary", 2, total)
            _ok("prep completed; skipping auditor + finalize per --dry-run")
            _info(
                "outputs to inspect: "
                f"{(self.run_dir / 'prep.json').relative_to(REPO_ROOT)}, "
                f"{(self.run_dir / 'static-tools.json').relative_to(REPO_ROOT)}"
            )
            return 0
        _stage_header("claude-auditor", 2, total)
        if not self._run_claude_auditor().ok:
            return 1
        _stage_header("finalize", 3, total)
        if not self._run_finalize().ok:
            return 1
        self._print_summary()
        return 0

    def run_multimodel(self) -> int:
        total = 2 if self.opts.dry_run else 5
        _stage_header("prep", 1, total)
        if not self._run_prep().ok:
            return 1
        if self.opts.dry_run:
            _stage_header("dry-run summary", 2, total)
            _ok("prep completed; skipping auditors + reconciler + finalize per --dry-run")
            _info(
                "outputs to inspect: "
                f"{(self.run_dir / 'prep.json').relative_to(REPO_ROOT)}, "
                f"{(self.run_dir / 'static-tools.json').relative_to(REPO_ROOT)}"
            )
            return 0

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
