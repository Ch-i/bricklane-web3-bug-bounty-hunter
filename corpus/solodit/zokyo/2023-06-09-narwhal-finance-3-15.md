---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-15
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Same contract written twice
vuln_class: []
---

# Same contract written twice

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational


**Status**: Acknowledged

**Description**

Vester.sol/VesterNLP.sol - Vester and VesterNLP are basically the same contract. Code repetition on that big scale is not advisable.

**Recommendation** 

Vester/VesterNLP inherit the common logic (which is basically the whole contract) from a base contract. Or implement one vester contract with two different settings on deployment (i.e. one points at NarwhalPool, other points at TradingVault).

**Fix** -  As of  commit a72e06b , note is acknowledged and no change by dev team. There is no significance in this issue as it does not affect the logic nor introduce a vulnerability.
