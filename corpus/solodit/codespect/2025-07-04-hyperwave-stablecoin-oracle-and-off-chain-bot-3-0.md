---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-01] Additional check for isAtomicRequestValid(...)'
vuln_class: []
---

# [I-01] Additional check for isAtomicRequestValid(...)

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`AtomicQueue.sol`](https://github.com/SwellNetwork/boring-vault/blob/cff94e7093a688578d13279748cdaa0d2b308293/src/atomic-queue/AtomicQueue.sol)

**Description:**

The `isAtomicRequestValid(...)` function is used to validate user-submitted withdrawal requests. It performs several checks, such as verifying the user’s balance and ensuring they have approved the Queue contract to spend their offer tokens.

However, the function does not verify whether the offer token is the Boring Vault share token. This check is crucial and should be added to ensure complete validation redundancy, as recommended for offchain filtering.

**Impact:** Invalid requests may delay the processing of valid ones, since this function plays a critical role in the bot’s request validation logic.

**Recommendation:** Add a check to confirm that the offer token is the Boring Vault share token.

**Status:** Fixed

**Client response:** Fixed in [d3d7f57116f1c366062daf6ddd762e18d9df12de](https://github.com/SwellNetwork/hlp-internal-be/commit/d3d7f57116f1c366062daf6ddd762e18d9df12de).
