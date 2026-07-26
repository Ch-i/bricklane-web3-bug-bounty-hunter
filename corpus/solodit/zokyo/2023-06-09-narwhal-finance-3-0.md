---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing import of `Initializable` contract
vuln_class: []
---

# Missing import of `Initializable` contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**

Contract NarwhalRefferal and Contract Narwhal Trading is using `initialize(...)` method with `initializer` modifier. 
This modifier is from `Initializable` contract which is not imported and inherited in both of these unlike in Trading Storage & NarwhalTradingCallbacks contract. It is recommended in OpenZeppelin documentation as well.

**Recommendation**: 

Import and inherit the `Initializable` contract.

**Fix1**: Initializable has been imported but not inherited for the Trading Storage & NarwhalTradingCallbacks contract. Import the initializable contracts same as in NarhwalTradingCallbacks.sol


**Fix-2**: Issue fixed in commit 5055e7
