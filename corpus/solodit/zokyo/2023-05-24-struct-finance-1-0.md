---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Authorization of only EOAs can break multisigs
vuln_class: []
---

# Authorization of only EOAs can break multisigs

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

The onlyEOAOrRole() modifier in the GACManaged contract, allows only EOAs to interact with the contracts that use this modifier. Smart contracts ideally should NOT be "not allowed" to interact with the client's contracts as it could break the client's smart contract's support with multisig contracts of users, which in turn is not advised for security. This is because usage of multisig contracts or wallets to interact with smart contracts is considered a good security practice. 

For example, if a user is using Gnosis safe to interact with the Product contract, the interaction will not be allowed as Gnosis safe(i.e. multisig) is a smart contract. 

**Remediation**- 

It is advised to remove disallowing smart contracts from interacting with the client's smart contracts unless absolutely necessary.
