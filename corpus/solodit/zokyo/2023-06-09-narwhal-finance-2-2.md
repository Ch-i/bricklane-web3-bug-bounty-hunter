---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Events lacking
vuln_class: []
---

# Events lacking

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

no events emitted in admin/gov setters:
Vester.sol/VesterNLP
setHandler()
setNarwhalPool() - setTradingVault()
setHasMaxVestableAmount()
setTransferredAverageStakedAmounts()
settransferredCumulativeRewards()

In TradingVaultV2.sol
setRewardsDuration()
setAllowed()
setRewardToken()
setVester()
setWithdrawTimelock()

In NarwhalReferrals.sol
setBaseRebatesAndDiscounts()
setTier3Tier2RebateBonus()
setTradingVault()
setWhitelistedAddress()

In NarwhalPriceAggregator.sol
setUSDTFeed(bytes32 _feed)
setOracle(address _oracle)
setAge(uint256 _age)
setNarwhalTrading(address _NarwhalTrading)

In NarwhalTrading.sol
setAllowedToInteract(address, bool)
Fixed: Issue fixed in commit a72e06b
