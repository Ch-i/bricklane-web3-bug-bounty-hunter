---
name: web3-codex-auditor
description: GPT-5.x / Codex-driven Solidity audit agent. Mirrors web3-auditor's contract but runs via the `codex exec` CLI. Use to get a second opinion from a different model family — the reconciler merges both.
tools: Bash, Read, Grep, Glob
model: opus
---

# NOTE

This agent definition is here for **documentation parity** with
`web3-auditor.md`. The actual codex auditor runs as a Python helper
(`harness.codex_audit`) that invokes `codex exec` directly — Claude Code
does not dispatch this subagent; the `/audit` skill calls the helper as
a subprocess in parallel with the Claude auditor.

The codex auditor's runtime system prompt (kept identical in spirit to
the Claude auditor's) is constructed by `harness.codex_audit.build_prompt`.
Citation rules, severity rubric, and corpus-grounding requirements are
the same as `web3-auditor`. The only differences:

- Codex doesn't have MCP wired up by default in this project, so the
  agent uses `python -m scripts.corpus_query` via Bash for corpus access.
- Output is enforced via codex's `--output-schema` flag so we don't have
  to extract JSON from prose.
- `discovered_by` is set to `"codex"` on every finding (the reconciler
  uses this to distinguish the two model families' outputs).
