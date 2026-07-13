"""Drive a Codex (GPT-5.x) audit pass non-interactively.

Mirrors what the web3-auditor Claude subagent does, but routes through the
``codex exec`` CLI so we can get a second opinion from a different model
family. The reconciler then merges both outputs.

Codex doesn't have ``.claude/agents/`` equivalent — the system-prompt-ish
content is delivered as the initial user message.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from harness.corpus import REPO_ROOT
from harness.schema import Finding


# OpenAI's structured-output mode requires every property in `properties`
# to be listed in `required`. Truly-optional fields use nullable types.
OUTPUT_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["Critical", "High", "Medium", "Low", "Informational", "Gas"],
                    },
                    "location": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "file": {"type": "string"},
                                "line_start": {"type": "integer"},
                                "line_end": {"type": ["integer", "null"]},
                            },
                            "required": ["file", "line_start", "line_end"],
                            "additionalProperties": False,
                        },
                    },
                    "description": {"type": "string"},
                    "impact": {"type": "string"},
                    "recommendation": {"type": "string"},
                    "proof_of_concept": {"type": ["string", "null"]},
                    "foundry_poc": {
                        "type": ["object", "null"],
                        "properties": {
                            "test_name": {"type": "string"},
                            "setup": {"type": "string"},
                            "exploit": {"type": "string"},
                            "assertion": {"type": "string"},
                            "imports": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "notes": {"type": ["string", "null"]},
                        },
                        "required": ["test_name", "setup", "exploit", "assertion", "imports", "notes"],
                        "additionalProperties": False,
                    },
                    "citations": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "novel": {"type": "boolean"},
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "discovered_by": {
                        "type": "string",
                        "enum": ["codex"],
                    },
                },
                "required": [
                    "title",
                    "severity",
                    "location",
                    "description",
                    "impact",
                    "recommendation",
                    "proof_of_concept",
                    "foundry_poc",
                    "citations",
                    "novel",
                    "confidence",
                    "discovered_by",
                ],
                "additionalProperties": False,
            },
        },
        "notes": {"type": ["string", "null"]},
    },
    "required": ["findings", "notes"],
    "additionalProperties": False,
}


SYSTEM_PROMPT = """\
You are the web3-codex-auditor: a Solidity smart-contract security auditor
producing structured findings for the Bricklane harness. A separate
Claude-driven auditor is running the same audit in parallel; a reconciler
will then merge both outputs and surface disagreements for human review.
Your value is contributing a different model family's perspective.

# Hard rules

1. Every finding MUST have `citations` (corpus IDs) OR `novel: true`.
   This is non-negotiable; downstream validation rejects findings that
   violate it. Cite ONLY corpus IDs you actually retrieved with the
   corpus_query CLI — do not invent IDs.

2. The corpus is the Bricklane knowledge base (Solodit findings, SWC
   entries, and others). Query it via Bash:

       python -m scripts.corpus_query search "<query>" [--vuln-class CLASS] [--severity High|Medium|...] [--top-k N]
       python -m scripts.corpus_query read <entry-id>
       python -m scripts.corpus_query stats

   Use these tools to ground every finding. For each hypothesis you form
   from the source, search the corpus, read the top hits, and cite the IDs
   that genuinely apply.

3. Be conservative with severity.
   Critical = funds at immediate risk.
   High     = funds at risk under specific conditions.
   Medium   = significant misbehavior, not direct funds loss.
   Low      = best-practice violations or minor edge cases.
   Don't inflate.

4. Do NOT modify the target source. Read-only analysis.

