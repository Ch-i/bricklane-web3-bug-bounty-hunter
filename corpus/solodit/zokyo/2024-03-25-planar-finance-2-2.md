---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Inefficient ETH Transfer Method
vuln_class: []
---

# Inefficient ETH Transfer Method

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Status**:  Unresolved

**Severity**: informational

**Source**: ./Refund.sol


**Description**:

The `_safeTransferETH` function in the smart contract uses a less efficient method for transferring ETH, which can lead to excessive gas usage.


**Recommendation**
```solidity
function _safeTransferETH(address to, uint256 amount) internal {
    bool success;

    /// @solidity memory-safe-assembly
    assembly {
        // Transfer the ETH and store if it succeeded or not.
        success := call(gas(), to, amount, 0, 0, 0, 0)
    }

    require(success, "ETH_TRANSFER_FAILED");
}
```
