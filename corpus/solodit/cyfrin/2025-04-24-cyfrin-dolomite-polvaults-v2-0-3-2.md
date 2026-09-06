---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Missing event emissions for some important state changes
vuln_class: []
---

# Missing event emissions for some important state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** The POL contracts are missing event emissions for several important state-changing operations.


_1. POLIsolationModeTokenVaultV1_

- `prepareForLiquidation`: No event when a position is prepared for liquidation
- `stake/unstake`: No event for (un)staking actions
- `getReward`: No event for reward claims
- `exit`:  No event for exiting positions

_2. InfraredBGTMetaVault_
- `chargeDTokenFee`: No event for fee charging

_3. POLIsolationModeTraderBaseV2_
- `_POLIsolationModeTraderBaseV2__initialize`:  No event when vault factory is set

_4. MetaVaultRewardTokenFactory_
- `depositIntoDolomiteMarginFromMetaVault`: No event for deposit from meta vault
- `depositIntoDolomiteMarginFromMetaVault`: No event for deposit of other token from meta vault


**Recommended Mitigation:** Consider reviewing the codebase and adding events that track important state changes.


**Dolomite:** Fixed in [e556252](https://github.com/dolomite-exchange/dolomite-margin-modules/commit/e556252bc49d222ea80540242f832fc996711c26) and [ccfcd12](https://github.com/dolomite-exchange/dolomite-margin-modules/commit/ccfcd1278afafae355020bdee4673c792687a109).

**Cyfrin:** Verified.

\clearpage
