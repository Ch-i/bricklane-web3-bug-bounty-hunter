"""Parse `forge coverage --report lcov` output.

Coverage is wired into the audit harness as a DAoB-style prior: functions
the project's own tests don't exercise are the highest-priority hunting
ground for the auditor.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileCoverage:
    file: str
    lines_found: int = 0
    lines_hit: int = 0
    functions_found: int = 0
    functions_hit: int = 0
    # Per-function: name -> hit count (LCOV ``FNDA``)
    function_hits: dict[str, int] = field(default_factory=dict)
    # First line of each function, used to compose locations
    function_lines: dict[str, int] = field(default_factory=dict)


@dataclass
class CoverageReport:
    files: list[FileCoverage] = field(default_factory=list)
    total_lines: int = 0
    hit_lines: int = 0
    total_functions: int = 0
    hit_functions: int = 0

    @property
    def line_pct(self) -> float:
        if not self.total_lines:
            return 0.0
        return 100.0 * self.hit_lines / self.total_lines

    @property
    def function_pct(self) -> float:
        if not self.total_functions:
            return 0.0
        return 100.0 * self.hit_functions / self.total_functions

    def uncovered_functions(self) -> list[dict]:
        """Flat list of {file, function, line} for every function with hit=0."""
        out: list[dict] = []
        for fc in self.files:
            for fn, hits in fc.function_hits.items():
                if hits == 0:
                    out.append(
                        {
                            "file": fc.file,
                            "function": fn,
                            "line": fc.function_lines.get(fn),
                        }
                    )
        return out


def parse_lcov(content: str) -> CoverageReport:
    """Parse LCOV format. Tolerant of forge's variations."""
    report = CoverageReport()
    current: FileCoverage | None = None

    for raw in content.splitlines():
        line = raw.strip()
        if not line:
            continue

        if line.startswith("SF:"):
            current = FileCoverage(file=line[3:])
            report.files.append(current)
        elif current is None:
            continue
        elif line == "end_of_record":
            current = None
        elif line.startswith("FN:"):
            # FN:<line>,<name>
            try:
                rest = line[3:]
                line_no, fn = rest.split(",", 1)
                current.function_lines[fn] = int(line_no)
                current.function_hits.setdefault(fn, 0)
            except ValueError:
                continue
        elif line.startswith("FNDA:"):
            # FNDA:<hits>,<name>
            try:
                rest = line[5:]
                hits, fn = rest.split(",", 1)
                current.function_hits[fn] = int(hits)
            except ValueError:
                continue
        elif line.startswith("FNF:"):
            try:
                current.functions_found = int(line[4:])
            except ValueError:
                pass
        elif line.startswith("FNH:"):
            try:
                current.functions_hit = int(line[4:])
            except ValueError:
                pass
        elif line.startswith("LF:"):
            try:
                current.lines_found = int(line[3:])
            except ValueError:
                pass
        elif line.startswith("LH:"):
            try:
                current.lines_hit = int(line[3:])
            except ValueError:
                pass

    for fc in report.files:
        report.total_lines += fc.lines_found
        report.hit_lines += fc.lines_hit
        report.total_functions += fc.functions_found
        report.hit_functions += fc.functions_hit
    return report


def _forge_bin() -> str | None:
    for c in (Path(sys.prefix) / "bin" / "forge", Path.home() / ".foundry" / "bin" / "forge"):
        if c.is_file() and os.access(c, os.X_OK):
            return str(c)
    return shutil.which("forge")


def run_coverage(project_root: Path, *, timeout_seconds: int = 600) -> tuple[CoverageReport | None, str]:
    """Run `forge coverage --report lcov` and parse the result.

    Returns (CoverageReport | None, message). None if forge isn't installed,
    no tests are present, or the run failed. Message gives context for
    failures so the auditor can be told "coverage unavailable: <reason>"
    rather than silently dropping the signal.
    """
    forge = _forge_bin()
    if not forge:
        return None, "forge not on PATH"
    if not (project_root / "foundry.toml").exists():
        return None, "no foundry.toml"

    env = os.environ.copy()
    env["PATH"] = os.pathsep.join(
        [str(Path(sys.prefix) / "bin"), str(Path.home() / ".foundry" / "bin"), env.get("PATH", "")]
    )

    try:
        proc = subprocess.run(
            [forge, "coverage", "--report", "lcov", "--report", "summary"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, f"forge coverage timed out after {timeout_seconds}s"
    except Exception as e:  # noqa: BLE001
        return None, f"forge coverage failed: {e}"

    if proc.returncode != 0 and "no tests found" in (proc.stdout + proc.stderr).lower():
        return None, "no tests in project"
    if proc.returncode != 0 and "is not test" in (proc.stdout + proc.stderr).lower():
        return None, "forge coverage failed: no tests run"

    lcov_path = project_root / "lcov.info"
    if not lcov_path.exists():
        return None, f"forge coverage produced no lcov.info (rc={proc.returncode})"

    content = lcov_path.read_text()
    return parse_lcov(content), "ok"
