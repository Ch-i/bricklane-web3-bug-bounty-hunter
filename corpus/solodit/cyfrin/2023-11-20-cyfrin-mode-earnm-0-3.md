---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Owner can rug-pull redemption tokens leaving mystery box contract insolvent
  and mystery box holders unable to redeem
vuln_class: []
---

# Owner can rug-pull redemption tokens leaving mystery box contract insolvent and mystery box holders unable to redeem

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** [`MysteryBox::ownerWithdrawEarnm()`](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L765-L777) allows the owner to transfer the contract's total redemption token balance to themselves, rug-pulling the redemption tokens which mystery boxes are supposed to be redeemed for.

**Impact:** The contract becomes totally insolvent and mystery box owners are unable to redeem.

**Recommended Mitigation:** The contract should always have the necessary tokens to payout the maximum redemption liability on all currently minted and unclaimed mystery boxes. The owner should only be able to withdraw the surplus amount (the excess over the total liability).

When mystery boxes are minted the total liability increases and when mystery boxes are claimed the total liability decreases. Consider tracking the total liability as mystery boxes are minted & claimed and only allowing the owner to withdraw the surplus tokens above this value.

**Mode:**
Fixed in commit [db7b48e](https://github.com/Earnft/smart-contracts/commit/db7b48e69c33e327d613f88035c8335531572e8d), [edefb61](https://github.com/Earnft/smart-contracts/commit/edefb61534ecee1a2f6cb7e687c113a1f7b82056), [a65a50c](https://github.com/Earnft/smart-contracts/commit/a65a50ca8af4d6abc58d3c429785bcd82182c04e).

**Cyfrin:** Verified.
