---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Checks-effects-interactions
vuln_class: []
---

# Checks-effects-interactions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Methods not following checks-effects-interactions pattern
```solidity
TradingVaultV2.harvest(address)
IERC20(esnar).safeTransfer(user, pendingTokens);
rewardsToken += pendingTokens;

TradingVaultV2.distributeRewardUSDT(uint,bool)
transferFrom precedes updating contract's state
if (_send) {
    IERC20(USDT).safeTransferFrom(msg.sender, address(this), _amount);
}
currentBalanceUSDT = currentBalanceUSDT.add(_amount);

TradingVaultV2.receiveUSDTFromTrader(address,uint,uint,bool)
Interaction with storageT is taking place before state update.
storageT.transferUSDT(address(storageT), address(this), _amount);
currentBalanceUSDT += _amount;
```

**Recommendation** 

transfer which represents external interactions should take place after the effects.

**Fixed**: Issue fixed in commit a72e06b
