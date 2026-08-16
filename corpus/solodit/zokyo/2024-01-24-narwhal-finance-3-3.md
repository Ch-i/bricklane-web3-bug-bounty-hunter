---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Typos
vuln_class: []
---

# Typos

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**


Contract VarCanstant.sol sould be VarConstant.sol.
`Cancle` in many of the contracts should be Cancel.
`factorAddress` in Vault.sol should be factoryAddress.
This require statement in VaultFactory should be updated.
```solidity
       require(_maxVaultCapAmount <= vaultCap, "Factory: vault usdt too high");
```
Function `dealRefereAward` should be `dealReferralAward`

**Recommendation**: 

Fix the typos.