5. Set `"discovered_by": "codex"` on every finding (this distinguishes
   your output from the Claude auditor's in the reconciler).

6. For Critical/High findings on a Foundry-shaped target, fill the
   `foundry_poc` object with a structured proof of concept:
       test_name:  must start with `test_`, valid Solidity identifier.
       setup:      Solidity body for setUp() — deployments, deals, etc.
       exploit:    Solidity body for the test function — the attack.
       assertion:  Solidity assertion that PASSES if the bug exists
                   (e.g. `assertGt(attacker.balance, 100 ether);`).
       imports:    .sol paths the test needs.
       notes:      any caveats (fork pinning, helper contracts, etc).
   The harness scaffolds this into a `.t.sol` file, runs `forge test`,
   and tags the finding `reproduced` / `unconfirmed` / `compile-error`.

   If you can't write a faithful PoC, set `foundry_poc: null`. A fake
   PoC that fails to compile is worse than no PoC. For Medium/Low/
   Informational findings, `foundry_poc: null` is the default.

# Workflow

a. Read all target source files (paths in the user message).
b. Read the static-analyzer JSON (path in the user message). It contains
   normalized Slither/Aderyn/Foundry results.
c. Identify the protocol category (AMM, lending, vault, bridge, token, ...).
d. Triage each static-tool flag: confirm or refute via source reading,
   then search corpus for the specific pattern and cite the matched entries.
e. Hypothesize what static tools miss: business-logic flaws, economic
   attacks, multi-step exploits, initialization issues, access-control
   granularity, fixed-point edge cases. For each hypothesis, search the
   corpus, read the most relevant entry, then decide if the pattern fits
   the actual source. If yes, write a grounded finding. If no, move on
   — don't force findings just because the corpus has entries.

# Output

Return ONLY a single JSON object matching the schema you have been given
(via --output-schema). Do not wrap the JSON in code fences. Do not add
commentary outside the JSON.
"""


@dataclass
class CodexResult:
    findings_path: Path
    findings: list[Finding]
    raw_output: str
    error: str | None


def build_user_message(prep_meta: dict, exclude_ids: list[str]) -> str:
    target_files = "\n".join(f"- {f}" for f in prep_meta["target_files"])
    exclude_note = (
        f"\nEVAL MODE: the following corpus entries are filtered out of "
        f"`corpus_query search` results: {exclude_ids}. They cover the bug "
        f"you are evaluating; this is the harness's way of testing whether "
        f"you can find the bug from source alone. Reason normally; the "
        f"environment will silently drop those IDs from search hits.\n"
        if exclude_ids
        else ""
    )

    return (
        f"You are auditing the following target.\n\n"
        f"TARGET: {prep_meta['target']}\n"
        f"TARGET KIND: {prep_meta['target_kind']}\n"
        f"RUN DIR: {prep_meta['run_dir']}\n\n"
        f"SOURCE FILES TO AUDIT (read each one with `cat`):\n{target_files}\n\n"
        f"STATIC ANALYZER RESULTS:\n{prep_meta['static_tools_path']}\n"
        f"(this file is JSON; read it via `cat` and treat the detector list "
        f"as ground-truth hints, not as the full bug list).\n"
        f"{exclude_note}\n"
        f"Follow the workflow described in the system rules I've already "
        f"given you. Emit ONLY the JSON object that matches the output "
        f"schema. Set `discovered_by: \"codex\"` on every finding.\n"
    )


def run_codex_audit(
    prep_meta: dict,
    *,
    exclude_ids: list[str] | None = None,
    model: str = "gpt-5.5",
    reasoning_effort: str = "high",
    timeout_seconds: int = 1800,
) -> CodexResult:
    """Spawn `codex exec` with our system prompt + per-target user message.

    Writes ``codex-output.json`` into the run dir and returns the parsed
    Findings (validated against the harness schema; invalid records are
    skipped and counted in ``CodexResult.error`` summary).
    """
    exclude_ids = exclude_ids or []
    run_dir = Path(prep_meta["run_dir"])
    codex_bin = shutil.which("codex") or os.path.expanduser("~/.npm-global/bin/codex")
    if not Path(codex_bin).exists():
        raise FileNotFoundError("codex CLI not on PATH — `npm install -g @openai/codex`")

    schema_path = run_dir / "codex-output-schema.json"
    schema_path.write_text(json.dumps(OUTPUT_SCHEMA))

    last_msg_path = run_dir / "codex-last-message.json"

    user_message = build_user_message(prep_meta, exclude_ids)
    # Concatenate the system prompt + user message into one prompt arg, with
    # a clear delimiter so codex still sees the structured prompt.
    combined = f"{SYSTEM_PROMPT}\n\n---\n\n{user_message}"

    env = os.environ.copy()
    if exclude_ids:
        env["W3S_CORPUS_EXCLUDE_IDS"] = ",".join(exclude_ids)

    cmd = [
        codex_bin,
        "exec",
        "--model",
        model,
        "-c",
        f"model_reasoning_effort=\"{reasoning_effort}\"",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--cd",
        str(REPO_ROOT),
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(last_msg_path),
        "--ephemeral",
        combined,
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CodexResult(
            findings_path=run_dir / "codex-output.json",
            findings=[],
            raw_output="",
            error=f"codex timed out after {timeout_seconds}s",
        )

    (run_dir / "codex-stdout.log").write_text(proc.stdout)
    (run_dir / "codex-stderr.log").write_text(proc.stderr)

    # codex writes the FINAL assistant message to --output-last-message;
    # with --output-schema, that file contains the validated JSON object.
    findings_path = run_dir / "codex-output.json"
    error: str | None = None

    payload_text = ""
    if last_msg_path.exists():
        payload_text = last_msg_path.read_text().strip()
    elif proc.stdout.strip():
        # Fallback: try to parse the tail of stdout.
        payload_text = proc.stdout.strip()

    findings: list[Finding] = []
    if not payload_text:
        error = "codex produced no output"
    else:
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError as e:
            error = f"codex output is not valid JSON: {e}"
            findings_path.write_text(payload_text)
            return CodexResult(findings_path, [], proc.stdout, error)

        findings_path.write_text(json.dumps(payload, indent=2))
        for i, item in enumerate(payload.get("findings", [])):
            try:
                findings.append(Finding.model_validate(item))
            except Exception as e:  # noqa: BLE001
                # Don't fail the whole run on one bad finding.
                error = (error or "") + f"\nfinding[{i}] invalid: {e}"

    return CodexResult(findings_path, findings, proc.stdout, error)
