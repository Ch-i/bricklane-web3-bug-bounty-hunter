---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Reserved assets could be extracted from the Vault
vuln_class: []
---

# Reserved assets could be extracted from the Vault

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Some strategy functions can release assets without checking if those assets are part of `reservedLiquidity`. `AccountableFixedTerm._loan.drawableFunds` is not verified to be in sync with the queue `reservedLiquidity`. Hence the borrower can inadvertently borrow more funds than they should.

**Impact:** The vault can become insolvent by releasing funds needed to honor a withdrawal.

**Proof of Concept:** Violated in `FixedTerm.acceptLoanLocked(), FixedTerm.borrow(), FixedTerm.pay(), FixedTerm.acceptLoanDynamic(), FixedTerm.claimInterest()`: https://prover.certora.com/output/52567/edb399a43d1849a9b22f027e66b17924/?anonymousKey=3dcf62dfa004381083966b3639b6a485fa2e9501

```solidity
// Reserved liquidity must not exceed total assets
invariant reservedLiquidityBacked(env e)
    ghostReservedLiquidity256 <= ghostTotalAssets256
```

**Recommended Mitigation:** When `reservedLiquidity` is increased in the withdrawal queue, this needs to be synced to the FixedTerm starategy.

**Accountable:** Fixed in commit [`979c0e`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/979c0ebe4bd5860fe9b2e446f9fac2ae3919b39c).

Issue was addressed to satisfy the invariant and prevent future upgrades that might allow redemptions in a FixedTerm loan, but as of right now there's no possible way to increase `reservedLiquidity` such that it is out-of-sync with`drawableFunds`.

Borrowing after the loan is in a `Repaid` state cannot happen due to `_requireLoanOngoing` so any redemptions that increase `reservedLiquidity` would require a state when both depositing/borrowing is blocked.

**Cyfrin:** Verified. `reservedLiquidity` is now checked in FixedTerm.
