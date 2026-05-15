---
name: research
description: Distill a cluster of corpus entries into a synthesis note. Use when the user types `/research <topic>` — e.g. `/research flash loan governance attacks`, `/research ERC4626 vault inflation`, `/research bridge replay`. Writes to corpus/synthesis/.
---

# /research — synthesizer driver

You are coordinating one synthesis pass. The user typed `/research`
followed by a topic. Build a synthesis note grounded in the existing
corpus and reindex so future audits can retrieve against it.

## Argument

Whatever the user passed after `/research` is the topic. Slugify it
for filenames (kebab-case, lowercase, alphanumerics + dashes).

Example user inputs:
- `/research flash loan governance attacks`     → slug: flash-loan-governance-attacks
- `/research ERC4626 vault inflation`            → slug: erc4626-vault-inflation
- `/research cross-chain bridge replay`          → slug: cross-chain-bridge-replay

## Workflow

### Step 1 — Pre-check existing notes

```bash
uv run python -m scripts.corpus_query list-synthesis 2>/dev/null | head -50
```

If a synthesis note already exists for this topic (`id: synthesis-<slug>`
or close), tell the user and ask whether to refresh / overwrite or
pick a different topic. Don't silently overwrite.

### Step 2 — Build the seed query

A good seed query is 3-6 words capturing the topic's specific jargon.
Don't use the literal slash-command argument verbatim; refine it.
Examples:
- "flash loan governance attacks" → "flash loan voting power governance"
- "ERC4626 vault inflation"        → "ERC4626 first depositor inflation share"
- "cross-chain bridge replay"      → "cross-chain bridge signature replay nonce"

### Step 3 — Spawn the synthesizer subagent

Use the Agent tool with `subagent_type: web3-synthesizer`. The prompt:

```
TOPIC: <user-supplied topic, verbatim>
SLUG: <slug>
SEED QUERY: <refined seed query>
OUTPUT PATH: corpus/synthesis/<slug>.md

Follow the workflow in your system prompt. Use the MCP corpus tools
(search_corpus, read_corpus_entry) to gather grounding entries. Write
the synthesis note to OUTPUT PATH via Write. End with the
"SYNTHESIS NOTE WRITTEN" confirmation block.
```

### Step 4 — Reindex

After the subagent confirms the note is written:

```bash
uv run python -c "from harness.corpus import reindex; r = reindex(); print(f'inserted={r.inserted} updated={r.updated} errors={len(r.errors)}')"
```

This makes the synthesis note immediately retrievable via search_corpus.

### Step 5 — Tell the user

In 2 lines: where the note is, how many corpus entries it derives from,
which sources it spans. Don't paste the note content.

## Constraints

- Do NOT modify entries outside `corpus/synthesis/`.
- Do NOT overwrite an existing synthesis note without confirming with
  the user first (Step 1).
- If the subagent fails to write the file, do not paper over by writing
  it yourself from chat context. Surface the failure to the user.
