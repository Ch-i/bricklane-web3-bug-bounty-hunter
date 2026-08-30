---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-10-13-thestandard-io-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md
tags:
- firm:zokyo
- report:2022-10-13-thestandard-io
title: Incomplete removal of multiply-added tokens in TokenManager.
vuln_class: []
---

# Incomplete removal of multiply-added tokens in TokenManager.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-10-13-TheStandard.io.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-10-13-TheStandard.io.md)_

---

**Description**

TokenManager.sol
Removing an accepted token that is added by the owner multiple times is possibly not removed completely in a single transaction.
Example flow:
Initialize contract
- Add a token e.g, "usdt" 3 times.
Call getAcceptedTokens. Result: ['weth', 'usdt', 'usdt', 'usdt']
Remove the token e.g. "usdt" 1 time
Call getAcceptedTokens Result: ['weth', 'usdt']

**Recommendation**

Allow only unique tokens to be added to the accepted token symbols.

**Re-audit comment**

Resolved
