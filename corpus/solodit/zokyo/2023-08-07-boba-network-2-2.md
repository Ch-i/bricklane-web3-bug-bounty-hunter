---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-08-07-boba-network-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-08-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md
tags:
- firm:zokyo
- report:2023-08-07-boba-network
title: '`getUserOpHashes()` Can Cause Unexpected Behavior'
vuln_class: []
---

# `getUserOpHashes()` Can Cause Unexpected Behavior

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-08-07-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba%20Network.md)_

---

**Description**

In the contract, 'EntryPointWrapper.sol', 'getUserOpHashes() on line 196 may cause unexpected behavior. If the wrong 'entryPoint address is input to the function parameters, then it will revert. There could be a check to ensure the right EntryPoint is used or removed from the parameters. Even if it is implied for one contract per chain, this might lower risk of accidental error.

**Recommendation**

1. Add a simple check to ensure the right entrypoint is used to ensure all hashes are the same. As the return value will hash something else with the wrong 'Entrypoint address. If this check is supposed to be off-chain, then proper documentation should be completed for developers to understand the importance.
2. Remove `IEntryPoint entryPoint from the function parameter as it is already defined inside the constructor.

**Re-audit comment**

Acknowledged.
Comment: The client acknowledges the finding but did not make any changes as there will only be one contract.
