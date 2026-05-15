"""Static analyzer wrappers.

Each wrapper:
  * detects whether the underlying binary is installed
  * runs it against a target (file or project root)
  * parses output to a common ``StaticToolFindings`` shape
  * NEVER raises on tool failure — failures are reported in the returned object
    so the audit subagent can reason about them.

The audit subagent receives the full collection as JSON-serialized context.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from harness.coverage import run_coverage
from harness.schema import StaticToolFindings


_EXTRA_BIN_DIRS = [
    Path(sys.prefix) / "bin",
    Path.home() / ".foundry" / "bin",
    Path.home() / ".cargo" / "bin",
    Path.home() / ".local" / "bin",
]


def _which(name: str) -> str | None:
    """Locate a binary in non-default install dirs first, then fall back to PATH.

    Resolves the gap between where pip/cargo/foundryup put binaries and what
    Claude Code's Bash actually has on PATH (no ~/.bashrc).
    """
    for d in _EXTRA_BIN_DIRS:
        candidate = d / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return shutil.which(name)


def _subprocess_env() -> dict[str, str]:
    """Augment PATH so subprocesses find tools we installed in non-default places:

    * venv/bin (slither, solc-select)
    * ~/.foundry/bin (forge, cast, anvil)
    * ~/.cargo/bin (aderyn)
    * ~/.local/bin (pipx)

    Necessary because Claude Code spawns Bash without sourcing ~/.bashrc.
    """
    env = os.environ.copy()
    extra = [
        str(Path(sys.prefix) / "bin"),
        str(Path.home() / ".foundry" / "bin"),
        str(Path.home() / ".cargo" / "bin"),
        str(Path.home() / ".local" / "bin"),
    ]
    current = env.get("PATH", "").split(os.pathsep)
    for p in extra:
        if p and p not in current:
            current.insert(0, p)
    env["PATH"] = os.pathsep.join(current)
    return env


@dataclass
class StaticToolsConfig:
    """Knobs the /audit skill flips depending on flags."""

    target: Path
    target_kind: str  # "foundry-project" | "single-file" | "directory"
    run_slither: bool = True
    run_aderyn: bool = True
    run_foundry: bool = True
    run_halmos: bool = False  # opt-in via --deep
    run_mythril: bool = False  # opt-in via --deep
    timeout_seconds: int = 600


# ---------------------------------------------------------------------------
# Slither
# ---------------------------------------------------------------------------


def run_slither(cfg: StaticToolsConfig) -> StaticToolFindings:
    slither_bin = _which("slither")
    if not slither_bin:
        return StaticToolFindings(
            tool="slither", succeeded=False, output={}, error="slither not on PATH"
        )

    try:
        result = subprocess.run(
            [slither_bin, str(cfg.target), "--json", "-"],
            capture_output=True,
            text=True,
            timeout=cfg.timeout_seconds,
            check=False,
            env=_subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return StaticToolFindings(
            tool="slither", succeeded=False, output={}, error="timeout"
        )
    except Exception as e:  # noqa: BLE001
        return StaticToolFindings(tool="slither", succeeded=False, output={}, error=str(e))

    # Slither writes JSON to stdout when `--json -` is set, but it still exits
    # non-zero if it found findings (annoying convention). Treat valid JSON
    # as success regardless of exit code.
    output: dict = {}
    if result.stdout.strip():
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            return StaticToolFindings(
                tool="slither",
                succeeded=False,
                output={"stdout": result.stdout[:5000], "stderr": result.stderr[:5000]},
                error="failed to parse slither JSON output",
            )

    version = _capture_version([slither_bin, "--version"])
    return StaticToolFindings(
        tool="slither",
        version=version,
        succeeded=True,
        output=_compact_slither(output),
        error=result.stderr[:1500] if result.stderr else None,
    )


def _compact_slither(raw: dict) -> dict:
    """Trim Slither's JSON to what the audit agent actually needs.

    Slither's raw JSON is ~10x larger than necessary because it includes the
    full AST node descriptor of every flagged region. We keep: detector,
    impact, confidence, description, elements (file/lines), markdown body.
    """
    detectors = raw.get("results", {}).get("detectors", []) or []
    compact = []
    for d in detectors:
        elements = []
        for el in d.get("elements", []) or []:
            sm = el.get("source_mapping", {}) or {}
            elements.append(
                {
                    "type": el.get("type"),
                    "name": el.get("name"),
                    "filename": sm.get("filename_relative") or sm.get("filename_short"),
                    "lines": sm.get("lines"),
                }
            )
        compact.append(
            {
                "check": d.get("check"),
                "impact": d.get("impact"),
                "confidence": d.get("confidence"),
                "description": d.get("description"),
                "markdown": d.get("markdown"),
                "elements": elements,
            }
        )
    return {"detectors": compact, "detector_count": len(compact)}


# ---------------------------------------------------------------------------
# Aderyn
# ---------------------------------------------------------------------------


def run_aderyn(cfg: StaticToolsConfig) -> StaticToolFindings:
    aderyn_bin = _which("aderyn")
    if not aderyn_bin:
        return StaticToolFindings(
            tool="aderyn", succeeded=False, output={}, error="aderyn not on PATH"
        )

    # Aderyn ≥ 0.x supports `--output report.json` for JSON output.
    out_file = cfg.target / ".aderyn-report.json" if cfg.target.is_dir() else cfg.target.parent / ".aderyn-report.json"
    cmd = [aderyn_bin, str(cfg.target), "--output", str(out_file)]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=cfg.timeout_seconds,
            check=False,
            env=_subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return StaticToolFindings(tool="aderyn", succeeded=False, output={}, error="timeout")
    except Exception as e:  # noqa: BLE001
        return StaticToolFindings(tool="aderyn", succeeded=False, output={}, error=str(e))

    if not out_file.exists():
        return StaticToolFindings(
            tool="aderyn",
            succeeded=False,
            output={"stderr": result.stderr[:5000]},
            error=f"aderyn did not produce JSON at {out_file}",
        )

    try:
        raw = json.loads(out_file.read_text())
    except json.JSONDecodeError as e:
        return StaticToolFindings(
            tool="aderyn", succeeded=False, output={}, error=f"invalid JSON: {e}"
        )
    finally:
        out_file.unlink(missing_ok=True)

    version = _capture_version([aderyn_bin, "--version"])
    return StaticToolFindings(
        tool="aderyn",
        version=version,
        succeeded=True,
        output=_compact_aderyn(raw),
    )


def _compact_aderyn(raw: dict) -> dict:
    """Aderyn JSON has high+low+info issues. Flatten and trim."""
    flat = []
    for severity in ("critical_issues", "high_issues", "medium_issues", "low_issues", "nc_issues"):
        section = raw.get(severity, {}) or {}
        for issue in (section.get("issues") or []):
            flat.append(
                {
                    "severity": severity.replace("_issues", ""),
                    "title": issue.get("title"),
                    "description": issue.get("description"),
                    "detector_name": issue.get("detector_name"),
                    "instances": [
                        {
                            "contract_path": i.get("contract_path"),
                            "line_no": i.get("line_no"),
                        }
                        for i in (issue.get("instances") or [])
                    ],
                }
            )
    return {"issues": flat, "issue_count": len(flat)}


# ---------------------------------------------------------------------------
# Foundry (build-only context, not detection)
# ---------------------------------------------------------------------------


def run_foundry(cfg: StaticToolsConfig) -> StaticToolFindings:
    forge_bin = _which("forge")
    if not forge_bin:
        return StaticToolFindings(
            tool="foundry", succeeded=False, output={}, error="forge not on PATH"
        )

    if not (cfg.target / "foundry.toml").exists():
        return StaticToolFindings(
            tool="foundry",
            succeeded=False,
            output={},
            error="no foundry.toml in target — not a Foundry project",
        )

    try:
        build = subprocess.run(
            [forge_bin, "build", "--json"],
            cwd=cfg.target,
            capture_output=True,
            text=True,
            timeout=cfg.timeout_seconds,
            check=False,
            env=_subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return StaticToolFindings(tool="foundry", succeeded=False, output={}, error="timeout")
    except Exception as e:  # noqa: BLE001
        return StaticToolFindings(tool="foundry", succeeded=False, output={}, error=str(e))

    build_ok = build.returncode == 0
    payload: dict = {
        "build_ok": build_ok,
        "stdout_tail": build.stdout[-2000:] if build.stdout else "",
        "stderr_tail": build.stderr[-2000:] if build.stderr else "",
    }

    # Coverage-guided prior: if the project has tests, run forge coverage and
    # surface uncovered functions as audit-priority hints. Failure is graceful
    # — coverage is opportunistic, never blocking.
    if build_ok:
        report, msg = run_coverage(cfg.target)
        if report is not None:
            payload["coverage"] = {
                "status": "ok",
                "line_pct": round(report.line_pct, 2),
                "function_pct": round(report.function_pct, 2),
                "total_functions": report.total_functions,
                "hit_functions": report.hit_functions,
                "total_lines": report.total_lines,
                "hit_lines": report.hit_lines,
                # The auditor reads this list as a "go-hunt-here" prior.
                "uncovered_functions": report.uncovered_functions()[:60],
            }
        else:
            payload["coverage"] = {"status": "unavailable", "reason": msg}

    version = _capture_version([forge_bin, "--version"])
    return StaticToolFindings(
        tool="foundry",
        version=version,
        succeeded=True,  # the wrapper succeeded; build may still have failed
        output=payload,
    )


# ---------------------------------------------------------------------------
# Halmos / Mythril (deferred to --deep mode)
# ---------------------------------------------------------------------------


def run_halmos(cfg: StaticToolsConfig) -> StaticToolFindings:
    halmos_bin = _which("halmos")
    if not halmos_bin:
        return StaticToolFindings(
            tool="halmos", succeeded=False, output={}, error="halmos not on PATH (pipx install halmos)"
        )
    if not (cfg.target / "foundry.toml").exists():
        return StaticToolFindings(
            tool="halmos",
            succeeded=False,
            output={},
            error="halmos requires a Foundry project (no foundry.toml found)",
        )
    try:
        result = subprocess.run(
            [halmos_bin, "--json-output", "/dev/stdout"],
            cwd=cfg.target,
            capture_output=True,
            text=True,
            timeout=cfg.timeout_seconds,
            check=False,
            env=_subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return StaticToolFindings(tool="halmos", succeeded=False, output={}, error="timeout")
    except Exception as e:  # noqa: BLE001
        return StaticToolFindings(tool="halmos", succeeded=False, output={}, error=str(e))

    output: dict | list | str
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = result.stdout[-5000:]

    return StaticToolFindings(
        tool="halmos",
        version=_capture_version([halmos_bin, "--version"]),
        succeeded=result.returncode == 0,
        output=output,
        error=result.stderr[-1500:] if result.stderr else None,
    )


def run_mythril(cfg: StaticToolsConfig) -> StaticToolFindings:
    myth_bin = _which("myth")
    if not myth_bin:
        return StaticToolFindings(
            tool="mythril", succeeded=False, output={}, error="myth not on PATH (pipx install mythril)"
        )
    if cfg.target_kind != "single-file":
        return StaticToolFindings(
            tool="mythril",
            succeeded=False,
            output={},
            error="mythril wrapper only supports single-file targets in v0",
        )
    try:
        result = subprocess.run(
            [myth_bin, "analyze", str(cfg.target), "-o", "json"],
            capture_output=True,
            text=True,
            timeout=cfg.timeout_seconds,
            check=False,
            env=_subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return StaticToolFindings(tool="mythril", succeeded=False, output={}, error="timeout")
    except Exception as e:  # noqa: BLE001
        return StaticToolFindings(tool="mythril", succeeded=False, output={}, error=str(e))

    output: dict | list | str
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        output = result.stdout[-5000:]

    return StaticToolFindings(
        tool="mythril",
        version=_capture_version([myth_bin, "version"]),
        succeeded=result.returncode in (0, 1),  # myth exits 1 when findings present
        output=output,
    )


# ---------------------------------------------------------------------------
# orchestrator
# ---------------------------------------------------------------------------


def run_all(cfg: StaticToolsConfig) -> list[StaticToolFindings]:
    results: list[StaticToolFindings] = []
    if cfg.run_slither:
        results.append(run_slither(cfg))
    if cfg.run_aderyn:
        results.append(run_aderyn(cfg))
    if cfg.run_foundry:
        results.append(run_foundry(cfg))
    if cfg.run_halmos:
        results.append(run_halmos(cfg))
    if cfg.run_mythril:
        results.append(run_mythril(cfg))
    return results


def _capture_version(cmd: list[str]) -> str | None:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=False)
        return (r.stdout or r.stderr).strip().splitlines()[0][:200] if r.stdout or r.stderr else None
    except Exception:  # noqa: BLE001
        return None
