---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Missing zero address checks
vuln_class: []
---

# Missing zero address checks

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In contract FEYTraderJoeProduct, there is missing zero address for _spToken, _initConfig.configTrancheSr.tokenAddress, _initConfig.configTrancheJr.tokenAddress, _nativeToken, _structPriceOracle, _distributionManager and _yieldSource in the initialize() function.

**Recommendation**: 

It is advised to add zero address checks for the same to avoid incorrect values being assigned.

**Comments**: 

The client stated that the products will be mostly created using the frontend so the users don’t have to worry about the addresses.  And that even if they added zero address check, there are many other addresses whose private key are unknown. They further added that If users or other protocols are interacting with the contract directly they need to be extremely careful when entering the input params.
