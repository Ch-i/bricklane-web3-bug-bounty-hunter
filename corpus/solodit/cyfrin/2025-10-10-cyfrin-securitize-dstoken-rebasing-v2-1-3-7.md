---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Remove obsolete `return` statements when already using named return variables
vuln_class: []
---

# Remove obsolete `return` statements when already using named return variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Remove obsolete `return` statements when already using named return variables.

* `contracts/utils/BulkBalanceChecker.sol`
```solidity
43:        return balances;
```

* `contracts/swap/SecuritizeSwap.sol`
```solidity
236:       return (dsTokenAmount, currentNavRate);
```

**Securitize:** Fixed in commit [f3daea2](https://github.com/securitize-io/dstoken/commit/f3daea22479e95886f25e2c3a70b9618fed97a1c) for `BulkBalanceChecker`; `SecuritizeSwap` was deleted as it is obsolete.

**Cyfrin:** Verified.
