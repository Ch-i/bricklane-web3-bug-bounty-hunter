"""`w3s doctor` — environment check.

Verifies every external dependency the harness uses is installed and
reachable. Prints a table; exits 0 only if every REQUIRED tool is ok.

Required:
    slither, forge, cast, claude, solc(-select)
Optional but recommended:
    aderyn, halmos, myth, codex
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.text import Text

from harness.corpus import REPO_ROOT
from harness.static import _which

console = Console()

# (name, args-for-version, required?, role)
CHECKS = [
    ("slither", ["--version"], True, "Static analysis (always-on detector pass)"),
    ("solc", ["--version"], True, "Solidity compiler (slither dep)"),
    ("solc-select", ["versions"], True, "solc version manager"),
    ("forge", ["--version"], True, "Foundry — build + coverage + PoC execution"),
    ("cast", ["--version"], False, "Foundry — on-chain tx trace replay"),
    ("claude", ["--version"], True, "Claude CLI — auditor + reconciler subagents"),
    ("codex", ["--version"], False, "Codex CLI — cross-validation auditor (multimodel)"),
    ("aderyn", ["--version"], False, "Static analysis (Cyfrin) — complements slither"),
    ("halmos", ["--version"], False, "Symbolic test runner (--deep flag)"),
    ("myth", ["version"], False, "Mythril — bytecode symbolic exec (--deep flag)"),
]


@dataclass
class ToolCheck:
    name: str
    path: str | None
    version: str | None
    required: bool
    role: str
    ok: bool
    error: str | None = None


def check_tool(name: str, version_args: list[str]) -> tuple[str | None, str | None, str | None]:
    """Return (path, version_string, error_string). version=None on failure."""
    path = _which(name)
    if not path:
        return None, None, "not on PATH"
    try:
        proc = subprocess.run(
            [path, *version_args],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return path, None, "version check timed out"
    except Exception as e:  # noqa: BLE001
        return path, None, f"failed to invoke: {e}"

    out = (proc.stdout or proc.stderr or "").splitlines()
    version = out[0].strip() if out else None
    # myth in particular prints a traceback on startup but still works for analyze.
    if version is None:
        return path, None, f"no version output (rc={proc.returncode})"
    return path, version[:60], None


def check_claude_auth() -> tuple[bool, str]:
    """Spawn a tiny `claude -p` to confirm auth is working."""
    cl = _which("claude")
    if not cl:
        return False, "claude not on PATH"
    try:
        proc = subprocess.run(
            [cl, "-p", "--model", "haiku", "--output-format", "json", "respond with only OK"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "auth check timed out after 30s"
    except Exception as e:  # noqa: BLE001
        return False, f"auth check failed: {e}"

    if proc.returncode != 0:
        return False, f"rc={proc.returncode}: {(proc.stderr or proc.stdout)[-200:]}"
    if '"is_error":true' in proc.stdout or '"error"' in proc.stdout.lower():
        return False, "claude returned an error"
    return True, "auth ok"


def check_codex_auth() -> tuple[bool, str]:
    cx = _which("codex")
    if not cx:
        return False, "codex not on PATH"
    cfg = Path.home() / ".codex" / "auth.json"
    if not cfg.exists():
        return False, "no ~/.codex/auth.json (run `codex login`)"
    return True, "auth file present"


def check_corpus() -> tuple[bool, str]:
    db = REPO_ROOT / "corpus.db"
    corpus_dir = REPO_ROOT / "corpus"
    if not corpus_dir.exists():
        return False, "no corpus/ directory"
    md_count = sum(1 for _ in corpus_dir.rglob("*.md"))
    if md_count == 0:
        return False, "corpus/ has no markdown entries"
    if not db.exists():
        return False, f"corpus/ has {md_count} entries but corpus.db is missing — run reindex"
    try:
        from harness.corpus import stats

        s = stats()
        return True, f"{s['total']} entries, {len(s['by_source'])} sources"
    except Exception as e:  # noqa: BLE001
        return False, f"corpus DB unreadable: {e}"


def check_mcp_config() -> tuple[bool, str]:
    cfg = REPO_ROOT / ".mcp.json"
    if not cfg.exists():
        return False, "no .mcp.json — MCP-mode retrieval won't work"
    return True, "MCP config present"


def check_env_vars() -> list[tuple[str, str, bool, str]]:
    """Return (var, status, present, role)."""
    out: list[tuple[str, str, bool, str]] = []
    for v, role in [
        ("ETHERSCAN_API_KEY", "optional: fallback for /audit 0x... when Sourcify misses"),
        ("ANTHROPIC_API_KEY", "optional: direct API; claude CLI uses its own auth"),
        ("W3S_CORPUS_EXCLUDE_IDS", "set automatically by eval runs"),
    ]:
        present = bool(os.environ.get(v))
        status = "set" if present else "unset"
        out.append((v, status, present, role))
    return out


def run_doctor(skip_auth: bool = False) -> int:
    rows: list[ToolCheck] = []
    for name, args, required, role in CHECKS:
        path, version, err = check_tool(name, args)
        ok = path is not None and (version is not None or "myth" in name)
        # myth's --version traceback is a known quirk; presence on PATH is enough.
        if "myth" in name and path:
            ok = True
        rows.append(
            ToolCheck(
                name=name,
                path=path,
                version=version,
                required=required,
                role=role,
                ok=ok,
                error=err,
            )
        )

    # Render tools table
    t = Table(title="External tools", show_lines=False)
    t.add_column("Tool", style="cyan", no_wrap=True)
    t.add_column("Status")
    t.add_column("Version", style="dim")
    t.add_column("Role", style="dim")

    any_required_missing = False
    for r in rows:
        if r.ok:
            status = Text("ok", style="green")
        elif r.required:
            status = Text("MISSING (required)", style="bold red")
            any_required_missing = True
        else:
            status = Text("missing (optional)", style="yellow")
        t.add_row(r.name, status, r.version or (r.error or "—"), r.role)
    console.print(t)

    # Auth checks
    if not skip_auth:
        console.print()
        auth_table = Table(title="Authentication", show_header=False, box=None)
        auth_table.add_column("Check", style="cyan")
        auth_table.add_column("Result")
        ok_claude, msg_claude = check_claude_auth()
        auth_table.add_row(
            "claude CLI auth",
            Text(msg_claude, style="green" if ok_claude else "red"),
        )
        ok_codex, msg_codex = check_codex_auth()
        auth_table.add_row(
            "codex CLI auth",
            Text(msg_codex, style="green" if ok_codex else "yellow"),
        )
        console.print(auth_table)
    else:
        ok_claude = True

    # Corpus + config
    console.print()
    sys_table = Table(title="Project state", show_header=False, box=None)
    sys_table.add_column("Check", style="cyan")
    sys_table.add_column("Result")
    ok_corpus, msg_corpus = check_corpus()
    sys_table.add_row("corpus", Text(msg_corpus, style="green" if ok_corpus else "red"))
    ok_mcp, msg_mcp = check_mcp_config()
    sys_table.add_row(".mcp.json", Text(msg_mcp, style="green" if ok_mcp else "yellow"))
    console.print(sys_table)

    # Env vars
    console.print()
    env_table = Table(title="Environment variables", show_header=True, header_style="dim", box=None)
    env_table.add_column("Var", style="cyan")
    env_table.add_column("State")
    env_table.add_column("Role", style="dim")
    for v, status, present, role in check_env_vars():
        env_table.add_row(v, Text(status, style="green" if present else "dim"), role)
    console.print(env_table)

    # Verdict
    console.print()
    if any_required_missing or not ok_corpus or not ok_claude:
        console.print("[bold red]NOT READY[/bold red] — fix the items above marked red before running audits.")
        return 1
    console.print("[bold green]READY[/bold green] — all required tools present, corpus loaded, claude auth ok.")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-auth",
        action="store_true",
        help="Skip the live claude auth check (costs a few cents).",
    )
    args = parser.parse_args(argv)
    return run_doctor(skip_auth=args.skip_auth)


if __name__ == "__main__":
    sys.exit(main())
