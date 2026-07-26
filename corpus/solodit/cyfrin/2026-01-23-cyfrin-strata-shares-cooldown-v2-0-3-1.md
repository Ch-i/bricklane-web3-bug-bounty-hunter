---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Redundant `user` parameter as it can only be set to `msg.sender` on `SharesCooldown::finalizeWithFee`
  and `SharesCooldown::cancel` functions
vuln_class: []
---

# Redundant `user` parameter as it can only be set to `msg.sender` on `SharesCooldown::finalizeWithFee` and `SharesCooldown::cancel` functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `SharesCooldown::finalizeWithFee` and `SharesCooldown::cancel` functions restrict the `user` parameter to being the `msg.sender`; if any other value is set, the tx reverts, which means using that parameter is redundant because `msg.sender` could be directly used.
```solidity
    modifier onlyUser (address user) {
@>      require(msg.sender == user, "OnlyOwner");
        _;
    }

function finalizeWithFee(ITranche vault, address user, uint256 i) external onlyUser(user) returns (uint256 claimed) {
        ...
}

function cancel(IERC20 vault, address user, uint256 i) external onlyUser(user) {
        ...
}


```

**Recommended Mitigation:** Consider removing the `user` parameter from the functions `finalizeWithFee` and `cancel`. Instead, use `msg.sender`.

**Strata:** Acknowledged. Keep it for consistency with the permissionless interface. Additionally, we may later introduce new roles for finalization, allowing third parties to finalize on behalf of users.

\clearpage
