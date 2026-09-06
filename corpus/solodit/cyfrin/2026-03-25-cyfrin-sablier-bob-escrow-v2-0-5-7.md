---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`SablierBob::_unstakeFullAmountViaAdapter` should take `vault.adapter` as
  input parameter'
vuln_class: []
---

# `SablierBob::_unstakeFullAmountViaAdapter` should take `vault.adapter` as input parameter

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierBob::_unstakeFullAmountViaAdapter` should take `vault.adapter` as an input parameter since both callers already read it, so there is no point in re-reading it again from storage when the value is already known.

**Sablier:** Fixed in commit [7d9ac86](https://github.com/sablier-labs/lockup/commit/7d9ac86a6edc85383b1fc9b58fdfbaf78a8f1cb1).

**Cyfrin:** Verified.
