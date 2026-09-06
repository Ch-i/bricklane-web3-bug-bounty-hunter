---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`TokenBank::removeToken` reverts when token balance is zero, making it impossible
  to remove tokens from the `developments` array'
vuln_class: []
---

# `TokenBank::removeToken` reverts when token balance is zero, making it impossible to remove tokens from the `developments` array

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** When removing a token from the TokenBank, the removal attempt reverts if it has zero tokens on the TokenBank balance. As time passes the `developments` array will grow having unnecessary tokens inside it that are impossible to remove.

**Impact:** The `developments` array will continue to grow leading to unnecessary waste of gas when claiming fees.

**Recommended Mitigation:** Before calling `withdrawTokens()`, check if the tokenAddress' balance is 0, if so, skip the call (it would anyways revert):
```diff
    function removeToken(address tokenAddress) external restricted {
        ...
-        withdrawTokens(tokenAddress, custodialWallet, 0);
+       if(IERC20(tokenAddress).balanceOf(address(this)) > 0) withdrawTokens(tokenAddress, custodialWallet, 0);
        ...
    }
```

**Remora:** Fixed in commit [2e797fc](https://github.com/remora-projects/remora-smart-contracts/commit/2e797fc45245e3cc731e7f2f70401e8df831f1f3).

**Cyfrin:** Verified.
