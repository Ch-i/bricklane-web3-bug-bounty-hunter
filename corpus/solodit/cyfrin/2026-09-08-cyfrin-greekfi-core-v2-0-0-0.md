---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::_payout` lets attacker-chosen token granularity bypass all redemption
  fees'
vuln_class: []
---

# `Receipt::_payout` lets attacker-chosen token granularity bypass all redemption fees

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::_payout` calculates fees in the payout token's raw units and rounds down. Market creation is permissionless and imposes no minimum token decimals, so an attacker can deploy a zero-decimal wrapper whose single unit represents a valuable amount of an underlying asset.

For any fee below 100%, redeeming one unit produces a zero fee. Partial redemption lets the holder repeat one-unit redemptions, bypassing a fee that would be charged if the position were redeemed at once.

Ordinary rounding loses less than one raw unit per call. Here, the attacker controls the denomination and can make that raw unit economically valuable, turning marginal rounding into a complete fee bypass.

**Impact:** All redemption fees can be avoided in wrapper-denominated markets. The wrapper can be fully backed and redeemable, allowing genuine volume to be routed through the affected market. Fee loss is repeatable and scales with volume. Solvency and other holders' claims are unaffected.

**Recommended Mitigation:** Round nonzero fees up or carry fractional fees in accounting that cannot be reset through redemption splitting, token transfers, or new markets. Otherwise, restrict coarse token denominations or charge fees in a separate high-precision asset.

**GreekFi:** Fixed in [PR31](https://github.com/greekfi/contracts/pull/31)

**Cyfrin:** Verified. Receipt now rounds nonzero redemption fees up, so splitting redemptions or using a coarse token denomination cannot reduce the fee to zero.

\clearpage
