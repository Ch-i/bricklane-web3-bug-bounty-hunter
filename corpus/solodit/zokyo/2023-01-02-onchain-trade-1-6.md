---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Centralization risk
vuln_class: []
---

# Centralization risk

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**: Unresolved

**Description**

There are multiple instances where the contract owner can change protocol parameters that affect the behavior of the contracts. These include calls to several functions like updating asset details, protocol revenue and general setters/mutators. 

**Recommendation**: 

Consider using multisig wallets and having a governance module

**Fix#1**: 

No response  to address that the project owners are planning to use multisig wallets to operate the contracts or not.
