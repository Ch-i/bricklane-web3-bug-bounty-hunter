---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: In `pUSDeDepositor::deposit_viaSwap`, using `block.timestamp` in swap deadline
  is not very effective
vuln_class: []
---

# In `pUSDeDepositor::deposit_viaSwap`, using `block.timestamp` in swap deadline is not very effective

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** [Using `block.timestamp` in a swap deadline](https://dacian.me/defi-slippage-attacks#heading-no-expiration-deadline) is not very effective since `block.timestamp` will be the block which the transaction gets put in, so the swap will never be able to expire in this way.

Instead the current `block.timestamp` should be retrieved off-chain and passed as input to the swap transaction.

**Strata:** Fixed in commit [2c43c07](https://github.com/Strata-Money/contracts/commit/2c43c07a839eb9d593c6bf67fc1b5c75b694aed7).

**Cyfrin:** Verified. Callers can now override the default swap deadline.
