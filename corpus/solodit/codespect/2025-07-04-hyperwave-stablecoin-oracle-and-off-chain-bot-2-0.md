---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[L-01] Insufficient offchain filtering for withdrawal requests'
vuln_class: []
---

# [L-01] Insufficient offchain filtering for withdrawal requests

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py#L229)

**Description:**

Before processing withdrawal requests, the bot performs offchain filtering to minimize the number of RPC calls. One of these filters involves verifying the validity of a request using the AtomicQueue, specifically via the `isAtomicRequestValid(...)` function.

However, the current implementation of the filtering only checks whether a request has been marked as solved or not. This is insufficient, as it does not reliably indicate whether the request has been *properly* solved.

The filtering logic should be improved by introducing the following checks:

- `offerAmount > 0`: This ensures that the request has actually been filled;
- Deadline not exceeded: Requests whose deadlines have passed should be skipped to avoid unnecessary RPC calls;
- offer token equals the `boringVault` address: If the offer token does not match the expected vault address, the withdrawal will revert. This check is currently missing from the `isAtomicRequestValid(...)` validation;

**Impact:** Failure to implement these checks may lead to unnecessary latency when solving withdrawal requests and could cause transaction reverts.

**Recommendation:** Enhance the offchain filtering logic to include:

- A check for `offerAmount > 0`;
- Validation that the deadline has not been exceeded;
- Confirmation that the offer token matches the `boringVault` address;

**Status:** Fixed

**Client response:** Fixed in [4ca30a19ba0e76c77ceff2c3ce7084133018b189](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/4ca30a19ba0e76c77ceff2c3ce7084133018b189).
