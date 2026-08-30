---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Instant governance transfer
vuln_class: []
---

# Instant governance transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

 **Description**
 
Contracts TradingStorage.sol, BaseToken.sol, Vester.sol, VesteNPL.sol use setGov function for transferring ownership. In case of a mistake in the provided address, the management of the particular contract will be irretrievably lost.

**Recommendation**: 

Modify the process of updating the governance to be a two-step process, similar to the one used in the NarwhalPool.sol contract. This will require the new owner to explicitly accept the ownership update.

**Fixed**: Protocol added a two-step of updating the governance.
