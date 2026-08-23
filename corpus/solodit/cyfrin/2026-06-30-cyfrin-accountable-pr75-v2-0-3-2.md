---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-3-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`AccountableYield::_accrueFees` re-reads the vault `totalSupply` already loaded
  by `_accruedFeeShares`'
vuln_class: []
---

# `AccountableYield::_accrueFees` re-reads the vault `totalSupply` already loaded by `_accruedFeeShares`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** `_accrueFees` runs on every deposit, mint, borrow, repay, and NAV publish. It calls `_accruedFeeShares` (`src/strategies/AccountableYield.sol:504`), which reads the vault `totalSupply` (`src/strategies/AccountableYield.sol:565`), and then `_accrueFees` reads `totalSupply` again (`src/strategies/AccountableYield.sol:511`) to compute the post-fee high-water mark. No shares are minted between the two reads (the fee-share mints happen later at `src/strategies/AccountableYield.sol:545,549`), so the second cross-contract `STATICCALL` returns an identical value and repeats work already done. `_sharePrice` (`src/strategies/AccountableYield.sol:617-623`) has the same pattern: it calls `_accruedFeeShares` and then re-reads `totalSupply`.

```solidity
AccountableYield.sol
504:        (uint256 performanceFeeShares, uint256 managementFeeShares, uint256 newTotalAssets) = _accruedFeeShares();
565:        uint256 supply = IAccountableVault(vault_).totalSupply();      // inside _accruedFeeShares
511:        uint256 totalSupply = IAccountableVault(vault).totalSupply();  // re-read on the same path, no mint between
```

**Recommended Mitigation:** Have `_accruedFeeShares` also return the `supply` it already loads, and consume that value in `_accrueFees` (and in `_sharePrice`) instead of issuing a second `totalSupply` call. This removes one external `STATICCALL` per fee accrual on every deposit, mint, borrow, repay, and NAV-publish path.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.

\clearpage
