---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Auto-draw on `AccountableFixedTerm::pay` lets third parties force unwanted
  borrowing
vuln_class: []
---

# Auto-draw on `AccountableFixedTerm::pay` lets third parties force unwanted borrowing

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

In [`AccountableFixedTerm::pay`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableFixedTerm.sol#L354-L357), any positive `_loan.drawableFunds` are automatically drawn via `_updateAndRelease(drawableFunds)` before transferring the due interest/fees:
```solidity
uint256 drawableFunds = _loan.drawableFunds;
if (drawableFunds > 0) {
    _updateAndRelease(drawableFunds);
}
```

Since `_loan.drawableFunds` increases when users deposit/mint into the vault, a third party can deposit immediately before the borrower calls `pay`. This causes `pay` to both increase `_loan.outstandingPrincipal` by the new liquidity and also add remaining-term interest on that added principal, while releasing the assets to the borrower, without borrower consent.

**Impact:** Borrower loses discretion over principal size. Calling `pay` can increase debt (principal + future interest) unexpectedly. This enables griefing/economic DoS as attackers can “stuff” the vault before each payment window, repeatedly forcing draws and increasing interest payments in the future.

**Recommended Mitigation:** Consider removing auto-draw from `AccountableFixedTerm::pay`. Loan increases should occur only via an explicit borrower action (e.g., `draw(uint256)`), not implicitly during interest payment.

**Accountable:** Fixed in commit [`03f871b`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/03f871bfc7baff5fe5f9dfbd8a0ef74e99619e78)

**Cyfrin:** Verified. "auto-draw" is removed from `pay`.
