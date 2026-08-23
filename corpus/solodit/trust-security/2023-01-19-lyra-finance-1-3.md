---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-4 sendAllFundsToLP() does not handle popular ERC20 tokens like BNB
vuln_class: []
---

# TRST-M-4 sendAllFundsToLP() does not handle popular ERC20 tokens like BNB

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
sendAllFundsToLP() is used to transfer quote and base tokens to the LP after interaction with 
GMX. It uses an unsafe transfer call:
```solidity
    if (baseBal > 0) {
       if (!baseAsset.transfer(address(liquidityPool), baseBal)) {
    revert AssetTransferFailed(address(this), baseAsset, baseBal, 
         address(liquidityPool));
     }
    emit BaseReturnedToLP(baseBal);
```
There are a great many tokens such as BNB and USDT that for historical reasons, don’t return 
a value in transfer(). Since Lyra aims to support blue-chip tokens, it should refactor and use 
the safe transfer variant.

**Recommended mitigation:**
Use Open Zeppelin’s SafeERC20 encapsulation of ERC20 transfer functions.

**Team response:**
USDT/BNB will not be supported for this set of contracts. Tokens supported will be limited to 
only those that do not return boolean values.
