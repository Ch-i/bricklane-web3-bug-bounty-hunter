---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-02] Check user’s offer balance across requests to prevent unnecessary reverts'
vuln_class: []
---

# [I-02] Check user’s offer balance across requests to prevent unnecessary reverts

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py)

**Description:**

Users create atomic requests via `safeUpdateAtomicRequest(...)`, which verifies whether the user has sufficient offer balance and allowance to the `AtomicQueue` contract. This is intended to ensure only valid requests are created and that the user has enough Boring Vault shares.

Later, the Hyperwave solver bot checks request validity again via `isAtomicRequestValid(...)`, which performs similar validations. However, these checks are insufficient and allow for a specific edge case that may cause the bot to raise an error and delay solving of otherwise valid requests. Here’s an example:

- A user holds 10 shares;
- The user submits two requests: A (`want = USDe`) and B (`want = USDT`), both with `offerAmount = 10`;
- Both requests pass the balance and allowance checks at submission time and during bot validation;
- The bot includes both requests in its solving plan;
- The batch for request A is solved successfully;
- When attempting to solve the batch containing request B, the user’s share balance is already depleted (0), causing the transaction to revert;

As a result, the bot encounters a failure when executing the second batch, leading to unnecessary delays in processing valid requests.

**Impact:** Potential failure of the bot and delay in solving requests due to inconsistent request accounting.

**Recommendation:** Consider adding logic on the bot side to track cumulative user balances across all pending requests, and only include those that can be fully covered.

**Status:** Fixed

**Client response:** Fixed in [5eedc610bb1d0e9df64e366067ccbc297cc3f9c0](https://github.com/SwellNetwork/hlp-internal-be/commit/5eedc610bb1d0e9df64e366067ccbc297cc3f9c0).
