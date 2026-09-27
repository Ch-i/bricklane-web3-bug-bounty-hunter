---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-7
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`IReceipt::redeem` amount overload NatSpec misstates the revert for amounts
  above the caller''s balance'
vuln_class: []
---

# `IReceipt::redeem` amount overload NatSpec misstates the revert for amounts above the caller's balance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `IReceipt::redeem(uint256)` documents that before `exerciseDeadline` an `amount` above the caller's balance is not an error, and that after the deadline it reverts `InsufficientPool` rather than `ERC20InsufficientBalance`. Neither holds once a market has more than one holder: `Receipt::_redeem` caps `amount_` against the global `consBacked` and never against the caller's balance, so it reaches `_burn` and reverts `ERC20InsufficientBalance` in both cases. The `_redeem` dev-comment already hedges the opposite way, so the two doc sites disagree.

**Impact:** The `redeem(uint256)` NatSpec is not correct on either side of the deadline, and no funds are affected.

**Recommended Mitigation:** Correct the `IReceipt::redeem(uint256)` NatSpec to match the implementation, or clamp `amount_` to the caller's balance in `Receipt::_redeem`.

**GreekFi:** Fixed in [PR45](https://github.com/greekfi/contracts/pull/45)

**Cyfrin:** Verified. The redeem amount NatSpec now describes the actual capped pre-deadline burn, full post-deadline burn, and possible revert ordering.
