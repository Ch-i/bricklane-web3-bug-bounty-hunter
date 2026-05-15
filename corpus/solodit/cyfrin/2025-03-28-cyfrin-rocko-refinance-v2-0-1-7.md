---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-1-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Consider allowing update to `AAVE_DATA_PROVIDER`
vuln_class: []
---

# Consider allowing update to `AAVE_DATA_PROVIDER`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::AAVE_DATA_PROVIDER` immutably stores the address of `AaveProtocolDataProvider`. However `AaveProtocolDataProvider` is not upgradeable and the "current" one on mainnet was deployed 43 days ago to address 0x497a1994c46d4f6C864904A9f1fac6328Cb7C8a6.

Hence consider whether `AAVE_DATA_PROVIDER` should not be `immutable` and an `onlyOwner` function should exist to allow updating it in the future.

Since `RockoFlashRefinance` has no relevant internal state it can just be re-deloyed. The trade-off is having  `immutable` `AAVE_DATA_PROVIDER` means user transactions involving it cost slightly less gas but the contract needs to be re-deployed to update it.

**Rocko:** Acknowledged; prefer the current setup for lower user gas costs.

\clearpage
