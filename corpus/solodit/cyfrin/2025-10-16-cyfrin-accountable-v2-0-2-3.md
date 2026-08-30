---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: InvestmentManager can use `AccountableFixedTerm::coverDefault` to misuse token
  approvals from anyone
vuln_class: []
---

# InvestmentManager can use `AccountableFixedTerm::coverDefault` to misuse token approvals from anyone

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** `AccountableFixedTerm::coverDefault` allows InvestmentManager of the loan to add additional assets to the system.

```solidity
    function coverDefault(uint256 assets, address provider) external onlySafetyModuleOrManager whenNotPaused {
        _requireLoanInDefault();

        loanState = LoanState.InDefaultClaims;

        IAccountableVault(vault).lockAssets(assets, provider);

        emit DefaultCovered(safetyModule, provider, assets);
    }
```

And `lockAssets()` pulls assets from the input "provider" address, transferring them to the vault.

This means any user address who had asset token balance, and approved the vault contract (potential pending approvals from the past) is at risk of losing their funds here.

The Manager can pull funds from a random provider address without any permissions, and the "provider" would lose his approved funds without getting anything in return.

**Impact:** Any pending asset approvals from user => vault contract, can be misused to cover loan default.

The same problem also exists in AccountableOpenTerm.

**Recommended Mitigation:** Consider removing the "provider" address logic from `coverDefault()`, and simply pull assets from `msg.sender`.

**Accountable:** Fixed in commit [`014d7fb`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/014d7fb6f11766fada9054a736a264cf1d95c9f6)

**Cyfrin:** Verified. `provider` is removed.
