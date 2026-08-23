---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-4-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Cached `_token0` not used
vuln_class: []
---

# Cached `_token0` not used

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** In [`SmartVaultYieldManager::_swapToSingleAsset`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L114-L117), the cached address `_token0` is not used in the condition of the ternary operation:

```solidity
address _token0 = IHypervisor(_hypervisor).token0();
address _unwantedToken = IHypervisor(_hypervisor).token0() == _wantedToken ?
    IHypervisor(_hypervisor).token1() :
    _token0;
```

**Recommended Mitigation:** Use the cached `_token0` variable in the comparison.

**The Standard DAO:** Fixed by commit [`1c30144`](https://github.com/the-standard/smart-vault/commit/1c3014465689d75d1fc057cadb5cdd75d8f18a2d).

**Cyfrin:** Verified, the cached address is now used.

\clearpage
