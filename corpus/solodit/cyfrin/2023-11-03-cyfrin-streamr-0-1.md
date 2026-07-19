---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Possible overflow in `_payOutFirstInQueue`
vuln_class: []
---

# Possible overflow in `_payOutFirstInQueue`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** High

**Description:** In `_payOutFirstInQueue()`, possible revert during `operatorTokenToDataInverse()`.

```solidity
uint amountOperatorTokens = moduleCall(address(exchangeRatePolicy), abi.encodeWithSelector(exchangeRatePolicy.operatorTokenToDataInverse.selector, amountDataWei));
```

If a delegator calls `undelegate()` with `type(uint256).max`, `operatorTokenToDataInverse()` will revert due to uint overflow and the queue logic will be broken forever.

```solidity
   function operatorTokenToDataInverse(uint dataWei) external view returns (uint operatorTokenWei) {
       return dataWei * this.totalSupply() / valueWithoutEarnings();
   }
```

**Impact:** The queue logic will be broken forever because `_payOutFirstInQueue()` keeps reverting.

**Recommended Mitigation:** We should cap `amountDataWei` before calling `operatorTokenToDataInverse()`.

**Client:** Fixed in commit [c62e5d9](https://github.com/streamr-dev/network-contracts/commit/c62e5d90ce8f8c084fe3917f499c967c85a3873b).

**Cyfrin:** Verified.
