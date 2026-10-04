---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[I-01] Introduce validation of the order size'
vuln_class: []
---

# [I-01] Introduce validation of the order size

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/TradeStakeManager.sol#L127)

**Description:**

The Hyperliquid core enforces decimal limits on order sizes for both perps and spots.

According to the documentation: *Prices can have up to 5 significant figures, but no more than `MAX_DECIMALS - szDecimals` decimal places, where `MAX_DECIMALS` is 6 for perps and 8 for spot.* [[ref](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/tick-and-lot-size)]

Implementing similar validation in `TradeStakeManager` would help prevent potential silent failures when an incorrect order size is submitted. While a similar limitation already exists for prices — and `TradeStakeManager` enforces price boundaries — the same should be applied to order sizes.

**Impact:** Proper validation can prevent unnecessary silent failures on the Hyperliquid Core side.

**Recommendation:** Validate order sizes in accordance with Hyperliquid documentation to ensure compliance before submission.

**Status:** Acknowledged

**Client response:** We acknowledge and choose not to implement in the contract. If invalid, hypercore will reject the request. There are many other validations we could do and this fits into the same category
