#!/usr/bin/env bash
# Automated overnight sweep and scrutinize loop for Bricklane Web3 Bug Bounty Hunter.
# Usage: ./scripts/overnight_bounty.sh
# Make sure ANTHROPIC_API_KEY is set in your environment or local .env file.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== [$(date)] Starting Bricklane Overnight Hunt ==="

# 1. Sweep active contests & rank new candidates
echo "--- Running daily sweep (feed ingestion + Stage 1 triage) ---"
uv run python -m harness.tui sweep

# 2. Show the current queue status
echo "--- Current ranked candidate queue ---"
uv run python -m harness.tui queue

# 3. Suggest the top targets
echo "--- Pick top suggestion ---"
SUGGESTED=$(uv run python -m harness.tui suggest --limit 1 || true)
echo "Top suggested target details:"
echo "$SUGGESTED"

# 4. Run automated maximum-depth scrutinize loop (audit + deep dive + filter + PoC generation)
# By default, autoscrutinize picks the top candidate greedily.
echo "--- Executing maximum-depth autoscrutinize pass ---"
uv run python -m harness.tui autoscrutinize --top 1

# 5. Summary of recent runs
echo "--- Summary of latest audit runs ---"
uv run python -m harness.tui list

echo "=== [$(date)] Bricklane Overnight Hunt Finished ==="
