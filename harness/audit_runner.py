"""Audit run orchestrator — invoked by the /audit skill.

Two subcommands:

    prep <target>           — resolve target, create run dir, run static tools,
                              print JSON describing what the auditor subagent
                              needs to consume.

    finalize <run-dir>      — given a findings JSON (from the subagent),
        --findings PATH       validate citations, build the report, write
                              report.md + sibling artifacts.

The skill drives both halves; the subagent runs in between.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from harness.citations import validate_findings
from harness.corpus import REPO_ROOT
from harness.onchain import ADDR_RE, fetch_verified_source, materialize_to_disk
from harness.render import write_report
from harness.schema import AuditReport, Finding, ModelDisagreement, StaticToolFindings
from harness.static import StaticToolsConfig, run_all


# ---------------------------------------------------------------------------
# target resolution
# ---------------------------------------------------------------------------


def resolve_target(arg: str, *, chain: str = "mainnet") -> tuple[Path, str, dict]:
    """Return (resolved_path, target_kind, target_metadata).

    Supports:
      * 0x-prefixed address (chain configurable) — fetched from Sourcify /
        Etherscan, materialized to a temp dir, then treated like a directory
      * single .sol file
      * directory (foundry-project if foundry.toml present, else generic)
    """
    # Deployed address mode
    if ADDR_RE.match(arg.strip()):
        addr = arg.strip()
        fetched = fetch_verified_source(addr, chain=chain)
        # Materialize under audits/<slug>-source/ — kept beside the audit run
        # for reproducibility. The actual run_dir is created later in cmd_prep.
        slug = f"{addr[:10]}-{fetched.chain_id}"
        target_dir = REPO_ROOT / "audits" / "onchain-source" / slug
        materialize_to_disk(fetched, target_dir)
        meta = {
            "address": fetched.address,
            "chain_id": fetched.chain_id,
            "chain": chain,
            "contract_name": fetched.name,
            "compiler": fetched.compiler_version,
            "source": fetched.fetched_via,
            "is_proxy": fetched.is_proxy,
            "implementation_address": fetched.implementation_address,
            "materialized_at": str(target_dir),
        }
        return target_dir, "deployed-address", meta

    p = Path(arg).expanduser().resolve()
    if not p.exists():
        raise SystemExit(f"target does not exist: {p}")

    if p.is_file():
        if p.suffix == ".sol":
            return p, "single-file", {}
        raise SystemExit(f"target is a file but not .sol: {p}")

    if (p / "foundry.toml").exists():
        return p, "foundry-project", {}
    return p, "directory", {}


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "-", s.lower()).strip("-") or "target"


# ---------------------------------------------------------------------------
# prep — runs static tools and writes them out
# ---------------------------------------------------------------------------


def cmd_prep(args: argparse.Namespace) -> int:
    target, kind, target_metadata = resolve_target(args.target, chain=args.chain)
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    ts_str = timestamp.strftime("%Y%m%dT%H%M%SZ")

    if kind == "deployed-address":
        target_slug = f"{target_metadata['address'][:10]}-{target_metadata['chain']}"
    else:
        target_slug = slugify(target.name)
    run_dir = REPO_ROOT / "audits" / f"{target_slug}-{ts_str}"
    run_dir.mkdir(parents=True, exist_ok=True)

    cfg = StaticToolsConfig(
        target=target,
        target_kind=kind,
        run_halmos=args.deep,
        run_mythril=args.deep,
    )
    static_results = run_all(cfg)

    # If --scope is set, drop detectors that don't touch any file in scope.
    # This keeps static-tools.json focused enough for the subagent's context.
    if args.scope:
        scope_path = Path(args.scope).resolve()
        scope_parts = scope_path.parts
        static_results = [_scope_filter_static(r, scope_path, scope_parts) for r in static_results]

    static_path = run_dir / "static-tools.json"
    static_path.write_text(
        json.dumps([t.model_dump() for t in static_results], indent=2)
    )

    # Tell the caller everything it needs to brief the subagent.
    # Static tools see the whole project (so imports resolve); target_files
    # is what the auditor subagent actually reads, so we filter out
    # dependencies/build artifacts.
    target_files: list[str] = []
    if kind == "single-file":
        target_files = [str(target)]
    else:
        scope_root = Path(args.scope).resolve() if args.scope else target
        target_files = sorted(
            str(p)
            for p in scope_root.rglob("*.sol")
            if not any(
                segment in p.parts
                for segment in ("node_modules", "lib", "out", "cache", ".forge-snapshots")
            )
        )

    meta = {
        "run_dir": str(run_dir),
        "target": str(target),
        "target_kind": kind,
        "target_metadata": target_metadata,
        "timestamp": timestamp.isoformat(),
        "static_tools_path": str(static_path),
        "static_tools_summary": [
            {
                "tool": r.tool,
                "succeeded": r.succeeded,
                "error": r.error,
                "finding_count": _finding_count(r),
            }
            for r in static_results
        ],
        "target_files": target_files,
        "corpus_snapshot": _git_sha(REPO_ROOT / "corpus"),
    }
    (run_dir / "prep.json").write_text(json.dumps(meta, indent=2))

    # Print as a single JSON line so the skill can capture it with `tail -1`.
    print(json.dumps(meta))
    return 0


def _scope_filter_static(r: StaticToolFindings, scope_path: Path, scope_parts: tuple) -> StaticToolFindings:
    """Drop detectors that have no element under scope_path. Idempotent for failed tools."""
    if not r.succeeded or not isinstance(r.output, dict):
        return r
    if r.tool == "slither":
        kept = []
        for d in r.output.get("detectors") or []:
            elements = d.get("elements") or []
            in_scope = False
            for el in elements:
                fname = el.get("filename")
                if not fname:
                    continue
                # filename comes back as a relative path from project root.
                try:
                    abs_path = (scope_path.parent / fname) if not Path(fname).is_absolute() else Path(fname)
                except Exception:  # noqa: BLE001
                    continue
                if scope_path in abs_path.parents or abs_path == scope_path:
                    in_scope = True
                    break
                # crude substring check for relative filenames like "src/unstoppable/Foo.sol"
                if str(scope_path).split("/")[-1] in fname:
                    in_scope = True
                    break
            if in_scope:
                kept.append(d)
        r.output = {"detectors": kept, "detector_count": len(kept)}
    elif r.tool == "aderyn":
        kept = []
        for issue in r.output.get("issues") or []:
            instances = issue.get("instances") or []
            for inst in instances:
                cp = inst.get("contract_path") or ""
                if str(scope_path).split("/")[-1] in cp:
                    kept.append(issue)
                    break
        r.output = {"issues": kept, "issue_count": len(kept)}
    return r


def _finding_count(r: StaticToolFindings) -> int | None:
    if not r.succeeded:
        return None
    if r.tool == "slither":
        return r.output.get("detector_count") if isinstance(r.output, dict) else None
    if r.tool == "aderyn":
        return r.output.get("issue_count") if isinstance(r.output, dict) else None
    return None


def _git_sha(path: Path) -> str:
    """SHA of the directory's last git commit, or 'untracked' if not under git."""
    try:
        result = subprocess.run(
            ["git", "log", "-n", "1", "--format=%H", "--", str(path)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=False,
        )
        sha = (result.stdout or "").strip()
        return sha or "untracked"
    except Exception:  # noqa: BLE001
        return "untracked"


# ---------------------------------------------------------------------------
# finalize — consumes subagent's findings JSON and renders the report
# ---------------------------------------------------------------------------


def cmd_finalize(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "prep.json").exists():
        raise SystemExit(f"no prep.json in {run_dir} — did you run `prep` first?")

    prep = json.loads((run_dir / "prep.json").read_text())
    findings_payload = json.loads(Path(args.findings).read_text())

    # Accept either a bare list or {"findings": [...]} envelope.
    raw_findings = (
        findings_payload["findings"]
        if isinstance(findings_payload, dict) and "findings" in findings_payload
        else findings_payload
    )
    raw_disagreements = (
        findings_payload.get("model_disagreements", [])
        if isinstance(findings_payload, dict)
        else []
    )

    findings: list[Finding] = []
    parse_errors: list[str] = []
    for i, item in enumerate(raw_findings):
        try:
            findings.append(Finding.model_validate(item))
        except Exception as e:  # noqa: BLE001
            parse_errors.append(f"finding[{i}]: {e}")

    model_disagreements: list[ModelDisagreement] = []
    for i, item in enumerate(raw_disagreements):
        try:
            model_disagreements.append(ModelDisagreement.model_validate(item))
        except Exception as e:  # noqa: BLE001
            parse_errors.append(f"disagreement[{i}]: {e}")

    check = validate_findings(findings)

    static_tools_raw = json.loads((run_dir / "static-tools.json").read_text())
    static_tools = [StaticToolFindings.model_validate(t) for t in static_tools_raw]

    model_versions: dict[str, str] = {}
    try:
        cli_v = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=False
        ).stdout.strip()
        if cli_v:
            model_versions["claude-cli"] = cli_v
    except Exception:  # noqa: BLE001
        pass

    prep_meta = prep.get("target_metadata") or {}
    prep_meta.setdefault("target_files_count", len(prep.get("target_files", [])))

    report = AuditReport(
        target=prep["target"],
        target_kind=prep["target_kind"],
        timestamp=datetime.fromisoformat(prep["timestamp"]),
        corpus_snapshot=prep.get("corpus_snapshot", "untracked"),
        model_versions=model_versions,
        static_tools=static_tools,
        findings=check.valid,
        model_disagreements=model_disagreements,
        target_metadata=prep_meta,
    )
    report_path = write_report(report, run_dir)

    # Write a rejection log so the user can see what was filtered.
    if check.rejected or parse_errors:
        log = ["# Rejected findings\n"]
        for f, reason in check.rejected:
            log.append(f"## `{f.title}`\nreason: {reason}\n")
        if parse_errors:
            log.append("## Parse errors\n")
            log.extend(f"- {e}\n" for e in parse_errors)
        (run_dir / "rejected.md").write_text("\n".join(log))

    print(
        json.dumps(
            {
                "report_path": str(report_path),
                "run_dir": str(run_dir),
                "findings_accepted": len(check.valid),
                "findings_rejected": len(check.rejected),
                "parse_errors": len(parse_errors),
            }
        )
    )
    return 0


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prep = sub.add_parser("prep", help="Resolve target, run static tools, write prep.json")
    p_prep.add_argument("target")
    p_prep.add_argument(
        "--chain",
        default="mainnet",
        help="Chain for deployed-address mode (mainnet | optimism | polygon | "
        "arbitrum | base | sepolia | <chain-id>). Ignored for local targets.",
    )
    p_prep.add_argument(
        "--scope",
        help="Restrict the auditor subagent's reading list to .sol files under "
        "this path (still compiles full project for slither). Useful for "
        "challenge-by-challenge audits of a multi-challenge repo.",
    )
    p_prep.add_argument("--deep", action="store_true", help="Also run Halmos and Mythril")
    p_prep.set_defaults(func=cmd_prep)

    p_fin = sub.add_parser("finalize", help="Render report.md from findings JSON")
    p_fin.add_argument("run_dir")
    p_fin.add_argument("--findings", required=True, help="Path to findings JSON from auditor")
    p_fin.set_defaults(func=cmd_finalize)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
