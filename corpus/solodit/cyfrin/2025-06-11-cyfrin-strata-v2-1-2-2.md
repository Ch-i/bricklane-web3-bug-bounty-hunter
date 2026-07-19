---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-2-2
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
title: Hard-coded slippage in `pUSDeDepositor::deposit_viaSwap` can lead to denial
  of service
vuln_class: []
---

# Hard-coded slippage in `pUSDeDepositor::deposit_viaSwap` can lead to denial of service

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** [Hard-coded slippage](https://dacian.me/defi-slippage-attacks#heading-hard-coded-slippage-may-freeze-user-funds) in `pUSDeDepositor::deposit_viaSwap` can lead to denial of service and in dramatic cases even [lock user funds](https://x.com/0xULTI/status/1875220541625528539).

**Recommended Mitigation:** Slippage parameters should be calculated off-chain and supplied as input to swaps.

**Strata:** Fixed in commit [2c43c07](https://github.com/Strata-Money/contracts/commit/2c43c07a839eb9d593c6bf67fc1b5c75b694aed7).

**Cyfrin:** Verified. Callers can now override the default slippage.
