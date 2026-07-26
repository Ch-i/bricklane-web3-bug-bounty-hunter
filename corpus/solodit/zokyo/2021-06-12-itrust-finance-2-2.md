---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Unused method for paused status
vuln_class: []
---

# Unused method for paused status

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Vault.sol, 437 _ifNotPaused() is never used.
So it makes function isPaused() from iTrustVaultFactory.sol unused as well.
Also these method are actual duplicates for isActiveVault() method, so isPaused() can be safely
removed.

**Recommendation**:

Remove unused method.
