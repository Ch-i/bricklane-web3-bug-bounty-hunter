---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Check `boxAmount < 100` only once before loop in `MysteryBox::_assignTierAndMint()`
vuln_class: []
---

# Check `boxAmount < 100` only once before loop in `MysteryBox::_assignTierAndMint()`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** As `boxAmount` input is static, [check `boxAmount < 100`](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L479) only once before loop in `MysteryBox::_assignTierAndMint()`.

**Impact:** Gas optimization.

**Recommended Mitigation:** See description.

**Mode:**
Fixed in commit [06a6a4f](https://github.com/Earnft/smart-contracts/commit/06a6a4f6f12e5a52f797af26c4a27a4994fe6ce1).

**Cyfrin:** Verified.

\clearpage
