---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-4
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
title: '[I-05] Missing alert on unfavourable exchange rate update'
vuln_class: []
---

# [I-05] Missing alert on unfavourable exchange rate update

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`accountant.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/contract/accountant.py#L37)

**Description:**

The `boring_vault` bot updates the exchange rate in the Accountant contract. The contract checks if the new rate is within the allowed bounds. If not, it pauses the vault:

```solidity
function updateExchangeRate(uint96 newExchangeRate) external requiresAuth {
    // ...
    uint64 currentTime = uint64(block.timestamp);
    uint256 currentExchangeRate = state.exchangeRate;
    uint256 currentTotalShares = vault.totalSupply();
    if (
        currentTime < state.lastUpdateTimestamp + state.minimumUpdateDelayInSeconds
            || newExchangeRate > currentExchangeRate.mulDivDown(state.allowedExchangeRateChangeUpper, 1e4)
            || newExchangeRate < currentExchangeRate.mulDivDown(state.allowedExchangeRateChangeLower, 1e4)
    ) {
        state.isPaused = true;
        // ...
```

As the rate is updated multiple times daily, an out-of-bound value may pause the vault unnecessarily. The bot should notify the protocol team (e.g., via Telegram) before applying such a value, so it can be reviewed and, if needed, updated manually.

**Impact:** An invalid exchange rate can pause the vault, potentially causing unexpected liquidations in integrated protocols that use the vault’s liquid HLP.

**Recommendation:** Notify the protocol team of unfavourable updates and skip the update until reviewed. However, the protocol team should ensure the rate stays fresh.

**Status:** Fixed

**Client response:** Fixed in [7ff95c02b0cb1b147bb1f8a4ae89314e001d982a](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/7ff95c02b0cb1b147bb1f8a4ae89314e001d982a) and [5328945b3866847bfed2b224e5c7d6086a017143](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/5328945b3866847bfed2b224e5c7d6086a017143).
