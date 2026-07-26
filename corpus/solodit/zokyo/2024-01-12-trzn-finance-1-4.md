---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Uncalled base constructor in MultiSig
vuln_class: []
---

# Uncalled base constructor in MultiSig

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**



The base constructor of the Ownable contract is not called in the MultiSig contract. This means that the initialOwner variable of the Ownable contract is not assigned.

**Recommendation**: 

It is advised to initialize the constructor of the Ownable contract with a call to Ownable(initialOwner) in the constructor of the MutiSig_V2 contract. 
For example: constructor(address[] memory _whiteWallet, uint _numConfirmationsRequired, address _stableToken, address initialOwner) Ownable (initialOwner){}
