---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Use require for checking if  USDT.approve was successful
vuln_class: []
---

# Use require for checking if  USDT.approve was successful

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In NarhwhalReferrals contract, in the claimRewards method, if user opted for compound then the USDT is approved first before depositing to the vault.
USDT token contract returns true if approval is successful so it is advised to use require statement.

**Recommendation**: 

Update the USDT.approve(...) line with the following
`require(IERC20(USDT).approve(TradingVault, pendings), “approval failed”)`
**Fixed**: Issue fixed in commit a72e06b
