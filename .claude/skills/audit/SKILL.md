---
name: audit
description: Run a smart-contract security audit on a Solidity target. Wraps static analyzers (Slither, Aderyn, Foundry) + the web3-auditor subagent grounded in the web3Sentinel corpus. Use when the user types `/audit <path-or-file>`.
---

# /audit — web3Sentinel audit driver

You are coordinating a full audit run. Inputs and outputs are deterministic;
the LLM judgement happens inside the `web3-auditor` subagent invocation in
step 3.

## Argument

The target is whatever the user passed after `/audit`. Capture it from the
slash-command argument. Accept:

- A path to a single `.sol` file
- A path to a directory (Foundry project if it contains `foundry.toml`)
- A `0x`-prefixed Ethereum / EVM address (with optional `--chain mainnet|optimism|polygon|arbitrum|base|sepolia`). Source is fetched
  from Sourcify (no auth) with Etherscan v2 as a fallback (set
  `ETHERSCAN_API_KEY` in `.env` if Sourcify misses). EIP-1967 proxies
  are auto-detected — the implementation is fetched into `impl/`.

## Workflow

Follow these steps in order. Do NOT skip the validation in step 5.

### Step 1 — Prep

Run the static analyzers and create the audit run directory:

```bash
uv run python -m harness.audit_runner prep "<target>"
```

Capture the JSON line from stdout — it contains `run_dir`,
`static_tools_path`, `target_files`, `corpus_snapshot`, and a summary of
which static tools succeeded.

If every static tool failed (likely missing binaries), stop and tell the
user what's missing. Otherwise continue even if some tools failed —
Slither alone is enough to proceed.

### Step 2 — Tell the user what we're auditing

In one short line: "Auditing <target> — Slither found N detectors, Aderyn
M, Foundry build <ok/fail>. Spawning auditor."

Don't dump the full prep JSON to the user.

### Step 3 — Invoke the web3-auditor subagent

Use the Agent tool with `subagent_type: web3-auditor`. The prompt must
brief the subagent fully (it cannot see this conversation):

```
You are auditing the following target.

TARGET: <target path>
TARGET KIND: <foundry-project | single-file | directory>
RUN DIR: <run_dir from prep>

SOURCE FILES TO AUDIT (read each one):
- <file 1>
- <file 2>
...

STATIC ANALYZER RESULTS:
The file <static_tools_path> contains the raw JSON output from Slither,
Aderyn, and Foundry. Read it before you start hypothesizing.

Follow the workflow in your system prompt. End with a single fenced
```json ... ``` block containing your findings, matching the schema. Set
"discovered_by": "claude" on every finding.
```

The subagent's tools include MCP corpus search/read — it can ground its
findings without further help from you.

### Step 4 — Capture the subagent's findings

The subagent ends its response with a fenced ```json``` block. Extract
the JSON object and write it to `<run_dir>/auditor-output.json`. If
extraction fails (no JSON block, malformed JSON), surface that to the
user and stop — do NOT try to "fix" the subagent's output.

### Step 5 — Finalize: validate and render

```bash
uv run python -m harness.audit_runner finalize "<run_dir>" --findings "<run_dir>/auditor-output.json"
```

This validates that every finding's `citations` reference real corpus
entries and that uncited findings are flagged `novel: true`. Findings
that fail validation go to `<run_dir>/rejected.md` (not into the report).

The command prints a JSON line with `report_path`, `findings_accepted`,
`findings_rejected`, `parse_errors`.

### Step 6 — Tell the user where the report is

In 1–2 lines: "Report: <report_path>. Accepted N findings, rejected M
(see <run_dir>/rejected.md)." If rejected > 0, briefly note why (most
common cause: subagent invented a citation ID).

Do not paste the full report into chat — the user can open the file.

## Constraints

- Do NOT modify files outside `audits/<run_dir>/`. The target is read-only.
- Do NOT skip the validation step. The citation rule is the load-bearing
  property of this harness; bypassing it defeats the whole point.
- If the subagent returns zero findings, that's a valid result. Render the
  report anyway — the static-tool output is itself useful.
