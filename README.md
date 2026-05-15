# web3Sentinel

Smart contract & web3 audit harness with an autoresearch corpus loop.

## What this is

A research-first project + Claude Code agent layer that:
1. **Builds a security corpus** automatically from Solodit, arXiv, public audit reports, and vulnerability registries.
2. **Audits Solidity targets** using two model families in parallel (Opus + GPT-5-Codex via authenticated CLIs), grounded in retrieved corpus entries with mandatory citation.
3. **Tracks recall** against a benchmark of historical exploits so improvements are measurable.

Not a daemon, not a CLI binary you ship — a directory you live inside via Claude Code.

## Layout

```
web3Sentinel/
├── corpus/           # Markdown entries with YAML frontmatter (one per finding/paper/post-mortem)
├── corpus.db         # sqlite mirror of frontmatter + FTS5 + embeddings (gitignored)
├── crawlers/         # Source-specific ingestion scripts (run via cron)
├── harness/          # Static-tool wrappers, schema, report renderer, citation validator
├── mcp_server/       # `web3sentinel-corpus` MCP server (search/read/list/stats)
├── eval/             # Historical-exploit benchmark + scoring
├── scripts/          # One-off and scheduled utilities (seed_swc, ingest_md)
├── notebooks/        # Research notebooks for corpus exploration
├── .claude/
│   ├── agents/       # web3-auditor, web3-codex-auditor, web3-reconciler, web3-synthesizer
│   └── skills/       # /audit, /research, /refresh-corpus
└── audits/           # Generated audit reports (gitignored)
```

## Setup

```sh
# Python deps via uv
uv sync --extra embed --extra mcp --extra static

# External Solidity tooling (binaries, not pip)
curl -L https://foundry.paradigm.xyz | bash && foundryup
cargo install aderyn   # https://github.com/Cyfrin/aderyn

# Optional --deep tools (pinned to conflicting z3-solver versions; install via pipx so they don't share an env)
pipx install halmos    # symbolic test runner for Foundry
pipx install mythril   # bytecode symbolic execution

# Optional: Codex CLI for cross-validation (slice 4)
# https://github.com/openai/codex
```

Claude Code picks up `.claude/agents/` and `.claude/skills/` automatically when you launch from this directory.

## Status

Slice 1 (v0): SWC seed corpus + single-model audit harness + Damn Vulnerable DeFi smoke test.

See `TaskList` from Claude Code for live progress.
