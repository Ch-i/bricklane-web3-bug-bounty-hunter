---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Redundant return
vuln_class: []
---

# Redundant return

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

SupplySourceHelper.sol - extra line for return ret; is unneeded because ret is already assigned and returning the values it is assigned to by default.
```solidity
   /// @notice Gets the balance in our treasury.
    function balance(SupplySource memory supplySource) internal view returns (uint256 ret) {
        if (supplySource.kind == SupplyKind.Native) {
            ret = address(this).balance;
        } else if (supplySource.kind == SupplyKind.ERC20) {
            ret = IERC20(supplySource.tokenAddress).balanceOf(address(this));
        }
        return ret;
    }
```
**Recommendation**

Omit the return statement.

**Fix**: Issue addressed and resolved according to recommendation in commit 9a663e5 .
