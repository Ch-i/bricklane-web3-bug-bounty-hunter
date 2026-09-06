---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing validation
vuln_class: []
---

# Missing validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity** : Low

**Status**: Resolved

**Description**

The setTradingVault function in the NarwhalReferrals contract allows the owner to set the address of the trading vault. However, the function does not check whether the new TradingVault address is valid or not, so there is a risk that an invalid address may be set accidentally or intentionally. This can compromise the security of the system
**Impact** : 
If Attacker gets the access of Owner then attacker can setup Malicious Vault as TradingVault

**Recommendation** 

TradingVault address can be initialised in the constructor to ensure that it is set correctly from the start.

**Fixed**: 

Issue fixed in commit a72e06b
