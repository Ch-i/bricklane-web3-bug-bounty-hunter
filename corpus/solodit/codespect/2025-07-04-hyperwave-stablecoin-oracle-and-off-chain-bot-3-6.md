---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-6
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
title: '[I-07] Note Error'
vuln_class: []
---

# [I-07] Note Error

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`RedstoneStablecoinRateProvider.sol`](https://github.com/SwellNetwork/boring-vault/tree/ce21e49b7a7be06c3a96c3c3ea6982c32e3ff224/src/oracles/RedstoneStablecoinRateProvider.sol)

**Description:**

During the assignment in the constructor function, there is an error in the note. The note states that the Default Lower Bound is 5 bps, but it should actually be 9995 bps.

```solidity
constructor(...) {
    //...
    // Default Lower Bound is 5 bps
    lowerBound = 10 ** RATE_DECIMALS * 9995 / 10_000;
    //...
}
```

**Impact:** Incorrect comments may mislead developers and cause difficulties in code maintenance.

**Recommendation:** Change 5 bps to 9995 bps.

**Status:** Fixed

**Client response:** Fixed in [PR-6](https://github.com/SwellNetwork/boring-vault/pull/6/files).
