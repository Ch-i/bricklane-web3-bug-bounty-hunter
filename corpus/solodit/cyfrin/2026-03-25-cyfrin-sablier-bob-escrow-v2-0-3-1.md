---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`feeAmount` never set when no vault adapter used in `SablierBob::redeem`'
vuln_class: []
---

# `feeAmount` never set when no vault adapter used in `SablierBob::redeem`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** When no vault adapter is used in `SablierBob::redeem`, the output `feeAmount` is never set even though:
* the user does pay a fee as `msg.value`
* `feeAmount` is returned as an output variable and also emitted in the `Redeem` event

**Sablier:** Fixed in commit [75448ba](https://github.com/sablier-labs/lockup/commit/75448ba4e6f5f22207cc5b03096206a7708e5a54) by renaming `feeAmount` to `feeAmountDeductedFromYield` to make it explicit that this applies only when vault adapters are used.

**Cyfrin:** Verified.
