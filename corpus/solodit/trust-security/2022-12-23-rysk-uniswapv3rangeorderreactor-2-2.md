---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2022-12-23-rysk-uniswapv3rangeorderreactor-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md
tags:
- firm:trust-security
- report:2022-12-23-rysk-uniswapv3rangeorderreactor
title: TRST-L-3 Lack of logging in important functions
vuln_class: []
---

# TRST-L-3 Lack of logging in important functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2022-12-23-rysk UniswapV3RangeOrderReactor.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2022-12-23-rysk%20UniswapV3RangeOrderReactor.md)_

---

**Description:**
For the sake of transparency, it is recommended to emit events during maintenance transfer 
of funds into and out of contracts. Make sure to add events for `withdraw()`, `recoverETH()` and 
`recoverERC20()`.

**Recommended Mitigation:**
Add the events listed above.

**Team response:**
Fixed

**Mitgation review:**
The issue was fixed with additional logging. However, the fix introduced an issue. In the 
event that logs withdraw, if withdrawal amount is greater than balance than the log will be 
incorrect.
```solidity
        if (_amount <= balance) {
             SafeTransferLib.safeTransfer(ERC20(collateralAsset), msg.sender, _amount);
        emit Withdraw(_amount);
        // return in collateral format
             return _amount;
                 } else {
        SafeTransferLib.safeTransfer(ERC20(collateralAsset), msg.sender, balance);
        emit Withdraw(_amount);
        // return in collateral format
                return balance;
             }
```
Correct behavior would be to log balance
