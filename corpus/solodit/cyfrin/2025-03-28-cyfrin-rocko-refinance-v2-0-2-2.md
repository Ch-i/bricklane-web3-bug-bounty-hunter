---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Use `msg.sender` instead of `owner()` inside `onlyOwner` functions
vuln_class: []
---

# Use `msg.sender` instead of `owner()` inside `onlyOwner` functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Using `msg.sender` instead of `owner()` inside `onlyOwner` functions is more efficient as it eliminates reading from storage. It is also safe since the `onlyOwner` modifier ensures that `msg.sender` is the owner:
```solidity
757:        IERC20(tokenAddress).safeTransfer(owner(), amount);
766:        (bool success, ) = owner().call{ value: amount }("");
```

**Rocko:** Fixed in commit [751e906](https://github.com/getrocko/onchain/commit/751e906b7c2df6cb587e709b12de25593eb02c75).

**Cyfrin:** Verified.
