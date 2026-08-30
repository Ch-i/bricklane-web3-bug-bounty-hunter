---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Lack of Minimum Fee Validation in `setDefaultFee` Function
vuln_class: []
---

# Lack of Minimum Fee Validation in `setDefaultFee` Function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Source**: ./HyperPoolFactory.sol

**Description**:

The `setDefaultFee` function in the `HyperPoolFactory` contract allows the contract owner to set a default fee for hyper pools. However, the function only checks that the new fee does not exceed the `MAX_DEFAULT_FEE` but does not validate a minimum fee threshold. This oversight could potentially allow setting the default fee to 0, which might not align with the protocol's economic model or intentions, 

**Recommendation**:
```solidity
uint256 public constant MIN_DEFAULT_FEE = 1; // Example minimum fee (0.01%), adjust as necessary

function setDefaultFee(uint256 newFee) external onlyOwner {
    require(newFee >= MIN_DEFAULT_FEE && newFee <= MAX_DEFAULT_FEE, "Fee must be between min and max");
    defaultFee = newFee;
    emit SetDefaultFee(newFee);
}
```
Note#5: HyperPool is a permission-less protocol to have other projects to build their Staking and Reward distribution strategies. `defaultFee` is kept to 0 in the beginning to attract protocols and users with no cost and more options.
