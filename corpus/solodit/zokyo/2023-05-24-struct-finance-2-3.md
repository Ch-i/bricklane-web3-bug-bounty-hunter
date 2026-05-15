---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Governance can indefinitely disable withdrawal of user funds
vuln_class: []
---

# Governance can indefinitely disable withdrawal of user funds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity** : Informational 

**Status**: Acknowledged

**Description**

In contract FEYTraderJoeProduct, function withdrawn(), allows a user to withdraw the investment from the product once the tranche is matured. The gacPausable() modifier is used in Withdrawn Function to check whether the contract is currently paused or not, if the contract is paused it restrict the deposits of users 

**Recommendation**: 

Withdrawals should never be paused because it affects the decentralization nature of the blockchain. Remove gacPausable modifier 

**Comment**: Governance will be a multisig.
