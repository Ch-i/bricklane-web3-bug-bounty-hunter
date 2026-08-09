---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Storage constants should be used.
vuln_class: []
---

# Storage constants should be used.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: function_process UserWithBounty(), line 184; bountyForUser(), line 277, value "10000". 
Eligibility DataProvider.sol: required UsdValue(), line 159, value "1e4". 
MiddleFee Distribution.sol: mint(), line 171; forward Reward(), line 197, 204, value "1e4". 
MFDstats.sol: add Transfer(), line 80, 90, value "1e4". 
LockZap.sol: lines 105, 107, values "10000", "9500". 
Leverager.sol: lines 107, 117, 141, 154, value "1e4". 
RadiantOFT.sol: _getBridgeFee(), line 114, value "1e4". 
StargateBorrow.sol: getXChain Borrow FeeAmount(), line 105, value "1e4". 
In order to increase readability of the contracts, it is recommended to use storage constants instead of values directly. 

**Recommendation**: 

Use storage constants instead of values directly in code.
